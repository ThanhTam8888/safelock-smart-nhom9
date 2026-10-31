from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    errors=[];remote_requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:remote_requests.append(r.url) if r.url.startswith(('http://','https://')) else None)
    page.goto((ROOT/'presentation/Mo_hinh_3D_SafeLock.html').as_uri())
    page.wait_for_function('window.G9 && G9.ready')
    page.wait_for_timeout(500)
    for mode in ['product','mounted','exploded','inside','open']:
        page.locator(f'[data-mode="{mode}"]').click()
        page.wait_for_timeout(450)
        page.screenshot(path=str(ROOT/'presentation'/f'G9_{mode}_viewer.png'))
    page.locator('#explode').fill('10')
    page.locator('#explode').dispatch_event('input')
    page.wait_for_timeout(200)
    assert page.locator('#slider-value').inner_text()=='0°'
    page.locator('#explode').fill('100');page.locator('#explode').dispatch_event('input')
    assert page.locator('#slider-value').inner_text()=='75°'
    page.set_viewport_size({'width':430,'height':920})
    page.evaluate('document.body.classList.remove("capture");G9.setMode("mounted",true)')
    page.wait_for_timeout(100)
    page.screenshot(path=str(ROOT/'research/mobile_viewer.png'),full_page=True)
    checks={'javascript_errors':errors,'mesh_count':page.evaluate('G9.meshes.length'),'canvas_count':page.locator('canvas').count(),'offline_file':True,'remote_requests':remote_requests,'modes_checked':['product','mounted','exploded','inside','open'],'toolbar_buttons_clicked':True,'open_slider_checked':True}
    (ROOT/'research/viewer_validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(checks))
    browser.close()
