"""Render deterministic 3D frames to Full HD MP4s with matching spatial cues."""
from pathlib import Path
import base64,json,subprocess,time,sys
from playwright.sync_api import sync_playwright
from build_library import films,build

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FFMPEG=next((Path.home()/'AppData/Local/Microsoft/WinGet/Packages').rglob('ffmpeg.exe'))
FPS=24
CHROME=r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def render(ids=None):
    for folder in ['cues','posters','captions']:(HERE/folder).mkdir(exist_ok=True)
    previous=HERE/'render_report.json'
    report=json.loads(previous.read_text(encoding='utf-8'))['videos'] if ids and previous.exists() else []
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox','--allow-file-access-from-files'])
        page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        engine=None
        for f in films():
            if ids and f['id'] not in ids:continue
            if f['engine']!=engine:
                engine=f['engine']
                src=ROOT/('presentation/Mo_hinh_3D_SafeLock.html' if engine=='product' else 'ung_dung_tren_xe/Mo_phong_SafeLock_tren_xe_may.html')
                page.goto(src.as_uri());page.wait_for_function('window.G9?.ready' if engine=='product' else 'window.G9SIM?.ready')
                if engine=='product':page.add_script_tag(content=(HERE/'director.js').read_text(encoding='utf-8'))
            target=(HERE/f['src']).resolve();temp=target.with_name(target.stem+'_rendering.mp4')
            args=[str(FFMPEG),'-y','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','mjpeg','-framerate',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(temp)]
            process=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            cues=[];last_chapter=-1;start=time.perf_counter();poster_at={'operation':24,'mechanism':1,'forgotten':2,'scenarios':33}[f['id']]
            for n in range(f['duration']*FPS):
                t=n/FPS;ci=max(i for i,c in enumerate(f['chapters']) if t>=c['start']);c=f['chapters'][ci]
                title=c['title'];caption=f"Bước {ci+1}/{len(f['chapters'])} · {f['tag']}"
                if c.get('stages'):
                    stage=max(x for x in c['stages'] if (t-c['start'])/(c['end']-c['start'])>=x[0]);caption=stage[1]+' · '+stage[2]
                    if len(caption)>150:caption=caption[:147]+'…'
                result=page.evaluate('(x)=>G9FILM.frame(x.id,x.time,{title:x.title,caption:x.caption})',dict(id=f['id'],time=t,title=title,caption=caption))
                data=base64.b64decode(result['jpeg'].split(',')[1]);process.stdin.write(data)
                if n%12==0:cues.append(dict(time=t,points=result['anchors']))
                if n==poster_at*FPS:(HERE/f['poster']).write_bytes(data)
                m=result.get('mechanism')
                if m and m['angle']>.01:assert m['stroke']>=11.99,(f['id'],t,m)
                if ci!=last_chapter:print(f"{f['id']}: chapter {ci+1}/{len(f['chapters'])}, t={t:.1f}s",flush=True);last_chapter=ci
            process.stdin.close();stderr=process.stderr.read().decode(errors='replace');code=process.wait()
            if code:raise RuntimeError(stderr)
            temp.replace(target)
            (HERE/'cues'/f"{f['id']}.json").write_text(json.dumps(cues,separators=(',',':')),encoding='utf-8')
            report=[r for r in report if r['id']!=f['id']]
            report.append(dict(id=f['id'],path=str(target.relative_to(ROOT)),duration=f['duration'],fps=FPS,width=1920,height=1080,frames=f['duration']*FPS,cue_samples=len(cues),megabytes=round(target.stat().st_size/1e6,2),render_seconds=round(time.perf_counter()-start,1)))
            print(json.dumps(report[-1]),flush=True)
        browser.close()
    assert not errors,errors
    (HERE/'render_report.json').write_text(json.dumps(dict(videos=report,javascript_errors=errors),ensure_ascii=False,indent=2),encoding='utf-8')
    build()

if __name__=='__main__':render(sys.argv[1:] or None)
