/* Shared 3D picking and anchored, non-modal component annotations. No network access. */
window.SafeLockInspector=(()=>{
  const explanations=[
    ['01_', 'Vỏ kẹp', 'Bảo vệ và giữ các chi tiết bên trong. Lõi thép đảm nhận đường truyền lực chính.', 'Cơ khí', 'Thân kẹp rộng 48 mm'],
    ['02_', 'Lõi thép chịu lực', 'Các má thép liên kết với giằng, bản lề và cơ cấu chốt để tạo khung chịu lực.', 'Cơ khí', 'Thép 40Cr · dày 3 mm'],
    ['03_hinge', 'Cối bản lề', 'Liên kết hai nửa khóa với trục bản lề. Gân nối đưa lực về khung thép.', 'Cơ khí', 'Mở bằng tay sau khi rút chốt'],
    ['03_latch', 'Hộp nhận chốt', 'Dẫn hướng tai khóa và đỡ chốt ở hai bên khi hai nửa khép lại.', 'Cơ khí', 'Làm việc cùng tai và chốt khóa'],
    ['03_', 'Giằng nối khung', 'Nối hai má thép, giữ vị trí tương đối và truyền lực giữa các cụm cơ khí.', 'Cơ khí', 'Liên kết cần chốt khi chế tạo'],
    ['04_', 'Đệm ôm tay ga', 'Tạo bề mặt tiếp xúc vừa với tay ga, hạn chế trượt và tiếp xúc cứng lên xe.', 'Tiếp xúc với xe', 'Mẫu Ø34 · có thể thay cỡ đệm'],
    ['05_', 'Đệm giữ tay phanh', 'Đỡ tay phanh ở vị trí đã bóp khi khóa được gắn. Tháo toàn bộ khóa trước khi chạy.', 'Tiếp xúc với xe', 'Rãnh mẫu 12 × 8 mm'],
    ['06_', 'Trục bản lề', 'Là tâm xoay của hai nửa khóa. Hai đầu trục được giữ trong cụm cối thép.', 'Cơ khí', 'Trục Ø6 mm'],
    ['07_', 'Ổ khóa cơ', 'Chìa điều khiển cơ cấu rút chốt. Việc mở cơ khí không phụ thuộc pin.', 'Cơ khí', 'Bao hình · cần chọn ruột khóa thật'],
    ['08_', 'Tai khóa', 'Đi vào hộp nhận khi khép khóa. Lỗ kín trên tai cho chốt thép xuyên qua để giữ hai nửa.', 'Cơ khí', 'Lỗ chốt Ø6,6 mm'],
    ['09_', 'Chốt giữ khóa', 'Xuyên qua tai khóa khi đóng. Cần rút chốt ra trước khi mở bản lề.', 'Cơ khí', 'Ø6 × 16 mm · hành trình rút 12 mm'],
    ['10_', 'Khay điện tử', 'Chứa và bảo vệ cụm điện tử phía trên. Pin và bo mạch tách khỏi khung chịu lực.', 'Điện tử', 'Bố trí riêng với cơ cấu kẹp'],
    ['11_', 'Bo mạch chính', 'Kết nối và quản lý các khối nguồn, cảm biến, định vị và truyền dữ liệu.', 'Điện tử', 'Bao hình PCB 60 × 32 × 1,6 mm'],
    ['12_', 'Bộ định vị & 4G', 'GNSS nhận tọa độ; 4G và SIM truyền dữ liệu về ứng dụng khi có nguồn và sóng.', 'Kết nối', 'SIM7670G · cần đúng tùy chọn GNSS'],
    ['13_mcu', 'Vi điều khiển', 'Chạy chương trình quản lý cảm biến, ngủ/thức và xử lý sự kiện trước khi gửi dữ liệu.', 'Điện tử', 'Chức năng dự kiến · cần firmware'],
    ['13_accel', 'Cảm biến rung', 'Ghi nhận gia tốc và tác động vào thiết bị. Cần lọc rung để hạn chế cảnh báo gây phiền.', 'Cảm biến', 'Không nhận diện danh tính người tác động'],
    ['13_hall', 'Cảm biến trạng thái khép', 'Nhận biết hai nửa áp sát nhờ nam châm đối diện. Không chứng minh chốt đã ăn hoặc khóa đang gắn trên xe.', 'Cảm biến', 'Hall + nam châm'],
    ['13_magnet', 'Nam châm nhận biết', 'Làm việc với cảm biến Hall ở nửa đối diện để nhận biết hai nửa khóa áp sát.', 'Cảm biến', 'Không thay cho cảm biến chốt'],
    ['14_', 'Khay nano-SIM', 'Giữ SIM dùng cho đường truyền 4G. SIM nằm trong khoang có nắp bảo vệ.', 'Kết nối', 'Cần SIM và dịch vụ dữ liệu phù hợp'],
    ['15_', 'Pin độc lập', 'Cấp điện cho định vị, cảm biến và truyền dữ liệu. Khi cạn pin, phần điện tử dừng; chìa cơ vẫn dùng được.', 'Nguồn điện', 'Li-Po 1S · bao hình 60 × 30 × 8 mm'],
    ['16_', 'Anten định vị GNSS', 'Nhận tín hiệu vệ tinh phía dưới nắp nhựa. Bố trí và ground plane cần được đo RF trên mẫu thật.', 'Kết nối', 'Không bảo đảm có fix trong hầm'],
    ['17_', 'Anten 4G', 'Hỗ trợ đường truyền dữ liệu qua mạng di động; bố trí dọc thành nhựa.', 'Kết nối', 'Bao hình FPC · cần tinh chỉnh RF'],
    ['18_usb_c', 'Cổng sạc USB-C', 'Đầu vào sạc pin của khóa. Tháo thiết bị khỏi xe và sạc tại nơi khô thoáng.', 'Nguồn điện', 'Đầu vào dự kiến 5 V'],
    ['18_usb_flap', 'Nút bịt cổng sạc', 'Che miệng cổng USB-C khi không sạc. Độ kín cần được kiểm chứng trên sản phẩm thật.', 'Bảo vệ', 'Silicone · chưa xác nhận cấp IP'],
    ['19_', 'Gioăng lỗ dây', 'Bảo vệ vị trí dây cảm biến đi vào khoang điện tử; giảm khe hở quanh đường dây.', 'Bảo vệ', 'Cần thử kín sau khi lắp'],
    ['20_', 'Gioăng nắp', 'Nằm quanh mép khoang điện tử và được ép khi đóng nắp.', 'Bảo vệ', 'Thiết kế gioăng · chưa chứng nhận IP'],
    ['21_', 'Nắp khoang điện tử', 'Đậy cụm pin, mạch và anten. Nắp nhựa tạo vùng bố trí anten phía trên khung thép.', 'Bảo vệ', 'Tháo bằng vít để bảo trì'],
    ['22_', 'Vít giữ nắp', 'Cố định nắp điện tử vào các trụ. Lực siết và độ ép gioăng cần được chốt khi làm mẫu.', 'Lắp ráp', 'Vít M3 · bao hình ren'],
    ['23_', 'Đèn trạng thái', 'Hiển thị trạng thái thiết bị trong thiết kế. Trạng thái sáng trên mô hình là minh họa.', 'Điện tử', 'Dẫn sáng · cần chương trình điều khiển'],
    ['24_', 'Nhãn nhận diện', 'Tên sản phẩm và dấu nhận diện trên nắp khoang điện tử.', 'Nhận diện', 'SAFELOCK SMART · Nhóm 9'],
    ['ref_', 'Chi tiết xe tham chiếu', 'Mô phỏng vị trí tiếp xúc giữa khóa và tay lái. Cần đo xe thật trước khi chốt tương thích.', 'Xe tham chiếu', 'Không thuộc bộ chi tiết khóa']
  ];
  const visible=o=>{for(let p=o;p;p=p.parent)if(!p.visible)return false;return true};
  function create({container,scene,targets,surfaces,metadata=[],onSelect}){
    const meta=new Map(metadata.map(x=>[x.id,x])),ray=new THREE.Raycaster();
    const root=document.createElement('div');root.className='part-inspector';root.hidden=true;
    root.innerHTML='<svg class="part-leader" aria-hidden="true"><path/><circle r="4"/></svg><section class="part-card" role="dialog" aria-modal="false" aria-label="Chú thích chi tiết"><div class="part-card-top"><span class="part-category"></span><button class="part-close" aria-label="Đóng chú thích" title="Đóng · Esc">×</button></div><h3 class="part-title"></h3><p class="part-description"></p><div class="part-spec"></div><div class="part-detail-name"></div></section>';
    container.appendChild(root);const card=root.querySelector('.part-card'),path=root.querySelector('path'),dot=root.querySelector('circle');
    let selected=null,point=null,surface=null,originalMaterial=null,outline=null,closedByClick=false;
    const getId=o=>o?.userData?.part?.id||o?.userData?.id||o?.name;
    function close(){if(selected){if(selected.material!==originalMaterial&&!Array.isArray(selected.material))selected.material.dispose();selected.material=originalMaterial;if(outline){selected.remove(outline);outline.geometry.dispose();outline.material.dispose()}root.hidden=true;selected=null;outline=null;surface=null;container.classList.remove('has-selection')}return true}
    root.querySelector('.part-close').onclick=()=>{closedByClick=true;close()};
    function select(object,worldPoint,source=surfaces[0]){
      close();if(!object||!visible(object))return false;const id=getId(object),data=meta.get(id)||{};
      const info=explanations.find(x=>id?.startsWith(x[0]))||['',data.name||id,'Chi tiết trong mô hình SafeLock.','Chi tiết','Thiết kế sơ bộ'];
      selected=object;surface=source;scene.updateMatrixWorld(true);
      if(worldPoint)point=object.worldToLocal(worldPoint.clone());else{object.geometry.computeBoundingBox();point=object.geometry.boundingBox.getCenter(new THREE.Vector3())}
      originalMaterial=object.material;
      if(!Array.isArray(originalMaterial)){object.material=originalMaterial.clone();if(object.material.emissive){object.material.emissive.set('#398879').convertSRGBToLinear();object.material.emissiveIntensity=.30}}
      outline=new THREE.LineSegments(new THREE.EdgesGeometry(object.geometry,32),new THREE.LineBasicMaterial({color:0x54baa8,transparent:true,opacity:.9,depthTest:true}));outline.name='__selection_outline';outline.raycast=()=>{};object.add(outline);
      root.querySelector('.part-category').textContent=info[3];root.querySelector('.part-title').textContent=info[1];root.querySelector('.part-description').textContent=info[2];root.querySelector('.part-spec').textContent=info[4];root.querySelector('.part-detail-name').textContent=data.name||object.userData?.part?.name||object.userData?.name||info[1];
      root.hidden=false;container.classList.add('has-selection');closedByClick=false;update();if(onSelect)onSelect(id);return true;
    }
    function hit(event,source){const rect=source.canvas.getBoundingClientRect();if(!rect.width||!rect.height)return null;scene.updateMatrixWorld(true);ray.setFromCamera(new THREE.Vector2((event.clientX-rect.left)/rect.width*2-1,1-(event.clientY-rect.top)/rect.height*2),source.camera);const objects=source.occluders?source.occluders():targets();const first=ray.intersectObjects(objects.filter(o=>o.isMesh&&visible(o)),false)[0];return first&&targets().includes(first.object)?first:null}
    for(const source of surfaces){let down=null,lastHover=0;const canvas=source.canvas;canvas.style.cursor='grab';canvas.tabIndex=0;canvas.setAttribute('aria-label','Mô hình 3D. Kéo để xoay, bấm chi tiết khóa để xem chú thích.');
      canvas.addEventListener('pointerdown',e=>{if(e.button!==0||!e.isPrimary){down=null;return}down={x:e.clientX,y:e.clientY,id:e.pointerId,max:0};});
      canvas.addEventListener('pointermove',e=>{if(down)down.max=Math.max(down.max,Math.hypot(e.clientX-down.x,e.clientY-down.y));if(e.buttons){canvas.style.cursor='grabbing';return}if(performance.now()-lastHover<75)return;lastHover=performance.now();canvas.style.cursor=hit(e,source)?'pointer':'grab';});
      canvas.addEventListener('pointerup',e=>{canvas.style.cursor='grab';if(!down||down.id!==e.pointerId||down.max>7||Math.hypot(e.clientX-down.x,e.clientY-down.y)>7){down=null;return}down=null;const picked=hit(e,source);if(picked)select(picked.object,picked.point,source);else close()});
      canvas.addEventListener('pointercancel',()=>{down=null});
    }
    function update(){if(!selected)return;if(!visible(selected)||document.body.classList.contains('capture')){close();return}const canvasRect=surface.canvas.getBoundingClientRect(),bounds=container.getBoundingClientRect();if(!canvasRect.width||!canvasRect.height){close();return}const p=selected.localToWorld(point.clone()).project(surface.camera);if(!Number.isFinite(p.x)||p.z>1||p.z< -1||Math.abs(p.x)>1.1||Math.abs(p.y)>1.1){root.style.visibility='hidden';return}root.style.visibility='visible';
      const x=(p.x+1)/2*canvasRect.width+canvasRect.left-bounds.left,y=(1-p.y)/2*canvasRect.height+canvasRect.top-bounds.top;
      card.style.width=Math.min(282,bounds.width-32)+'px';const w=card.offsetWidth,h=card.offsetHeight,pad=16,mobile=bounds.width<540;
      let cx=x+28,cy=y-h*.38;if(cx+w>bounds.width-pad)cx=x-w-28;
      if(mobile){cx=Math.max(pad,Math.min(bounds.width-w-pad,cx));cy=y+h+30<bounds.height-160?y+28:y-h-28}
      cx=Math.max(pad,Math.min(bounds.width-w-pad,cx));cy=Math.max(Math.min(114,bounds.height-h-16),Math.min(bounds.height-h-(mobile?130:110),cy));
      card.style.left=cx+'px';card.style.top=cy+'px';let ex=Math.max(cx+12,Math.min(cx+w-12,x)),ey=Math.max(cy+12,Math.min(cy+h-12,y));if(x<cx)ex=cx;else if(x>cx+w)ex=cx+w;else if(y<cy)ey=cy;else ey=cy+h;
      path.setAttribute('d',`M${x},${y} L${(x+ex)/2},${y} L${ex},${ey}`);dot.setAttribute('cx',x);dot.setAttribute('cy',y);
    }
    window.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
    return {close,select,update,state(){return {id:selected?getId(selected):null,open:!!selected&&!root.hidden,source:surfaces.indexOf(surface),rect:selected?card.getBoundingClientRect().toJSON():null}},pick(id){const m=targets().find(o=>getId(o)===id);return select(m,null,surfaces[0])}};
  }
  return {create};
})();
