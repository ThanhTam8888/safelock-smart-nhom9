/* Native 3D geometry. All scene coordinates are meters. Scooter is a reference design. */
const G9WORLD=(()=>{
const host=document.getElementById('scene'), insetHost=document.getElementById('inset');
const scene=new THREE.Scene();scene.background=new THREE.Color('#e8e9e1');scene.fog=new THREE.Fog('#e8e9e1',15,36);
let renderer;try{renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true})}catch(e){document.getElementById('error').style.display='block';throw e}
renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.outputEncoding=THREE.sRGBEncoding;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;host.appendChild(renderer.domElement);
const insetRenderer=new THREE.WebGLRenderer({antialias:true});insetRenderer.setPixelRatio(Math.min(devicePixelRatio,1.5));insetRenderer.outputEncoding=THREE.sRGBEncoding;insetRenderer.toneMapping=THREE.ACESFilmicToneMapping;insetRenderer.toneMappingExposure=1.12;insetHost.insertBefore(insetRenderer.domElement,insetHost.firstChild);
const camera=new THREE.PerspectiveCamera(39,1,.015,70), insetCamera=new THREE.PerspectiveCamera(34,1,.008,45);
const controls=new THREE.OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;controls.minDistance=.25;controls.maxDistance=17;controls.maxPolarAngle=Math.PI*.485;controls.autoRotateSpeed=.55;
const hemi=new THREE.HemisphereLight(0xffffff,0x89977c,1.05);scene.add(hemi);scene.add(new THREE.AmbientLight(0xffffff,.20));
const sun=new THREE.DirectionalLight(0xfff6e3,1.65);sun.position.set(-3,8,4);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-7,right:8,top:6,bottom:-5,near:.5,far:22});sun.shadow.bias=-.00012;sun.shadow.normalBias=.012;scene.add(sun);
const fill=new THREE.DirectionalLight(0xd4e6ee,.7);fill.position.set(5,4,-5);scene.add(fill);
function mat(c,metal=0,rough=.6,extras={}){return new THREE.MeshPhysicalMaterial({color:new THREE.Color(c).convertSRGBToLinear(),metalness:metal,roughness:rough,clearcoat:metal>.1?.25:0,clearcoatRoughness:.28,...extras})}
const M={paint:mat('#4d756c',.28,.31),trim:mat('#d3ddd5',.15,.4),dark:mat('#27393b',.18,.4),rubber:mat('#1b2729',.04,.83),tire:mat('#242d2b',.02,.89),metal:mat('#aebcbd',.68,.29),blackMetal:mat('#3e4a4c',.5,.35),orange:mat('#dd7941',.13,.42),glass:mat('#c4d7cf',.2,.2),red:mat('#a94c3f',.2,.35),skin:mat('#d7a17c',0,.84),hair:mat('#34403c'),hoodie:mat('#c98554',0,.88),pants:mat('#3f5365',0,.9),shoe:mat('#ded8c9',0,.87),visitor:mat('#78858d',0,.88),pavement:mat('#c9cfc3',0,.95),road:mat('#a9b3a9',0,.94),white:mat('#e9eadd',0,.86),tree:mat('#8fa580',0,.96),bark:mat('#9c9078',0,.95)};
const all=[];
function mesh(g,m,name,parent=scene){const a=new THREE.Mesh(g,m);a.name=name;a.castShadow=true;a.receiveShadow=true;parent.add(a);all.push(a);return a}
function rounded(w,h,d,r=.025){r=Math.min(r,w/4,h/4,d/3);const s=new THREE.Shape();const x=-w/2,y=-h/2;s.moveTo(x+r,y);s.lineTo(x+w-r,y);s.quadraticCurveTo(x+w,y,x+w,y+r);s.lineTo(x+w,y+h-r);s.quadraticCurveTo(x+w,y+h,x+w-r,y+h);s.lineTo(x+r,y+h);s.quadraticCurveTo(x,y+h,x,y+h-r);s.lineTo(x,y+r);s.quadraticCurveTo(x,y,x+r,y);const g=new THREE.ExtrudeGeometry(s,{depth:d-2*r,bevelEnabled:true,bevelThickness:r,bevelSize:r*.45,bevelSegments:2,steps:1,curveSegments:5});g.translate(0,0,-d/2+r);g.computeVertexNormals();return g}
function box(name,w,h,d,p,m,parent=scene,r=.02){const a=mesh(r?rounded(w,h,d,r):new THREE.BoxGeometry(w,h,d),m,name,parent);a.position.set(...p);return a}
function ellipsoid(name,r,scale,p,m,parent=scene){const a=mesh(new THREE.SphereGeometry(r,24,14),m,name,parent);a.scale.set(...scale);a.position.set(...p);return a}
function rod(name,a,b,r,m,parent=scene,r2=r){const va=new THREE.Vector3(...a),vb=new THREE.Vector3(...b),dir=vb.clone().sub(va);const o=mesh(new THREE.CylinderGeometry(r2,r,dir.length(),12),m,name,parent);o.position.copy(va.add(vb).multiplyScalar(.5));o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());return o}
function tube(name,points,r,m,parent=scene){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));return mesh(new THREE.TubeGeometry(curve,28,r,8,false),m,name,parent)}
function profile(name,points,depth,m,parent){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(p[0],p[1],0)),true,'catmullrom',.3);const pts=curve.getPoints(96);const s=new THREE.Shape(pts.map(p=>new THREE.Vector2(p.x,p.y)));const g=new THREE.ExtrudeGeometry(s,{depth:depth-.05,bevelEnabled:true,bevelThickness:.025,bevelSize:.025,bevelSegments:5,curveSegments:5});g.translate(0,0,-depth/2+.025);return mesh(SafeLockVisuals.smoothSurface(g),m,name,parent)}
function textTexture(lines,w=512,h=128,bg='#e7eadf',fg='#35524a',size=45){const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d');x.fillStyle=bg;x.fillRect(0,0,w,h);x.fillStyle=fg;x.textAlign='center';x.textBaseline='middle';x.font=`600 ${size}px Arial`;lines.forEach((t,i)=>x.fillText(t,w/2,h/(lines.length+1)*(i+1)));const t=new THREE.CanvasTexture(c);t.encoding=THREE.sRGBEncoding;return t}
function sign(name,words,w,h,p,parent=scene,bg='#e7eadf',fg='#35524a'){const o=mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:textTexture(words,512,128,bg,fg,words.length>1?30:43),side:THREE.DoubleSide}),name,parent);o.position.set(...p);o.castShadow=false;return o}

