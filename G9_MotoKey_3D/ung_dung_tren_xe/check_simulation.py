from pathlib import Path
import json
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
(HERE/'anh').mkdir(exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':1540,'height':1050},device_scale_factor=1)
    errors=[];remote=[]
    def on_error(e):
        errors.append(str(e));print('BROWSER ERROR:',e.stack,flush=True)
    page.on('pageerror',on_error)
    page.on('request',lambda r:remote.append(r.url) if r.url.startswith(('http://','https://')) else None)
    page.goto((HERE/'Mo_phong_SafeLock_tren_xe_may.html').as_uri());page.wait_for_function('window.G9SIM && G9SIM.ready',timeout=30000)
    results=[]
    for i,case in enumerate(page.evaluate('G9SIM.cases')):
        page.locator(f'[data-case="{case["id"]}"]').click()
        page.evaluate('G9SIM.seek(.7)')
        state=page.evaluate('G9SIM.state()')
        assert state['id']==case['id']
        results.append({'case':case['id'],'notice':state['notice']['title'],'power':state['power'],'network':state['network'],'gps':state['gps']})
        if case['id'] in ['park','ignition_key','forced_move','lift','removed_lock','phone_left']:
            page.screenshot(path=str(HERE/'anh'/f'{i+1:02d}_{case["id"]}.png'))
        print('Checked',case['id'],flush=True)
    # Capability boundaries: R01 cannot acquire the new BLE reminder automatically.
    page.evaluate('G9SIM.setCase("ignition_key");G9SIM.seek(.7);G9SIM.setTier("r01")')
    assert not page.evaluate('G9SIM.state().reminder')
    assert page.evaluate('G9SIM.state().keyOnBike')
    page.locator('#tier-r02').click()
    assert page.evaluate('G9SIM.state().reminder')
    page.evaluate('G9SIM.setCase("phone_left");G9SIM.seek(.7)')
    assert not page.evaluate('G9SIM.state().phoneCarried')
    assert page.evaluate('G9SIM.state().ble')=='Vẫn ở gần trên xe'
    page.evaluate('G9SIM.setCase("offline");G9SIM.seek(.65)')
    assert not page.evaluate('G9SIM.state().deliveredRemote')
    page.evaluate('G9SIM.seek(.9)')
    assert page.evaluate('G9SIM.state().deliveredRemote')
    page.evaluate('G9SIM.setCase("gps_lost");G9SIM.seek(.7)')
    assert page.evaluate('G9SIM.state().locationOld') and page.evaluate('G9SIM.state().network')
    page.evaluate('G9SIM.setCase("empty_battery");G9SIM.seek(.7)')
    assert not page.evaluate('G9SIM.state().power') and not page.evaluate('G9SIM.state().localBuzzer')
    assert page.evaluate('G9SIM.state().mechanicalClosed')
    page.evaluate('G9SIM.setCase("lift");G9SIM.seek(.9)')
    assert page.evaluate('G9SIM.world.vehicle.position.y')>=.805
    page.evaluate('G9SIM.setCase("authorized");G9SIM.seek(.7);G9SIM.setInputs({network:false})')
    assert 'Chưa gửi được' in page.evaluate('G9SIM.state().notice.title')
    page.evaluate('G9SIM.setInputs({network:true})')
    page.evaluate('G9SIM.setCase("forced_move");G9SIM.seek(.7)')
    page.locator('.inputs summary').click()
    page.locator('#network').uncheck()
    assert not page.evaluate('G9SIM.state().deliveredRemote')
    page.locator('#network').check()
    page.locator('#power').uncheck()
    assert not page.evaluate('G9SIM.state().localBuzzer')
    page.locator('#power').check()
    # Slider, pause/play, camera controls and responsive layout.
    page.locator('#timeline').fill('500');page.locator('#timeline').dispatch_event('input')
    assert abs(page.evaluate('G9SIM.state().p')-.5)<.001
    page.locator('#play').click();page.wait_for_timeout(250)
    assert page.evaluate('G9SIM.state().playing')
    page.locator('#play').click()
    page.locator('#zoom-lock').click();page.screenshot(path=str(HERE/'anh/15_can_canh_khoa_tren_xe.png'))
    page.locator('#home').click()
    page.evaluate('G9SIM.capture({id:"park",progress:.48,clean:false})')
    raw=page.evaluate('G9SIM.world.exportGeometry()')
    (HERE/'scene_geometry.json').write_text(json.dumps(raw,separators=(',',':')),encoding='utf-8')
    page.set_viewport_size({'width':430,'height':920});page.evaluate('G9SIM.world.resize()');page.screenshot(path=str(HERE/'anh/16_giao_dien_dien_thoai.png'),full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth+1')
    report={'javascript_errors':errors,'remote_requests':remote,'scenario_count':len(results),'cases':results,'mesh_count':page.evaluate('G9SIM.world.meshCount'),'exported_meshes':len(raw),'capability_boundary_tests':'passed','toolbar_and_slider':'passed','mobile_layout':'passed'}
    assert not errors and not remote
    (HERE/'kiem_tra_mo_phong.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},ensure_ascii=False),flush=True)
    browser.close()
