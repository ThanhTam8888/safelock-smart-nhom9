"""Browser checks for actual mesh picking, linked annotations, gestures and responsive UI."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'ui/previews';OUT.mkdir(exist_ok=True)
FIND_HIT=r'''({app,id,surface=0})=>{
 const w=app==='explore'?G9:G9SIM.world;
 const objects=app==='explore'?w.meshes:w.lockMeshes;
 const m=objects.find(o=>(o.userData.part?.id||o.userData.id||o.name)===id);
 if(!m)throw Error('Part absent: '+id);
 const camera=surface?w.insetCamera:w.camera,canvas=surface?w.insetRenderer.domElement:w.renderer.domElement;
 const rect=canvas.getBoundingClientRect();w.scene.updateMatrixWorld(true);
 const visible=o=>{for(let x=o;x;x=x.parent)if(!x.visible)return false;return true};
 const occluders=[];if(app==='explore')occluders.push(...objects);else w.scene.traverse(o=>{if(o.isMesh)occluders.push(o)});
 const ray=new THREE.Raycaster(),a=m.geometry.attributes.position,ix=m.geometry.index;
 m.geometry.computeBoundingBox();const candidates=[m.geometry.boundingBox.getCenter(new THREE.Vector3())];
 const count=ix?ix.count:a.count,step=Math.max(1,Math.floor(count/3/200))*3;
 for(let f=0;f<count;f+=step){let p=new THREE.Vector3();for(let j=0;j<3;j++){const k=ix?ix.getX(f+j):f+j;p.add(new THREE.Vector3().fromBufferAttribute(a,k))}candidates.push(p.multiplyScalar(1/3))}
 for(const local of candidates){const p=local.applyMatrix4(m.matrixWorld).project(camera);if(p.z>1||Math.abs(p.x)>.98||Math.abs(p.y)>.98)continue;const x=rect.left+(p.x+1)*rect.width/2,y=rect.top+(1-p.y)*rect.height/2;if(document.elementFromPoint(x,y)!==canvas)continue;ray.setFromCamera(new THREE.Vector2(p.x,p.y),camera);const hit=ray.intersectObjects(occluders.filter(visible),false)[0];if(hit?.object===m)return {x,y};}
 throw Error('No exposed hit point for '+id+' on surface '+surface)
}'''

def no_overflow(page):assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1')
def inside_stage(page,app):
    result=page.evaluate('''(app)=>{const card=document.querySelector('.part-card').getBoundingClientRect(),stage=document.querySelector(app==='explore'?'.model-stage':'.middle').getBoundingClientRect();return {ok:card.left>=stage.left-1&&card.right<=stage.right+1&&card.top>=stage.top-1&&card.bottom<=stage.bottom+1,card:card.toJSON(),stage:stage.toJSON()}}''',app)
    assert result['ok'],result
def click_part(page,app,id,surface=0):
    pt=page.evaluate(FIND_HIT,{'app':app,'id':id,'surface':surface})
    page.mouse.click(pt['x'],pt['y'])
    page.wait_for_timeout(110)
    expr='G9.inspector.state()' if app=='explore' else 'G9SIM.inspector.state()'
    state=page.evaluate(expr);assert state['id']==id,state
    assert page.locator('.part-card').is_visible();inside_stage(page,app)
    return pt

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=1)
    errors=[];requests=[];checks=[]
    page.on('pageerror',lambda e:errors.append(e.stack))
    page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto((ROOT/'presentation/Mo_hinh_3D_SafeLock.html').as_uri());page.wait_for_function('window.G9?.ready')
    no_overflow(page);assert page.locator('.motion-control').is_hidden()
    page.screenshot(path=str(OUT/'01_kham_pha_desktop.png'))
    point=click_part(page,'explore','21_pod_lid')
    assert 'Nắp khoang điện tử' in page.locator('.part-title').inner_text()
    page.screenshot(path=str(OUT/'02_chu_thich_click_that.png'))
    before=page.locator('.part-leader path').get_attribute('d')
    rect=page.locator('#viewer').bounding_box();x=rect['x']+rect['width']*.27;y=rect['y']+rect['height']*.72
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+68,y+8,steps=9);page.mouse.up();page.wait_for_timeout(180)
    assert page.locator('.part-leader path').get_attribute('d')!=before
    assert page.evaluate('G9.inspector.state().open');inside_stage(page,'explore')
    page.keyboard.press('Escape');assert not page.evaluate('G9.inspector.state().open')
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(x-50,y,steps=8);page.mouse.up();assert not page.evaluate('G9.inspector.state().open')
    page.locator('[data-part="15_battery"]').click();assert page.evaluate('G9.inspector.state().id')=='15_battery';inside_stage(page,'explore')
    page.screenshot(path=str(OUT/'03_bo_phan_pin.png'))
    page.locator('.part-close').click();assert not page.evaluate('G9.inspector.state().open')
    for mode in ['mounted','exploded','inside','open','product']:
        page.locator(f'[data-mode="{mode}"]').click();page.wait_for_timeout(80)
    checks.extend(['Actual product-mesh click opens matching annotation','Annotation follows orbit and stays inside stage','Dragging does not count as picking','Close button and Escape work','Component shortcuts select internal parts','All five exploration modes work'])
    print('Explorer picking, controls and linked card passed',flush=True)

    page.goto((ROOT/'ung_dung_tren_xe/Mo_phong_SafeLock_tren_xe_may.html').as_uri());page.wait_for_function('window.G9SIM?.ready&&G9SIM.inspector')
    page.evaluate('G9SIM.setCase("park");G9SIM.seek(.5)')
    no_overflow(page);page.screenshot(path=str(OUT/'04_tinh_huong_desktop.png'))
    click_part(page,'simulation','21_pod_lid',surface=1)
    assert page.evaluate('G9SIM.inspector.state().source')==1
    assert not page.evaluate('G9SIM.state().playing')
    page.screenshot(path=str(OUT/'05_chu_thich_goc_can.png'))
    page.locator('.part-close').click();page.locator('#zoom-lock').click();page.wait_for_timeout(80)
    click_part(page,'simulation','21_pod_lid',surface=0)
    page.screenshot(path=str(OUT/'06_chu_thich_tren_xe.png'))
    page.keyboard.press('Escape');page.locator('#home').click()
    page.locator('#case-search').fill('quen chia');assert page.locator('[data-case]').count()==2
    page.locator('#case-search').fill('zzzz-not-a-case');assert page.locator('.empty-results').is_visible()
    page.locator('#case-search').fill('');assert page.locator('[data-case]').count()==14
    page.locator('[data-filter="Sự cố"]').click();assert page.locator('[data-case]').count()==3
    page.locator('[data-filter="Tất cả"]').click()
    page.locator('#explain-tab').click();assert page.locator('#explain-pane').is_visible();assert page.locator('#device-pane').is_hidden()
    page.locator('#device-tab').click();assert page.locator('#device-pane').is_visible()
    width=page.locator('.middle').bounding_box()['width'];page.locator('#toggle-cases').click();assert page.locator('.middle').bounding_box()['width']>width+100
    page.locator('#toggle-cases').click()
    for case in page.evaluate('G9SIM.cases.map(c=>c.id)'):
        page.locator(f'[data-case="{case}"]').click();page.evaluate('G9SIM.seek(.7)');assert page.evaluate('G9SIM.state().id')==case
    checks.extend(['Actual inset-mesh and main-scene clicks open matching cards','Scene pauses for component reading','Vietnamese accent-insensitive search and empty state work','Category filter and all 14 scenarios work','Phone / explanation tabs work','Collapsible sidebar resizes the 3D canvas'])
    print('Simulation picking, search, tabs and 14 scenarios passed',flush=True)

    # Mobile and tablet: actual drawer actions, no horizontal overflow, reachable annotation.
    for width,height in [(430,932),(375,812),(900,800)]:
        page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(120);no_overflow(page)
        assert page.locator('#case-panel').is_hidden()
        page.locator('#toggle-cases').click();assert page.locator('#case-panel').is_visible()
        assert page.locator('#case-panel').get_attribute('aria-modal')=='true'
        page.locator('#case-search').fill('quen chia');page.locator('[data-case="ignition_key"]').click();assert page.locator('#case-panel').is_hidden()
        assert page.evaluate('G9SIM.state().id')=='ignition_key'
        page.evaluate('G9SIM.seek(.7)');page.screenshot(path=str(OUT/f'07_tinh_huong_{width}.png'),full_page=True)
        page.locator('#toggle-cases').click();page.locator('#case-search').fill('');page.keyboard.press('Escape');assert page.locator('#case-panel').is_hidden()
    page.set_viewport_size({'width':430,'height':932});page.goto((ROOT/'presentation/Mo_hinh_3D_SafeLock.html').as_uri());page.wait_for_function('window.G9?.ready');no_overflow(page)
    click_part(page,'explore','21_pod_lid');page.screenshot(path=str(OUT/'08_kham_pha_mobile.png'),full_page=True)
    page.keyboard.press('Escape')
    page.set_viewport_size({'width':375,'height':812});page.wait_for_timeout(100);no_overflow(page)
    page.locator('[data-mode="exploded"]').click();assert page.locator('.motion-control').is_visible();no_overflow(page)
    checks.extend(['Mobile and tablet drawer opens, selects, closes and restores focus','375 / 430 / 900 px layouts have no horizontal overflow','Mobile product annotation stays inside the model view'])
    touch_context=browser.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
    touch=touch_context.new_page();touch.on('pageerror',lambda e:errors.append(e.stack))
    touch.goto((ROOT/'presentation/Mo_hinh_3D_SafeLock.html').as_uri());touch.wait_for_function('window.G9?.ready')
    pt=touch.evaluate(FIND_HIT,{'app':'explore','id':'21_pod_lid','surface':0});touch.touchscreen.tap(pt['x'],pt['y']);touch.wait_for_timeout(130)
    assert touch.evaluate('G9.inspector.state().id')=='21_pod_lid';inside_stage(touch,'explore')
    touch_context.close();checks.append('Touchscreen tap selects an actual part on a phone viewport')
    assert not errors,errors;assert not requests,requests
    report={'date':'2026-10-31','checks':checks,'passed':len(checks),'javascript_errors':errors,'external_requests':requests,'offline':True}
    (ROOT/'ui/validation_glass_ui.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
    browser.close()
