(()=>{
  const W=G9SIM.world,$=id=>document.getElementById(id);let lastFocus=null;
  const meshOccluders=()=>{const objects=[];W.scene.traverse(o=>{if(o.isMesh)objects.push(o)});return objects};
  const inspector=SafeLockInspector.create({container:document.querySelector('.middle'),scene:W.scene,targets:()=>W.lockMeshes,surfaces:[{canvas:W.renderer.domElement,camera:W.camera,occluders:meshOccluders},{canvas:W.insetRenderer.domElement,camera:W.insetCamera,occluders:meshOccluders}],metadata:PART_META,onSelect:()=>G9SIM.pause()});
  const draw=W.draw;W.draw=function(t){draw(t);inspector.update()};G9SIM.inspector=inspector;
  const mobile=()=>matchMedia('(max-width:980px)').matches;
  function syncLayout(){const narrow=mobile(),opened=$('case-panel').classList.contains('mobile-open');$('toggle-cases').setAttribute('aria-expanded',String(narrow?opened:!document.body.classList.contains('cases-collapsed')));$('case-panel').setAttribute('role',narrow&&opened?'dialog':'complementary');$('case-panel').setAttribute('aria-modal',String(narrow&&opened));if(narrow&&!opened)$('case-panel').setAttribute('aria-hidden','true');else $('case-panel').removeAttribute('aria-hidden');W.resize()}
  function closeCases(){const wasOpen=$('case-panel').classList.contains('mobile-open');$('case-panel').classList.remove('mobile-open');$('cases-backdrop').classList.remove('is-open');document.querySelector('.middle').inert=false;document.querySelector('.device-sidebar').inert=false;document.querySelector('.app-header').inert=false;syncLayout();if(wasOpen&&lastFocus)lastFocus.focus()}
  function toggleCases(){if(mobile()){if($('case-panel').classList.contains('mobile-open'))return closeCases();lastFocus=document.activeElement;$('case-panel').classList.add('mobile-open');$('cases-backdrop').classList.add('is-open');document.querySelector('.middle').inert=true;document.querySelector('.device-sidebar').inert=true;document.querySelector('.app-header').inert=true;syncLayout();$('case-search').focus()}else{document.body.classList.toggle('cases-collapsed');syncLayout()}}
  $('toggle-cases').onclick=toggleCases;$('close-cases').onclick=closeCases;$('cases-backdrop').onclick=closeCases;
  document.querySelectorAll('[data-detail]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-detail]').forEach(x=>{const active=x===b;x.classList.toggle('active',active);x.setAttribute('aria-selected',String(active));$(x.dataset.detail==='device'?'device-pane':'explain-pane').hidden=!active})});
  document.querySelector('.detail-tabs').addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key))return;e.preventDefault();const buttons=[...document.querySelectorAll('[data-detail]')];const i=buttons.indexOf(document.activeElement);const next=buttons[(i+1)%buttons.length];next.click();next.focus()});
  $('case-list').addEventListener('click',e=>{if(e.target.closest('[data-case]')){inspector.close();if(mobile())closeCases()}});
  for(const id of ['next','previous','replay'])$(id).addEventListener('click',()=>inspector.close());
  document.addEventListener('keydown',e=>{if(!mobile()||!$('case-panel').classList.contains('mobile-open'))return;if(e.key==='Escape'){e.preventDefault();closeCases()}if(e.key==='Tab'){const focusable=[...$('case-panel').querySelectorAll('button,input')].filter(x=>x.offsetParent!==null);const i=focusable.indexOf(document.activeElement);if(e.shiftKey&&i<=0){e.preventDefault();focusable.at(-1)?.focus()}else if(!e.shiftKey&&i===focusable.length-1){e.preventDefault();focusable[0]?.focus()}}});
  window.addEventListener('resize',()=>{if(!mobile())closeCases();else syncLayout()});
  new ResizeObserver(()=>W.resize()).observe(document.querySelector('.middle'));
  window.SafeLockUI={toggleCases,closeCases,syncLayout};syncLayout();
})();
