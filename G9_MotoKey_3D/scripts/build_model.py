"""SafeLock Smart G9 — parametric concept assembly. Coordinates and CAD in mm.
X: grip axis; Y: towards brake lever; Z: up. No vehicle dimensions claimed universal.
"""
from pathlib import Path
import json, math, csv
import cadquery as cq
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
for d in ['CAD','STL','presentation','research']: (ROOT/d).mkdir(exist_ok=True)
PARTS=[]
COLORS={'shell':'#26323b','orange':'#ed762e','steel':'#a4b2bc','rubber':'#202326','pcb':'#176e63','gold':'#d5ac58','battery':'#b8c9d3','white':'#e8ece9','led':'#8ae6c5'}

def box(x,y,z,p=(0,0,0),r=0):
    w=cq.Workplane('XY').box(x,y,z)
    if r:
        try: w=w.edges('|Z').fillet(r)
        except Exception: pass
    return w.translate(p).val()

def cylx(r,l,p): return cq.Solid.makeCylinder(r,l,cq.Vector(p[0]-l/2,p[1],p[2]),cq.Vector(1,0,0))
def cylz(r,l,p): return cq.Solid.makeCylinder(r,l,cq.Vector(p[0],p[1],p[2]-l/2),cq.Vector(0,0,1))
def add(id,name,shape,color,group,exp=(0,0,0),material='',note='',printable=False):
    if not shape.isValid(): raise ValueError('Invalid CAD: '+id)
    PARTS.append(dict(id=id,name=name,shape=shape,color=COLORS.get(color,color),group=group,explode=exp,material=material,note=note,printable=printable))
    print(id,round(shape.Volume(),2),flush=True)
    return shape

grip_bore=cylx(20.3,80,(0,-25,0))
lever_bore=box(80,20,16,(0,29,0),r=0)
hinge=(0,-53,0)
hinge_upper=cylx(6,27,hinge).cut(cylx(3.15,30,hinge)).fuse(box(27,7,16,(0,-49.5,12)))
hinge_lower=[cylx(6,9,(x,-53,0)).cut(cylx(3.15,12,(x,-53,0))) for x in [-19,19]]
receiver=box(29,20,20,(0,49,-13)).cut(box(8.1,14.5,25,(0,49,-10))).cut(cylx(3.2,40,(0,48,-11))).cut(cylx(7.2,17,(16.5,48,-11)))
def half(shape,upper): return shape.intersect(box(300,400,100,(0,0,50 if upper else -50)))

# Two polymer covers. Four steel side plates carry the mechanical load.
cores={}
for upper in [False,True]:
    tag='upper' if upper else 'lower'; sign=1 if upper else -1
    for side in [-1,1]:
        plate=box(3,112,24,(side*16,-0,sign*12),r=0).cut(grip_bore).cut(lever_bore)
        plate=plate.cut(cylx(3.15,80,hinge))
        if upper:
            plate=plate.cut(cylx(6.4,80,hinge))
            plate=plate.cut(box(90,30,80,(0,-68,0)))
        # Front bolt/cylinder hole through bottom load plates only.
        if not upper: plate=plate.cut(cylx(7.2,90,(0,48,-11)))
        cores[(tag,side)]=plate

