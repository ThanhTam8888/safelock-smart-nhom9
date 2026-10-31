"""Exercise offline playback, timed explanations, seeking, mobile and video encoding."""
from pathlib import Path
import json,subprocess,math
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OUT=HERE/'previews';OUT.mkdir(exist_ok=True)
BIN=next((Path.home()/'AppData/Local/Microsoft/WinGet/Packages').rglob('ffmpeg.exe')).parent
checks=[];media=[];errors=[];remote=[]
library=json.loads((HERE/'library.json').read_text(encoding='utf-8'))
for f in library:
    path=(HERE/f['src']).resolve()
    probe=json.loads(subprocess.check_output([str(BIN/'ffprobe.exe'),'-v','error','-show_streams','-show_format','-of','json',str(path)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert stream['width']==1920 and stream['height']==1080
    assert stream['avg_frame_rate']=='24/1'
    assert abs(float(probe['format']['duration'])-f['duration'])<.05
    assert int(stream['nb_frames'])==f['duration']*24
    decode=subprocess.run([str(BIN/'ffmpeg.exe'),'-v','error','-i',str(path),'-f','null','-'],capture_output=True)
    assert decode.returncode==0 and not decode.stderr,decode.stderr.decode(errors='replace')
    assert (HERE/f['poster']).is_file()
    assert f['anchors'] and len(f['anchors'])==f['duration']*2
    assert all(math.isfinite(x) for s in f['anchors'] for p in s['points'].values() for x in p.values())
    media.append(dict(id=f['id'],seconds=f['duration'],frames=stream['nb_frames'],size=[stream['width'],stream['height']],fps=stream['avg_frame_rate'],decode='passed',spatial_cues=len(f['anchors'])))
checks.append('All four MP4s decode completely: Full HD / 24 fps / correct frame count and duration')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--no-sandbox'])
    page=b.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:remote.append(r.url) if r.url.startswith(('http://','https://')) else None)
    page.goto((HERE/'Video_cach_van_hanh.html').as_uri());page.wait_for_function('window.G9VIDEO&&document.querySelector("video").readyState>=1')
    assert page.locator('.app-tabs a').count()==3
    assert not page.locator('#cue-card').is_visible()
    page.locator('#start-film').click();page.wait_for_function('document.querySelector("video").currentTime>.12')
    assert page.locator('#cue-card').is_visible()
    assert page.locator('#cue-title').inner_text()==library[0]['chapters'][0]['title']
    page.locator('#pause-read').click();assert page.evaluate('G9VIDEO.state().paused')
    page.locator('[data-chapter="1"]').click();page.wait_for_function('G9VIDEO.state().time>=7&&G9VIDEO.state().chapter===1')
    page.locator('#pause-read').click();assert page.evaluate('G9VIDEO.state().paused')
    page.locator('#close-cue').click();assert not page.locator('#cue-card').is_visible()
    page.locator('#cue-point').click();assert page.locator('#cue-card').is_visible()
    page.locator('#show-cues').uncheck();assert not page.locator('#cue-card').is_visible()
    page.locator('#film-seek').fill('2170');page.locator('#film-seek').dispatch_event('input')
    page.wait_for_function('G9VIDEO.state().chapter===3')
    assert not page.locator('#cue-card').is_visible()
    page.locator('#show-cues').check();assert page.locator('#cue-card').is_visible()
    assert page.locator('#cue-title').inner_text()==library[0]['chapters'][3]['title']
    page.wait_for_function('document.querySelector("video").readyState>=2')
    page.screenshot(path=str(OUT/'video_desktop.png'),full_page=True)
    checks.append('Playing shows synchronized explanation; pause, seek, close, hotspot reopen and hide/show work')
    page.locator('#captions').click();page.wait_for_function('document.querySelector("video").textTracks[0]?.cues?.length===8')
    assert page.evaluate('document.querySelector("video").textTracks[0].mode')=='showing'
    page.locator('#film-speed').select_option('0.5');assert page.evaluate('document.querySelector("video").playbackRate')==.5
    page.locator('#captions').click();assert page.evaluate('document.querySelector("video").textTracks[0].mode')=='hidden'
    checks.append('Vietnamese captions load offline from Blob; playback speed works')
    for index,f in enumerate(library):
        page.locator(f'[data-film="{index}"]').click();page.wait_for_function('(duration)=>document.querySelector("video").duration===duration',arg=f['duration'])
        assert page.evaluate('document.querySelector("video").videoHeight')==1080
        assert page.locator('#chapters button').count()==len(f['chapters'])
        page.locator('#play-film').click();page.evaluate('(t)=>G9VIDEO.seek(t)',f['chapters'][-1]['start']+.25)
        page.wait_for_function('(i)=>G9VIDEO.state().chapter===i',arg=len(f['chapters'])-1)
        assert page.locator('#cue-title').inner_text()==f['chapters'][-1]['title']
        assert page.locator('#cue-card').is_visible()
        assert not page.locator('#film-error').is_visible()
    checks.append('Selecting all four films loads correct file, chapters and last-step explanation')
    page.locator('[data-film="0"]').click();page.wait_for_function('document.querySelector("video").duration===56');page.locator('#play-film').click();page.evaluate('G9VIDEO.seek(17)');page.wait_for_function('document.querySelector("video").readyState>=2')
    page.locator('#fullscreen').click();page.wait_for_function('!!document.fullscreenElement');assert page.locator('#cue-card').is_visible();page.evaluate('document.exitFullscreen()')
    checks.append('Fullscreen keeps the video and its explanation together')
    for width in [900,430,375]:
        page.set_viewport_size({'width':width,'height':920});page.wait_for_timeout(100)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
        assert page.locator('#cue-card').is_visible()
        rect=page.locator('#cue-card').bounding_box();assert rect['x']>=0 and rect['x']+rect['width']<=width+1
        if width<=850:assert page.evaluate('document.querySelector(".chapter-panel").nextElementSibling.matches(".library-heading")')
        if width==430:page.screenshot(path=str(OUT/'video_mobile.png'),full_page=True)
    checks.append('900 / 430 / 375 px layouts fit; mobile explanation sits below the film')
    for rel in ['presentation/Mo_hinh_3D_SafeLock.html','ung_dung_tren_xe/Mo_phong_SafeLock_tren_xe_may.html']:
        page.goto((ROOT/rel).as_uri());page.wait_for_selector('.app-tabs a')
        links=page.locator('.app-tabs a');assert links.count()==3
        assert 'Video cách vận hành' in links.nth(2).inner_text()
        links.nth(2).click();page.wait_for_function('!!window.G9VIDEO')
    checks.append('The new video tab is reachable from both existing 3D pages')
    assert not errors and not remote,(errors,remote)
    b.close()
report=dict(revision='R04',passed=len(checks),checks=checks,media=media,javascript_errors=errors,external_requests=remote)
(HERE/'validation_video.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