const environment=new THREE.Group();environment.name='Boi_canh_khu_do_xe';scene.add(environment);
box('Nen_quang_truong',35,.07,30,[0,-.055,0],mat('#d8ddce',0,1),environment,0);
box('Khu_do_xe',11,.045,4.7,[.6,-.012,-.3],M.road,environment,.05);
box('Via_he',13,.1,2.1,[.2,.012,3.0],M.pavement,environment,.04);
for(let i=-6;i<7;i++)box('Gach_via_he_'+i,.012,.004,2,[i,.067,3],mat('#b8c1b5',0,1),environment,0);
for(let i=-6;i<7;i++)box('Bo_via_'+i,.95,.15,.16,[i,.04,1.88],i%2?M.white:mat('#adbaab'),environment,.025);
for(let x of [-2.5,-.5,1.5]){box('Vach_do_xe',.045,.005,2.2,[x,.015,.05],M.white,environment,0)}
box('Vach_cuoi_o_do',4.06,.006,.04,[-.5,.017,-1.05],M.white,environment,0);
for(let x=-6;x<7;x+=1.3)box('Vach_duong',.62,.005,.055,[x,.015,-2.2],M.white,environment,0);
const parkingSign=new THREE.Group();parkingSign.position.set(-2.45,0,-.98);environment.add(parkingSign);rod('Cot_bien', [0,0,0],[0,1.9,0],.028,M.blackMetal,parkingSign);box('Bang_do',.44,.5,.05,[0,1.7,0],mat('#496b65'),parkingSign,.035);sign('Chu_P',['P'],.30,.32,[0,1.71,.028],parkingSign,'#496b65','#f3f2e5');
for(let [x,z] of [[-3.6,-2.9],[4.8,-3.2]]){box('Bon_cay',.9,.31,.8,[x,.15,z],mat('#bbc7b4'),environment,.08);rod('Than_cay',[x,.28,z],[x,2.5,z],.085,M.bark,environment,.05);ellipsoid('Tan_cay',.7,[1.05,1.1,.95],[x,2.65,z],M.tree,environment);ellipsoid('Tan_cay_nho',.52,[1,.9,1],[x+.5,2.4,z+.14],mat('#9eae89'),environment)}
box('Ghe_ngoi',1.2,.12,.37,[-2.7,.45,2.8],mat('#9b9c7e'),environment,.04);for(let x of [-3.1,-2.3])box('Chan_ghe',.08,.43,.30,[x,.23,2.8],M.blackMetal,environment,.01);
// Low background storefront: context without external textures or brand assets.
box('Khoi_nha_nen',7,2.7,.35,[1,1.35,-4.1],mat('#d7d8c9'),environment,.04);
box('Cua_hang',2.8,1.8,.05,[1.9,.95,-3.9],mat('#8caba0',.15,.35),environment,.015);
for(let x of [.55,1.9,3.25])box('Khung_kinh',.045,1.9,.08,[x,.96,-3.85],mat('#b9c8b8'),environment,.005);
box('Mai_hien',3.5,.13,.85,[1.9,2.03,-3.6],mat('#adb99a'),environment,.035);sign('Ten_quan',['GÓC PHỐ  /  CAFÉ'],3.0,.37,[1.9,2.45,-3.88],environment,'#d7d8c9','#4e6a5b');
const canopy=new THREE.Group();canopy.name='Khu_co_mai_che_tuong_trung_ham';scene.add(canopy);for(let x of [-1.6,1.6])for(let z of [-1.0,1.0])box('Cot_ham',.15,2.7,.15,[x,1.35,z],mat('#aebdb0'),canopy,.015);box('Mai_che_tuong_trung',3.5,.12,2.6,[0,2.72,0],mat('#9eafa4',0,.9,{transparent:true,opacity:.35}),canopy,.02);canopy.visible=false;

