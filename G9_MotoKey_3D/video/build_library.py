"""Build an offline film library; content and cue times have one source of truth."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def films():
    items = json.loads((HERE/'library_source.json').read_text(encoding='utf-8'))
    cases = json.loads((ROOT/'ung_dung_tren_xe/scenarios.json').read_text(encoding='utf-8'))
    items[-1]['chapters'] = [dict(start=i*6,end=(i+1)*6,title=s['title'],body=s['goal'],detail=s['limit'],anchor='lock',tag=s['group'].upper(),stages=s['stages'],case=s['id']) for i,s in enumerate(cases)]
    for f in items:
        f['poster'] = f"posters/{f['id']}.jpg"
        cue = HERE/'cues'/f"{f['id']}.json"
        f['anchors'] = json.loads(cue.read_text(encoding='utf-8')) if cue.exists() else []
        f['captions'] = captions(f)
    return items

def stamp(t):
    return f'{int(t)//3600:02}:{int(t)//60%60:02}:{int(t)%60:02}.{int(round(t%1*1000)):03}'

def captions(f):
    return 'WEBVTT\n\n'+'\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['title']}\n{c['body']}" for i,c in enumerate(f['chapters']))+'\n'

def build():
    items = films()
    (HERE/'captions').mkdir(exist_ok=True)
    for f in items:
        (HERE/'captions'/f"{f['id']}.vtt").write_text(f['captions'],encoding='utf-8')
    (HERE/'library.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    s=(HERE/'page.html').read_text(encoding='utf-8')
    for marker,source in [('GLASS',ROOT/'ui/liquid-glass.css'),('STYLE',HERE/'player.css'),('PLAYER',HERE/'player.js')]:
        s=s.replace('/*__'+marker+'__*/',source.read_text(encoding='utf-8'))
    s=s.replace('/*__LIBRARY__*/',json.dumps(items,ensure_ascii=False).replace('</',r'<\/'))
    (HERE/'Video_cach_van_hanh.html').write_text(s,encoding='utf-8')
    print(f'Built offline video library: {len(items)} films / {sum(len(f["chapters"]) for f in items)} chapters')

if __name__=='__main__':build()
