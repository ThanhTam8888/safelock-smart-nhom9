/* Deterministic film choreography shared by the render pipeline and visual tests. */
window.G9FILM=(()=>{
 const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>{x=clamp(x);return x*x*(3-2*x)},phase=(t,a,b)=>ease((t-a)/(b-a)),mix=(a,b,v)=>a+(b-a)*v;
 let output=null;const vec=(...v)=>new THREE.Vector3(...v);
 function camera(W,position,target){W.controls.autoRotate=false;W.camera.position.set(...position);W.controls.target.set(...target);W.camera.lookAt(W.controls.target);}
 function parts(W){return new Map(W.lockMeshes.map(m=>[m.userData.part.id,m]))}
 function setMechanism(W,open,withdraw){for(const m of W.lockMeshes){const p=m.userData.part;m.rotation.set(0,0,0);m.position.set(0,0,0);if(p.group==='upper'){const a=open*Math.PI*75/180;m.rotation.x=a;m.position.set(0,-53+53*Math.cos(a),53*Math.sin(a))}if(p.id==='09_cam_bolt')m.position.x=withdraw*12;}
  return {hingeDegrees:open*75,boltStroke:withdraw*12};
 }
 function hands(W,amount=1){W.scene.updateMatrixWorld(true);const left=W.lockRoot.localToWorld(vec(-19,-5,-16)),top=W.lockMeshes.find(o=>o.userData.part.id==='01_upper_cover'),right=top.localToWorld(vec(23,17,15));W.owner.reachTo(0,left,amount);W.owner.reachTo(1,right,amount);return {left,right}}
 function keyAt(W,insert,turn=0){W.lockKey.visible=insert>0;if(!W.lockKey.visible)return;W.lockKey.position.copy(W.lockRoot.localToWorld(vec(26,48,-11))).add(vec(0,0,(1-insert)*.05));W.lockKey.quaternion.setFromAxisAngle(vec(0,0,1),turn*Math.PI/2).multiply(new THREE.Quaternion().setFromAxisAngle(vec(1,0,0),Math.PI/2));}
 function operation(t){const W=G9SIM.world;G9SIM.setCase('park');G9SIM.seek(.5);W.owner.root.position.set(.48,0,.76);W.owner.root.rotation.y=Math.PI;W.owner.phone.visible=false;W.owner.pose(0,0,.35);W.ignitionKey.position.set(.395,.88,.16);W.ignitionKey.visible=t<32;W.keyHalo.visible=false;W.rings.visible=false;for(const o of W.contextRoot.children){o.position.set(0,0,0);o.rotation.set(0,0,0)}
  const base=vec(.475,1.19,.34),held=vec(.38,1.10,.62);let open=0,withdraw=0,hold=0,keyInsert=0,turn=0;
  if(t<7){W.lockRoot.position.copy(held);open=0;hold=phase(t,3,5);camera(W,[2.6,1.82,3.3],[.45,.96,.2]);}
  else if(t<14){W.lockRoot.position.copy(held);withdraw=phase(t,8,9.5);open=phase(t,10,13);hold=1;keyInsert=phase(t,7,8);turn=withdraw;camera(W,[.80,1.36,.25],[.40,1.13,.64]);}
  else if(t<21){W.lockRoot.position.lerpVectors(held,base,phase(t,14,20));open=1;withdraw=1;hold=1;keyInsert=1;turn=1;camera(W,[.84,1.44,.05],[.49,1.23,.37]);}
  else if(t<28){W.lockRoot.position.copy(base);open=1-phase(t,21,24.5);withdraw=1-phase(t,25.0,26.8);hold=1;keyInsert=1;turn=withdraw;camera(W,[.83,1.40,.07],[.49,1.20,.36]);}
  else if(t<35){W.lockRoot.position.copy(base);hold=1-phase(t,33,35);keyInsert=1-phase(t,29,31);camera(W,[.84,1.41,.07],[.48,1.19,.36]);}
  else if(t<42){W.lockRoot.position.copy(base);const v=phase(t,35,41);W.owner.root.position.set(mix(.48,2.75,v),0,mix(.76,1.05,v));W.owner.root.rotation.y=Math.PI/2;W.owner.pose(v>0&&v<1?1:0,v*16,0);W.owner.phone.visible=t>38;camera(W,[3.65,2.12,4.9],[.95,.90,.13]);}
  else if(t<49){const v=phase(t,42,44);W.owner.root.position.set(mix(2.75,.48,v),0,mix(1.05,.76,v));W.owner.root.rotation.y=v>.98?Math.PI:-Math.PI/2;W.owner.pose(v>0&&v<1?1:0,v*16,.3);W.lockRoot.position.copy(base);hold=phase(t,43.7,44.3);keyInsert=phase(t,44,44.8);withdraw=phase(t,45,46);turn=withdraw;open=phase(t,46.7,48.6);camera(W,[.83,1.40,.07],[.48,1.20,.36]);}
  else{W.lockRoot.position.lerpVectors(base,vec(.33,1.08,.67),phase(t,49,52));open=1;withdraw=1;hold=1-phase(t,54,56);keyInsert=1;turn=1;camera(W,[.84,1.41,.07],[.48,1.18,.37]);}
  const mechanism=setMechanism(W,open,withdraw);keyAt(W,keyInsert,turn);if(hold>0)hands(W,hold);
  if(t>=7&&t<10||t>=25&&t<31||t>=44&&t<46.5)W.owner.reachTo(1,W.lockKey.localToWorld(vec(0,.075,0)),Math.min(1,hold));
  const lever=W.contextRoot.children.find(m=>m.userData.part?.id==='ref_brake_lever');const release=phase(t,52,55);if(lever){const a=release*.14,c=Math.cos(a),s=Math.sin(a);lever.rotation.z=a;lever.position.set(-90-(-90*c-13*s),13-(-90*s+13*c),0)}
  W.draw(t);return {...mechanism,anchorMap:{lock:W.lockRoot.localToWorld(vec(0,0,25)),bolt:W.lockRoot.localToWorld(vec(0,48,-11)),liner:W.lockRoot.localToWorld(vec(0,-25,0)),key:W.lockRoot.localToWorld(vec(26,48,-11)),brake:W.vehicle.localToWorld(vec(.51,1.19,.34))}};
 }
 function forgotten(t){const W=G9SIM.world;W.ignitionKey.position.set(.395,.88,.16);for(const o of W.contextRoot.children){o.position.set(0,0,0);o.rotation.set(0,0,0)}G9SIM.setCase('ignition_key');let p;if(t<6)p=mix(0,.22,phase(t,0,6));else if(t<12)p=mix(.22,.60,phase(t,6,12));else if(t<24)p=.70;else if(t<30)p=mix(.82,.96,phase(t,24,30));else p=mix(.96,1,phase(t,30,33));G9SIM.setTier(t>=18&&t<24?'r01':'r02');G9SIM.seek(p);
  W.owner.pose(p>.22&&p<.63||p>.82&&p<.96?1:0,p*18,0);if(t>=30){W.owner.root.position.set(.48,0,.76);W.owner.root.rotation.y=Math.PI;W.owner.phone.visible=false;W.owner.reachTo(1,W.vehicle.localToWorld(vec(.395,.90,.17)),1-phase(t,33,35));}
  W.ignitionKey.visible=t<34.5;if(t>=32){W.scene.updateMatrixWorld(true);const hand=W.vehicle.worldToLocal(W.owner.hands[1].getWorldPosition(vec()));W.ignitionKey.position.lerpVectors(vec(.395,.88,.16),hand,phase(t,32,34));}if(t<6)camera(W,[1.12,1.26,.55],[.40,.92,.18]);else if(t<24)camera(W,[3.6,2.13,5.2],[1.0,.90,.14]);else if(t<30)camera(W,[3.4,1.95,4.5],[.9,.9,.10]);else camera(W,[1.12,1.26,.55],[.40,.94,.19]);W.draw(t);
  return {anchorMap:{ignition:W.vehicle.localToWorld(vec(.395,.91,.18)),lock:W.lockRoot.localToWorld(vec(0,0,25)),phone:W.owner.phone.getWorldPosition(vec()),key:W.vehicle.localToWorld(vec(.395,.92,.18))}};
 }
 function scenarios(t){const W=G9SIM.world;W.ignitionKey.position.set(.395,.88,.16);const i=Math.min(13,Math.floor(t/6)),id=G9SIM.cases[i].id,p=clamp((t-i*6)/6);G9SIM.setCase(id);G9SIM.setTier('r02');G9SIM.seek(p);W.owner.pose(G9SIM.state().ownerAway>.01&&G9SIM.state().ownerAway<.99?1:0,G9SIM.state().ownerAway*18,0);
  if(id==='park'&&p<.5){W.owner.root.position.set(.48,0,.76);W.owner.root.rotation.y=Math.PI;W.owner.phone.visible=false;hands(W,1)}
  camera(W,id==='lift'?[5.1,2.9,7.3]:[3.6,2.24,5.4],id==='lift'?[1.35,.95,-.6]:[.9,.92,.13]);W.draw(t);return {anchorMap:{lock:W.lockRoot.localToWorld(vec(0,0,28))}};
 }
 function mechanism(t){const W=G9;let m='product',open=0,explode=0;if(t>=4&&t<8){m='exploded';explode=mix(.15,.70,phase(t,4,7.7))}else if(t>=8&&t<16){m='open';open=t<12?phase(t,8,11.5)*.20:.20+phase(t,12,15.8)*.80}else if(t>=16&&t<24)m='inside';
  W.capture({m,open,explode,clean:true,distance:m==='exploded'?430:m==='open'?350:270,targetY:m==='exploded'?58:m==='open'?38:14,az:.68+Math.min(1,t/28)*.12,elev:.44});
  if(t>=8&&t<12){for(const o of W.meshes)if(/^(01_|04_|05_|10_|21_)/.test(o.userData.id))o.visible=false;camera(W,[87,17,-95],[0,-5,-43]);}
  W.scene.updateMatrixWorld(true);W.renderer.render(W.scene,W.camera);const ids={lock:'21_pod_lid',core:'02_core_upper_R',bolt:'09_cam_bolt',hinge:'06_hinge_pin',battery:'15_battery',antenna:'16_gnss_patch'};const anchors={};for(const [key,id] of Object.entries(ids)){const mesh=W.meshes.find(o=>o.userData.id===id);mesh.geometry.computeBoundingBox();anchors[key]=mesh.localToWorld(mesh.geometry.boundingBox.getCenter(vec()))}return {anchorMap:anchors};
 }
 function frame(id,time,{jpeg=true,width=1920,height=1080,title='',caption=''}={}){const isProduct=id==='mechanism',W=isProduct?G9:G9SIM.world;if(isProduct)G9.freezeRendering=true;else G9SIM.freezeRendering=true;document.body.classList.add('capture');document.body.classList.remove('story');const result=isProduct?mechanism(time):id==='operation'?operation(time):id==='forgotten'?forgotten(time):scenarios(time);
  const r=W.renderer;if(r.domElement.width!==width||r.domElement.height!==height){r.setPixelRatio(1);r.setSize(width,height,false);W.camera.aspect=width/height;W.camera.updateProjectionMatrix();r.render(W.scene,W.camera)}
  const anchors={};for(const [key,p] of Object.entries(result.anchorMap)){const v=p.clone().project(W.camera);anchors[key]={x:(v.x+1)/2,y:(1-v.y)/2}}
  if(!output){output=document.createElement('canvas')}output.width=width;output.height=height;const c=output.getContext('2d');c.fillStyle=isProduct?'#e8eeeb':'#e6e9e9';c.fillRect(0,0,width,height);c.drawImage(r.domElement,0,0,width,height);
  c.fillStyle='rgba(17,35,31,.78)';c.fillRect(0,height-91,width,91);c.fillStyle='#eef6f1';c.font='600 27px Segoe UI';c.fillText(title,44,height-48);c.font='17px Segoe UI';c.fillStyle='#c7d8ce';c.fillText(caption,44,height-19);c.fillStyle='rgba(245,250,247,.90)';c.fillRect(width-345,23,319,31);c.fillStyle='#536e62';c.font='13px Segoe UI';c.fillText('SAFELOCK / MÔ PHỎNG 3D THAM CHIẾU',width-332,44);
  return {jpeg:jpeg?output.toDataURL('image/jpeg',.94):null,anchors,mechanism:result.hingeDegrees!==undefined?{angle:result.hingeDegrees,stroke:result.boltStroke}:null};
 }
 return {frame};
})();