for upper in [False,True]:
    tag='upper' if upper else 'lower'; sign=1 if upper else -1
    outer=box(48,120,27,(0,0,sign*13.5),r=6)
    # Accessible hollow shell, with two transverse support webs.
    cavity=box(39,110,23,(0,0,sign*11.1),r=3)
    cover=outer.cut(cavity).cut(grip_bore).cut(lever_bore)
    for y in [-48,6,47]:
        web=box(39,3,23,(0,y,sign*12),r=0).cut(grip_bore).cut(lever_bore)
        cover=cover.fuse(web)
    for side in [-1,1]:
        # Slots seat steel inserts, with 0.2mm per-side assembly allowance.
        slot=box(3.4,113,24.5,(side*16,0,sign*12),r=0).cut(grip_bore).cut(lever_bore)
        cover=cover.cut(slot)
    # Clear the other half's knuckle before adding complementary hinge segments.
    cover=cover.cut(cylx(6.4,70,hinge))
    # Metal knuckles, not polymer, transfer load into the steel skeleton.
    if upper:
        cover=cover.cut(box(27.5,7.5,20,(0,-49.5,12)))
        # Rear lip must stop at the hinge axis; otherwise it sweeps into the lower half.
        cover=cover.cut(box(90,30,80,(0,-68,0)))
    cover=cover.cut(cylx(3.15,70,hinge))
    if not upper:
        cover=cover.cut(cylx(7.5,80,(0,48,-11)))
        cover=cover.cut(box(9.0,15.0,25,(0,49,-9)))
        cover=cover.cut(receiver)
    else:
        cover=cover.cut(box(8.5,11.4,40,(0,48,0)))
        # Pod cable feedthrough above cavity; filled with silicone grommet.
        cover=cover.cut(cylz(2.6,8,(0,5,25)))
    if len(cover.Solids())>1:
        print('Cover solids before cleanup',tag,[round(s.Volume(),3) for s in cover.Solids()],flush=True)
        cover=max(cover.Solids(),key=lambda s:s.Volume())
    add('01_'+tag+'_cover','Nắp kẹp trên' if upper else 'Thân kẹp dưới',cover,'shell','upper' if upper else 'lower',(0,0,sign*13),'PA6-GF30 / mẫu PA12','Vỏ không được tính là bộ phận chống cắt chính.',True)

for (tag,side),plate in cores.items():
    add('02_core_'+tag+('_L' if side<0 else '_R'),'Lõi thép '+('trên' if tag=='upper' else 'dưới')+(' trái' if side<0 else ' phải'),plate,'steel','upper' if tag=='upper' else 'lower',(side*27,0,8 if tag=='upper' else -8),'Thép 40Cr, dày 3 mm','Cắt laser, gia công lỗ; nhiệt luyện và chống gỉ theo thử nghiệm.')

# Steel end crossbars tie the side plates together and transfer latch/hinge loads.
for upper in [False,True]:
    sign=1 if upper else -1; tag='upper' if upper else 'lower'
    for idx,y in enumerate([-51,48]):
        bridge=box(29,7,6,(0,y,sign*20),r=0)
        if not upper and idx==1: bridge=box(29,20,6,(0,49,-20)).cut(box(8.5,14.5,12,(0,49,-20)))
        add(f'03_bridge_{tag}_{idx}','Giằng nối lõi thép',bridge,'steel',tag,(0,-10 if idx==0 else 10,sign*10),'Thép 40Cr','Hàn/gia công liên kết với hai má lõi trước nhiệt luyện.')

add('03_hinge_upper','Cối bản lề thép trên và gân nối',hinge_upper,'steel','upper',(0,-25,16),'Thép tôi','Gân nối hàn vào giằng trên; truyền lực cơ học qua thép.')
for i,shape in enumerate(hinge_lower): add(f'03_hinge_lower_{i}','Cối bản lề thép dưới',shape,'steel','lower',((-1 if i==0 else 1)*24,-25,-8),'Thép tôi','Hàn vào má lõi dưới trước nhiệt luyện.')
add('03_latch_receiver','Hộp dẫn hướng tai và chốt khóa',receiver,'steel','lower',(0,25,-16),'Thép tôi','Liên kết với giằng dưới; giữ và dẫn hướng tai khóa.')

