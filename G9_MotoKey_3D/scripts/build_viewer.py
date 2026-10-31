from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'ui'))
from nav import add_video_tab
p=ROOT/'presentation'
html=(ROOT/'ui/explore.html').read_text(encoding='utf-8')
html=add_video_tab(html,'../video/Video_cach_van_hanh.html')
for key,path in [('THREE',p/'vendor/three.min.js'),('ORBIT',p/'vendor/OrbitControls.js'),('MODEL',p/'model_data.json'),('GLASS_CSS',ROOT/'ui/liquid-glass.css'),('READABILITY_CSS',ROOT/'ui/readability.css'),('REALISM',ROOT/'ui/realism.js'),('INSPECTOR',ROOT/'ui/component_inspector.js'),('VIEWER',p/'viewer.js')]:
    html=html.replace('/*__'+key+'__*/',path.read_text(encoding='utf-8'))
meta=json.loads((ROOT/'research/part_manifest.json').read_text(encoding='utf-8'))
html=html.replace('</style>','\n'+(ROOT/'ui/video-nav.css').read_text(encoding='utf-8')+'\n</style>',1)
html=html.replace('/*__PART_META__*/',json.dumps([{k:x[k] for k in ['id','name','material','note']} for x in meta],ensure_ascii=False))
(p/'Mo_hinh_3D_SafeLock.html').write_text(html,encoding='utf-8')
print('Wrote offline viewer:',(p/'Mo_hinh_3D_SafeLock.html').stat().st_size)