const vehicle=new THREE.Group();vehicle.name='Xe_tay_ga_tham_chieu';scene.add(vehicle);
const wheelGroups=[];
function wheel(x,front){const g=new THREE.Group();g.name=front?'Banh_truoc':'Banh_sau';g.position.set(x,.275,0);vehicle.add(g);wheelGroups.push(g);mesh(new THREE.TorusGeometry(.216,.059,14,48),M.tire,'Lop_xe',g);const rim=mesh(new THREE.CylinderGeometry(.179,.179,.085,32),M.blackMetal,'Vanh_xe',g);rim.rotation.x=Math.PI/2;const hub=mesh(new THREE.CylinderGeometry(.045,.045,.14,20),M.metal,'Truc_banh',g);hub.rotation.x=Math.PI/2;for(let j=0;j<8;j++){let a=j*Math.PI/4;rod('Nan_hoa',[Math.cos(a)*.04,Math.sin(a)*.04,.051],[Math.cos(a+.15)*.168,Math.sin(a+.15)*.168,.051],.008,M.metal,g)}mesh(new THREE.TorusGeometry(.169,.006,7,40),M.metal,'Vien_vanh',g).position.z=.053;const disk=mesh(new THREE.CylinderGeometry(.116,.116,.008,28),M.metal,'Dia_phanh',g);disk.rotation.x=Math.PI/2;disk.position.z=.077;for(let j=0;j<10;j++){let a=j*Math.PI/5;const h=mesh(new THREE.CylinderGeometry(.008,.008,.01,8),M.dark,'Lo_dia_phanh',g);h.rotation.x=Math.PI/2;h.position.set(.089*Math.cos(a),.089*Math.sin(a),.084)}box('Heo_phanh',.055,.095,.04,[.08,.05,.10],M.orange,g,.015);return g}
wheel(-.69,false);wheel(.73,true);
// Chassis, engine, swingarm, exhaust, center stand and front suspension.
rod('Khung_chinh',[-.72,.39,0],[.45,.43,0],.045,M.blackMetal,vehicle);rod('Khung_len_dau',[.37,.41,0],[.50,1.08,0],.035,M.blackMetal,vehicle);
box('Khoi_dong_co',.50,.22,.26,[-.62,.37,0],M.blackMetal,vehicle,.06);ellipsoid('Nap_truyen_dong',.2,[1.65,.53,.72],[-.62,.40,.115],M.dark,vehicle);
for(let z of [-.10,.10]){rod('Cang_sau',[-.34,.46,z],[-.69,.275,z],.027,M.blackMetal,vehicle);rod('Phuoc_truoc',[.51,1.02,z],[.73,.275,z],.021,M.metal,vehicle);rod('Vo_phuoc_truoc',[.62,.66,z],[.73,.275,z],.030,M.dark,vehicle)}
rod('Ong_xa',[-.3,.34,-.22],[-.91,.35,-.22],.057,M.blackMetal,vehicle);box('Tam_chan_nhiet',.43,.09,.025,[-.65,.38,-.278],M.metal,vehicle,.025);
rod('Chan_chong',[0,.31,.05],[-.14,.045,.24],.014,M.blackMetal,vehicle);box('De_chan_chong',.15,.025,.09,[-.14,.04,.24],M.dark,vehicle,.008);
profile('Vo_duoi_xe',[[-1,.54],[-.85,.68],[-.58,.74],[-.20,.73],[.12,.64],[.16,.47],[-.30,.38],[-.72,.42]],.47,M.paint,vehicle);
profile('Op_duoi_phu',[[-.92,.56],[-.72,.68],[-.30,.68],[-.05,.57],[-.18,.45],[-.70,.43]],.487,mat('#78968a',.25,.38),vehicle);
box('San_de_chan',.72,.075,.43,[.18,.30,0],M.dark,vehicle,.045);for(let z of [-.145,-.075,0,.075,.145])box('Goi_chong_truot_san',.42,.007,.014,[.16,.344,z],M.blackMetal,vehicle,.003);
profile('Yem_truoc',[[.30,.35],[.33,.56],[.40,.83],[.47,1.08],[.63,1.13],[.76,1.01],[.77,.81],[.69,.52],[.59,.34]],.40,M.paint,vehicle);
profile('Tam_op_trong',[[.30,.37],[.34,.60],[.41,.88],[.47,1.04],[.52,1.00],[.46,.73],[.41,.45]],.32,M.dark,vehicle);
profile('Nap_truoc_mau_sang',[[.63,.47],[.70,.66],[.75,.91],[.69,1.04],[.65,1.01],[.66,.75],[.59,.53]],.20,M.trim,vehicle);
box('Yen_xe',.92,.14,.43,[-.42,.77,0],M.rubber,vehicle,.065);box('Duong_may_yen',.77,.007,.39,[-.42,.847,0],mat('#55615a'),vehicle,.03);
tube('Tay_nam_sau',[[-.95,.70,-.24],[-1.02,.74,-.17],[-1.04,.75,0],[-1.02,.74,.17],[-.95,.70,.24]],.016,M.metal,vehicle);
const taillight=ellipsoid('Den_hau',.12,[.38,.5,1.45],[-.968,.69,0],M.red,vehicle);
box('Gia_bien_so',.025,.17,.19,[-1.01,.47,0],M.dark,vehicle,.015);const plate=sign('Bien_so_minh_hoa',['G9','SAFELOCK'],.21,.15,[-1.03,.47,0],vehicle,'#e5e9df','#405e55');plate.rotation.y=-Math.PI/2;
let mud=mesh(new THREE.TorusGeometry(.302,.041,9,38,Math.PI),M.paint,'Chan_bun_truoc',vehicle);mud.position.set(.73,.275,0);mud.scale.z=1.55;
// Steering and controls. CAD reference supplies the right grip, master cylinder and lever.
rod('Truc_lai',[.50,1.0,0],[.45,1.19,0],.025,M.blackMetal,vehicle);rod('Tay_lai',[.45,1.19,-.39],[.45,1.19,.25],.011,M.metal,vehicle);
rod('Tay_nam_trai',[.45,1.19,-.39],[.45,1.19,-.27],.017,M.rubber,vehicle);box('Cum_cong_tac_trai',.052,.047,.047,[.45,1.19,-.24],M.dark,vehicle,.012);
box('Cum_dong_ho',.18,.078,.24,[.48,1.18,0],M.dark,vehicle,.035);const speedo=box('Mat_dong_ho',.12,.008,.17,[.46,1.225,0],mat('#829d95',.08,.2),vehicle,.02);
ellipsoid('Den_pha',.1,[.62,.62,1.5],[.718,1.065,0],mat('#edf0d8',.1,.25,{emissive:new THREE.Color('#c4c5a2'),emissiveIntensity:.18}),vehicle);
for(let z of [-.18,.18]){ellipsoid('Den_xi_nhan',.038,[.8,.5,1],[.72,1.03,z],mat('#e1b377',.15,.3),vehicle);tube('Can_guong',[[.45,1.2,z],[.48,1.36,z*1.45],[.54,1.45,z*1.9]],.008,M.blackMetal,vehicle);ellipsoid('Guong_chieu_hau',.1,[.22,.55,1],[.54,1.46,z*1.9],M.dark,vehicle);ellipsoid('Mat_guong',.085,[.10,.47,1],[.523,1.46,z*1.9],M.glass,vehicle)}
tube('Day_phanh_truoc',[[.50,1.17,.24],[.52,.98,.18],[.63,.66,.13],[.73,.34,.13]],.004,M.rubber,vehicle);
// Exact R01 lock mesh, original CAD in millimeters, cyclic axis permutation to vehicle axes.
const lockRoot=new THREE.Group(),contextRoot=new THREE.Group();lockRoot.name='SafeLock_G9_R01_50_chi_tiet';contextRoot.name='Tay_nam_phai_tham_chieu_CAD';vehicle.add(lockRoot,contextRoot);
const basis=new THREE.Matrix4().set(0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1);const q=new THREE.Quaternion().setFromRotationMatrix(basis);
for(let g of [lockRoot,contextRoot]){g.quaternion.copy(q);g.scale.setScalar(.001);g.position.set(.475,1.19,.34)}
const lockMeshes=[];
for(const p of LOCK_DATA){const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p.v,3));g.setIndex(p.f);g.computeVertexNormals();const m=mat(p.color,p.color==='#a4b2bc'||p.color==='#d5ac58'?.45:.04,.5);const o=mesh(g,m,p.id,p.group==='context'?contextRoot:lockRoot);o.userData={part:p};if(p.group!=='context')lockMeshes.push(o)}
const sensorLED=lockMeshes.find(m=>m.name==='23_status_lens');
SafeLockVisuals.setupWorld(renderer,scene,M,lockMeshes);
// Ignition assembly, two different key models, and phone left on the seat in a limit case.
const ignition=new THREE.Group();ignition.position.set(.395,.88,.14);ignition.rotation.z=-.20;vehicle.add(ignition);const socket=mesh(new THREE.CylinderGeometry(.027,.027,.018,24),M.metal,'O_chia_xe',ignition);socket.rotation.x=Math.PI/2;box('Ranh_chia_xe',.014,.003,.004,[0,0,.011],M.dark,ignition,.001);
function keyModel(name,parent){const g=new THREE.Group();g.name=name;parent.add(g);const gold=mat('#d7b46c',.55,.32);box('Than_chia',.011,.04,.004,[0,.014,0],gold,g,.002);box('Dau_chia',.030,.025,.008,[0,.045,0],M.dark,g,.007);mesh(new THREE.TorusGeometry(.022,.003,7,20),gold,'Vong_chia',g).position.y=.077;return g}
const ignitionKey=keyModel('Chia_khoa_xe_de_quen',vehicle);ignitionKey.position.set(.395,.88,.16);ignitionKey.rotation.x=Math.PI/2;
const lockKey=keyModel('Chia_khoa_co_SafeLock',vehicle);lockKey.position.set(.523,1.178,.368);lockKey.rotation.x=Math.PI/2;
const leftPhone=new THREE.Group();vehicle.add(leftPhone);leftPhone.position.set(-.40,.865,.0);leftPhone.rotation.x=-Math.PI/2;box('Dien_thoai_de_quen',.072,.147,.009,[0,0,0],M.dark,leftPhone,.01);box('Man_hinh_dien_thoai',.061,.122,.002,[0,0,.006],mat('#789a8c',0,.3),leftPhone,.005);leftPhone.visible=false;
// Rigged stylized figures. Articulated legs/arms move deterministically with the timeline.
function person(name,coat){return SafeLockVisuals.createPerson({name,scene,materials:M,mesh})}
const owner=person('Chu_xe',M.hoodie),visitor=person('Nguoi_tac_dong',M.visitor),helper=person('Nguoi_ho_tro_di_chuyen',M.visitor);helper.root.visible=false;visitor.phone.visible=false;helper.phone.visible=false;
// Utility truck. No model of bypass methods or disassembly is shown.
const truck=new THREE.Group();truck.name='Phuong_tien_van_chuyen_minh_hoa';truck.position.set(3.5,0,-1.8);scene.add(truck);
box('San_cho_hang',2.7,.15,1.55,[-.45,.73,0],mat('#889c98',.4,.5),truck,.035);box('Sat_xi',3.8,.18,1.35,[0,.48,0],M.blackMetal,truck,.025);box('Cabin',1.05,1.25,1.48,[1.35,1.12,0],mat('#e2dcc7',.15,.5),truck,.16);box('Kinh_cabin',.03,.50,1.16,[1.90,1.35,0],mat('#7faaa2',.12,.25),truck,.03);box('Kinh_hong',.58,.45,.02,[1.37,1.40,.754],mat('#8bb0a6',.15,.3),truck,.035);
for(let x of [-1.25,1.2])for(let z of [-.68,.68]){const w=mesh(new THREE.TorusGeometry(.23,.07,10,24),M.tire,'Lop_xe_tai',truck);w.position.set(x,.30,z);const h=mesh(new THREE.CylinderGeometry(.13,.13,.1,18),M.metal,'Vanh_xe_tai',truck);h.rotation.x=Math.PI/2;h.position.copy(w.position)}truck.visible=false;
// Visual rings are event markers, not a claim of acoustic output for R01.
const rings=new THREE.Group();rings.name='Vong_hien_thi_su_kien';scene.add(rings);for(let i=0;i<3;i++){const r=mesh(new THREE.TorusGeometry(.44,.006,6,64),new THREE.MeshBasicMaterial({color:0xd37842,transparent:true,opacity:.5}),`Vong_${i}`,rings);r.rotation.x=-Math.PI/2;r.position.y=.025+i*.003}
const pathLine=mesh(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,.025,0),new THREE.Vector3(0,.025,0)]),new THREE.MeshBasicMaterial({color:0xd58a54}), 'Duong_di_minh_hoa',scene);pathLine.visible=false;
const keyHalo=mesh(new THREE.TorusGeometry(.085,.004,6,48),new THREE.MeshBasicMaterial({color:0xe5953f,transparent:true,opacity:.7}), 'Danh_dau_chia',vehicle);keyHalo.visible=false;
let focus='lock',closeup=false,viewFit=1;
function home(){closeup=false;controls.target.set(.80,.78,.12);camera.position.set(3.7,3.0,6.45);camera.position.sub(controls.target).multiplyScalar(viewFit).add(controls.target);controls.update()}
function zoomLock(){closeup=true;const p=vehicle.localToWorld(new THREE.Vector3(.475,1.2,.34));controls.target.copy(p);camera.position.copy(p).add(new THREE.Vector3(.35,.21,.42));controls.update()}
function resize(){const w=host.clientWidth,h=host.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();const previous=viewFit;viewFit=Math.max(1,Math.min(2,.9/camera.aspect));if(!closeup&&camera.position.lengthSq()>0)camera.position.sub(controls.target).multiplyScalar(viewFit/previous).add(controls.target);controls.update();const iw=insetHost.clientWidth,ih=insetHost.clientHeight;if(iw>0&&ih>0){insetRenderer.setSize(iw,ih,false);insetCamera.aspect=iw/ih;insetCamera.updateProjectionMatrix()}}
function draw(t=0){controls.update();scene.updateMatrixWorld(true);renderer.render(scene,camera);if(insetHost.clientWidth>0){let target;if(focus==='ignition')target=vehicle.localToWorld(new THREE.Vector3(.395,.91,.16));else if(focus==='lockkey')target=vehicle.localToWorld(new THREE.Vector3(.522,1.19,.37));else if(focus==='phone')target=vehicle.localToWorld(new THREE.Vector3(-.40,.87,0));else target=lockRoot.localToWorld(new THREE.Vector3(0,0,22));insetCamera.position.copy(target).add(new THREE.Vector3(.21,.15,.26));insetCamera.lookAt(target);insetRenderer.render(scene,insetCamera);}const p=lockRoot.localToWorld(new THREE.Vector3(0,0,54));p.project(camera);const el=document.getElementById('lock-pin');el.style.left=((p.x+1)/2*host.clientWidth+9)+'px';el.style.top=((-p.y+1)/2*host.clientHeight-7)+'px';el.style.display=p.z<1&&p.x>-1&&p.x<1&&p.y>-1&&p.y<1?'flex':'none'}
function lockPose(open=0){for(let m of lockMeshes){const p=m.userData.part;m.rotation.set(0,0,0);m.position.set(0,0,0);if(p.group==='upper'){const a=open*Math.PI*75/180;m.rotation.x=a;m.position.set(0,-53+53*Math.cos(a),53*Math.sin(a))}if(p.id==='09_cam_bolt'&&open>0)m.position.x=12}}
function exportGeometry(){const groups=[vehicle,owner.root];scene.updateMatrixWorld(true);const list=[];for(let group of groups)group.traverse(o=>{if(!o.isMesh||!o.visible)return;let ancestor=o.parent;while(ancestor&&ancestor!==scene){if(!ancestor.visible)return;ancestor=ancestor.parent}const g=o.geometry.clone();g.applyMatrix4(o.matrixWorld);const color=o.material.color?o.material.color.clone().convertLinearToSRGB().getHexString():'b5bdad';list.push({name:o.name,v:Array.from(g.attributes.position.array),f:g.index?Array.from(g.index.array):null,color:'#'+color});g.dispose()});return list}
window.addEventListener('resize',resize);resize();home();owner.root.position.set(.05,0,.95);owner.root.rotation.y=Math.PI;visitor.root.visible=false;
return {scene,renderer,insetRenderer,camera,insetCamera,controls,vehicle,lockRoot,contextRoot,lockMeshes,owner,visitor,helper,truck,canopy,rings,keyHalo,ignitionKey,lockKey,leftPhone,wheelGroups,sensorLED,home,zoomLock,draw,resize,lockPose,exportGeometry,setFocus(f){focus=f;document.getElementById('inset-label').textContent=f==='ignition'?'CẬN CẢNH / CHÌA XE':f==='lockkey'?'CẬN CẢNH / CHÌA SAFELOCK':f==='phone'?'CẬN CẢNH / ĐIỆN THOẠI ĐỂ LẠI':'CẬN CẢNH / SAFELOCK ĐÚNG TỶ LỆ'},setCloseup(v){closeup=v},isCloseup(){return closeup},meshCount:all.length};
})();