for upper in [False,True]:
    tag='upper' if upper else 'lower';sign=1 if upper else -1
    liner=half(cylx(20,36,(0,-25,0)).cut(cylx(17,40,(0,-25,0))),upper)
    add('04_grip_liner_'+tag,'Đệm tay ga Ø34 — '+tag,liner,'rubber',tag,(0,-18,sign*18),'EPDM 65–75 Shore A','Lòng Ø34 mm; thay đệm Ø30/32/36. Độ ép thực tế cần đo.',True)
    # Lever pad fills 20x16 opening leaving a 12x8 passage, centered Y=29.
    pad=half(box(36,19.6,15.6,(0,29,0)).cut(box(40,12,8,(0,29,0))),upper)
    add('05_brake_pad_'+tag,'Đệm giữ tay phanh — '+tag,pad,'rubber',tag,(0,18,sign*20),'EPDM','Thay đệm lệch tâm sau khi đo tay phanh; không ép phanh quá hành trình.',True)

pin=cylx(3,49,(0,-53,0))
add('06_hinge_pin','Trục bản lề Ø6',pin,'steel','lower',(-36,-18,0),'Thép không gỉ / thép tôi','Chốt tán kín hai đầu; lõi thép có lỗ đồng trục.')
for x in [-24.5,24.5]:
    add('06_hinge_cap_'+str(x),'Đầu tán trục',cylx(4.3,1.2,(x,-53,0)),'steel','lower',(math.copysign(40,x),-18,0),'Thép')

# Key operated quarter-turn cam. The cylinder is a purchased component envelope.
lock=cylx(7,14,(15,48,-11))
add('07_key_cylinder','Ruột khóa cơ Ø14 × 14',lock,'steel','lower',(36,20,-8),'Cụm ruột khóa mua sẵn','Bao hình mua hàng; chưa thiết kế bi/tumbler bên trong.')
face=cylx(8.5,2,(25,48,-11)).cut(box(5,2.1,8,(25,48,-11)))
add('07_key_face','Mặt ruột khóa và rãnh chìa',face,'steel','lower',(40,20,-8),'Thép không gỉ')
tongue=box(7.5,10,38,(0,48,0)).cut(cylx(3.3,12,(0,48,-11)))
add('08_lock_tongue','Tai khóa thép có lỗ chốt',tongue,'steel','upper',(0,27,28),'Thép tôi, 7,5 × 10 mm','Tai nối với giằng trên; lỗ Ø6.6 là lỗ kín, còn gân hai bên.')
bolt=cylx(3,16,(0,48,-11))
# Cam end located in tongue hole. A cam geometry is indicative, sourced cylinder must be matched.
add('09_cam_bolt','Chốt khóa Ø6 × 16, hành trình 12',bolt,'gold','lower',(16,38,-8),'Thép tôi','Chốt ăn vào má nhận hai bên; ổ khóa nhà cung cấp phải có cơ cấu rút chốt 12 mm thực.',False)

# RF pod, isolated from mechanical core by plastic floor and soft battery carrier.
pod_outer=box(44,80,23,(0,3,38.5),r=5)
pod_inner=box(39,75,21,(0,3,40.5),r=3)
pod=pod_outer.cut(pod_inner)
pod=pod.cut(box(11,8,4.8,(0,41,33.4),r=0)).cut(cylz(2.6,8,(0,5,28)))
bosses=[(-15,-29),(15,-29),(-15,35),(15,35)]
for x,y in bosses:
    boss=cylz(3.5,17,(x,y,37.8)).cut(cylz(1.35,20,(x,y,38)))
    pod=pod.fuse(boss)
add('10_pod_tray','Khay điện tử, gân và trụ vít',pod,'shell','upper',(0,0,30),'PC-ABS chống UV','Tách khỏi đường chịu lực; đế dày 2,5 mm.',True)

# 60×32 custom PCB. Battery on its own deck; room reserved for wires/pack protection.
pcb=box(32,60,1.6,(0,2,30.3),r=1)
for x,y in bosses: pcb=pcb.cut(cylz(1.6,5,(x,y,30.3)))
add('11_main_pcb','PCB đặt riêng 60 × 32 × 1,6',pcb,'pcb','upper',(0,0,48),'FR4 4 lớp','Bao hình PCB; không phải sơ đồ mạch/gerber đã xác nhận.')
module=box(24,24,2.4,(0,-10,32.3),r=.6)
add('12_lte_module','SIM7670G, tùy chọn có GNSS',module,'steel','upper',(0,-18,56),'Module LTE Cat 1bis','Kích thước hãng 24 × 24 × 2,4; phải mua đúng SKU có GNSS.')
add('13_mcu','MCU tiết kiệm điện',box(6,6,1.0,(-9,17,31.6)),'shell','upper',(-12,0,57),'MCU low power','Bao hình linh kiện; chọn STM32L0/L4 hoặc tương đương.')
add('13_accel','Cảm biến gia tốc 3 trục',box(3,3,1,(9,17,31.6)),'gold','upper',(12,0,57),'MEMS','Wake-on-motion; lọc rung do môi trường bằng firmware.')
add('13_hall','Cảm biến Hall trạng thái đóng',box(3,3,1,(-7,42,2.5)),'pcb','upper',(-12,20,15),'Hall low power','Dây đi trong nửa trên, xuyên gioăng lên PCB; không qua bản lề.')
add('13_magnet','Nam châm nhận biết trạng thái',cylz(1.5,2,(-7,42,-2)),'steel','lower',(-12,20,-15),'Nam châm','Hall chỉ xác nhận hai nửa áp sát, không thay thế kiểm tra chốt.')
add('14_sim_holder','Khay nano-SIM',box(12,15,1.5,(0,19,33.2),r=.6),'steel','upper',(0,23,57),'Khay SIM','SIM nằm trong nắp kín, không có khe hở bên hông.')
add('15_battery','Pin Li-Po 1S, bao hình 60 × 30 × 8',box(30,60,8,(0,2,40.4),r=1),'battery','upper',(0,0,74),'Pin Li-Po có bảo vệ + NTC','Khoảng 1.500 mAh là mục tiêu mua hàng; xác nhận datasheet cell. Dành khe nở ≥1 mm.')
add('15_battery_label','Nhãn pin',box(23,42,.15,(0,2,44.48),r=1),'white','upper',(0,0,74),'Nhãn cách điện')
add('16_gnss_ground','Ground plane anten GNSS 24 × 24',box(24,24,.6,(0,-14,45.1),r=.6),'pcb','upper',(0,-24,86),'FR4 phủ đồng','Khay cách điện đỡ riêng phía trên pin; ground plane theo datasheet anten.')
add('16_gnss_patch','Anten GNSS patch 18 × 18 × 4',box(18,18,4,(0,-14,47.4),r=.7),'gold','upper',(0,-24,91),'Gốm / PCB groundplane','Bao hình anten; cần ground plane và đo RF, không có thép che phía trên.')
add('17_lte_antenna','Anten LTE FPC 40 × 10',box(10,40,.25,(-19.2,4,43.8),r=.3),'gold','upper',(-30,0,90),'FPC dán thành nhựa','Bao hình tham khảo; kích thước cuối theo anten và tuning RF.')
add('18_usb_c','Cổng USB-C 5 V',box(9,7,3.2,(0,40,33.4),r=.7),'steel','upper',(0,27,45),'Cổng USB-C','Hai điện trở CC; bộ sạc 1S có NTC, bảo vệ và đường cấp modem.')
add('18_usb_flap','Nút bịt cổng sạc',box(13,2,7,(0,44,33.4),r=1),'rubber','upper',(0,40,46),'Silicone','Gờ ép kín; chỉ sạc khi tháo khỏi xe, nơi khô thoáng.',True)
add('19_cable_grommet','Gioăng lỗ dây cảm biến',cylz(2.5,4,(0,5,27)),'rubber','upper',(0,0,34),'Silicone','Dây tới cảm biến Hall/tamper; bịt kín bằng silicone.')

gasket=box(42,78,1.4,(0,3,50.1),r=4).cut(box(38,74,4,(0,3,50.1),r=2))
add('20_seal','Gioăng chu vi nắp điện tử',gasket,'rubber','upper',(0,0,99),'Silicone','Gioăng hình chữ nhật bo góc; mục tiêu ép 15–25%, cần thử kín.',True)
lid=box(44,80,2.4,(0,3,52),r=5)
for x,y in bosses: lid=lid.cut(cylz(1.6,6,(x,y,52)))
add('21_pod_lid','Nắp anten tháo bằng vít',lid,'orange','upper',(0,0,112),'PC-ABS chống UV','Mục tiêu chống bụi/nước sau thử nghiệm; chưa công bố IP.',True)
for i,(x,y) in enumerate(bosses):
    screw=cylz(1.45,8,(x,y,48.6)).fuse(cylz(2.6,1.5,(x,y,53.35)))
    screw=screw.cut(box(.8,4,1,(x,y,54)))
    add('22_lid_screw_'+str(i),'Vít nắp M3',screw,'steel','upper',(x*.4,y*.3,121),'Thép không gỉ','Ren vào insert đồng lắp nhiệt trong boss, mô hình bao hình ren.')
add('23_status_lens','LED trạng thái và dẫn sáng',box(3,9,.8,(14,12,53.6),r=1),'led','upper',(14,0,115),'PC trong','LED sáng ngắn khi thao tác để giảm điện năng.')
# Branding is real raised CAD geometry, independent of external fonts.
brand=cq.Workplane('XY').text('SAFELOCK',4.1,.24,font='Arial',kind='bold',combine=True).translate((0,-8,53.3)).val()
add('24_brand','Chữ SAFELOCK',brand,'white','upper',(0,0,112),'In pad / khắc laser')
small=cq.Workplane('XY').text('SMART / G9',2.4,.16,font='Arial',combine=True).translate((0,0,53.3)).val()
add('24_brand_small','Chữ SMART / G9',small,'white','upper',(0,0,112),'In pad')

# Vehicle context: a measured example envelope only, not a manufacturer model.
add('ref_handlebar','Ống tay lái tham chiếu',cylx(11,166,(-23,-25,0)),'steel','context',(0,0,0),'Ống Ø22','Chỉ minh họa, không nằm trong BOM khóa.')
grip=cylx(17,108,(-5,-25,0)).cut(cylx(11.5,112,(-5,-25,0)))
for xp in range(-55,48,5):
    ring=cylx(17.5,1.4,(xp,-25,0)).cut(cylx(17,1.7,(xp,-25,0)))
    grip=grip.fuse(ring)
add('ref_throttle','Tay ga mẫu Ø34',grip,'rubber','context',(0,0,0),'Cao su','Vân gờ nằm ngoài vùng kẹp hoặc bị đệm ép; minh họa.')
add('ref_bar_end','Gù tay lái',cylx(19,11,(55,-25,0)),'shell','context',(0,0,0),'Nhôm','Gù Ø38 giúp hạn chế tuột ngang, phải kiểm tra xe thật.')
add('ref_switch','Cụm công tắc tham chiếu',box(26,49,37,(-74,-25,0),r=6),'shell','context',(0,0,0),'Nhựa')
add('ref_master','Cụm phanh tham chiếu',box(37,28,20,(-82,12,10),r=4),'shell','context',(0,0,0),'Nhôm')
# Lever profile in XY, extruded through Z; center passes through opening at Y29.
poly=[(-90,8),(-73,9),(-51,17),(-23,24),(15,25),(40,30),(41,36),(13,33),(-24,32),(-54,25),(-75,18),(-90,18)]
lever=cq.Workplane('XY').polyline(poly).close().extrude(6).translate((0,0,-3)).val()
lever=lever.fuse(cylz(6.0,6,(41,33,0)))
add('ref_brake_lever','Tay phanh ở vị trí đã bóp',lever,'steel','context',(0,0,0),'Nhôm','Tâm rãnh mẫu cách tâm tay ga 54 mm. Đo thực tế trước chọn đệm.')

def hexrgb(c): return tuple(int(c.lstrip('#')[i:i+2],16)/255 for i in (0,2,4))
assembly=cq.Assembly(name='SafeLock_Smart_G9_R01_mm')
scene=trimesh.Scene()
meshdata=[];meta=[]
for p in PARTS:
    verts,tri=p['shape'].tessellate(.15,.15)
    v=np.array([[a.x,a.y,a.z] for a in verts],dtype=np.float64);f=np.array(tri,dtype=np.int32)
    mesh=trimesh.Trimesh(v,f,process=True)
    rgb=[int(255*a) for a in hexrgb(p['color'])]
    mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=rgb+[255])
    if p['group']!='context':
        assembly.add(p['shape'],name=p['id'],color=cq.Color(*hexrgb(p['color'])))
        # GLB uses meters per glTF specification; CAD and STL retain millimeters.
        gm=mesh.copy();gm.apply_scale(.001)
        gm.visual.material=trimesh.visual.material.PBRMaterial(baseColorFactor=rgb+[255],metallicFactor=.45 if p['color']==COLORS['steel'] else .08,roughnessFactor=.45)
        scene.add_geometry(gm,node_name=p['id'],geom_name=p['id'])
        cq.exporters.export(p['shape'],str(ROOT/'STL'/f"{p['id']}.stl"),tolerance=.12,angularTolerance=.15)
    meshdata.append({'id':p['id'],'name':p['name'],'color':p['color'],'group':p['group'],'explode':p['explode'],'v':np.round(v,3).flatten().tolist(),'f':f.flatten().tolist()})
    bb=p['shape'].BoundingBox()
    meta.append({k:p[k] for k in ['id','name','color','group','explode','material','note','printable']} | {'volume_mm3':round(p['shape'].Volume(),3),'valid':p['shape'].isValid(),'bbox_mm':[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],'solids':len(p['shape'].Solids())})
assembly.export(str(ROOT/'CAD'/'SafeLock_G9_R01.step'))
scene.export(str(ROOT/'CAD'/'SafeLock_G9_R01.glb'))
model=[p['shape'] for p in PARTS if p['group']!='context']
cq.exporters.export(cq.Compound.makeCompound(model),str(ROOT/'CAD'/'SafeLock_G9_lap_rap.stl'),tolerance=.15)
(ROOT/'presentation'/'model_data.json').write_text(json.dumps(meshdata,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
(ROOT/'research'/'part_manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'CAD'/'BOM_chi_tiet.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.writer(stream);writer.writerow(['Mã','Tên chi tiết','Nhóm','Vật liệu','In mẫu nhựa được','Ghi chú'])
    for p in PARTS:
        if p['group']!='context':writer.writerow([p['id'],p['name'],p['group'],p['material'],p['printable'],p['note']])

# Report exact interfering solids. Elastomer/branding/fastener functional contacts excluded.
ids={p['id']:p for p in PARTS}
checks=[]
for a,b in [('15_battery','21_pod_lid'),('15_battery','12_lte_module'),('15_battery','11_main_pcb'),('16_gnss_patch','21_pod_lid'),('01_upper_cover','01_lower_cover'),('08_lock_tongue','07_key_cylinder')]:
    vol=ids[a]['shape'].intersect(ids[b]['shape']).Volume()
    checks.append({'a':a,'b':b,'overlap_mm3':round(vol,6)})
result={'revision':'R01','units_cad_stl':'mm','units_glb':'m','parts_total':len(PARTS),'lock_parts':len(model),'all_cad_valid':all(p['valid'] for p in meta),'critical_fit_checks':checks,'note':'Digital concept; dimensional checks are not physical test or manufacturing sign-off.'}
(ROOT/'research'/'cad_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
