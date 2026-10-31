from pathlib import Path
import json
import sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'ui'))
from nav import add_video_tab
html=(ROOT/'ui/simulation.html').read_text(encoding='utf-8')
html=add_video_tab(html,'../video/Video_cach_van_hanh.html')
sources={'THREE':ROOT/'presentation/vendor/three.min.js','ORBIT':ROOT/'presentation/vendor/OrbitControls.js','MODEL':ROOT/'presentation/model_data.json','SCENARIOS':HERE/'scenarios.json','SCENE':HERE/'scene_builder.js','SIMULATION':HERE/'simulation.js','GLASS_CSS':ROOT/'ui/liquid-glass.css','READABILITY_CSS':ROOT/'ui/readability.css','REALISM':ROOT/'ui/realism.js','INSPECTOR':ROOT/'ui/component_inspector.js','SIM_UI':ROOT/'ui/simulation-ui.js','DIRECTOR':ROOT/'video/director.js'}
for key,file in sources.items():html=html.replace('/*__'+key+'__*/',file.read_text(encoding='utf-8'))
meta=json.loads((ROOT/'research/part_manifest.json').read_text(encoding='utf-8'))
html=html.replace('</style>','\n'+(ROOT/'ui/video-nav.css').read_text(encoding='utf-8')+'\n</style>',1)
html=html.replace('/*__PART_META__*/',json.dumps([{k:x[k] for k in ['id','name','material','note']} for x in meta],ensure_ascii=False))
(HERE/'Mo_phong_SafeLock_tren_xe_may.html').write_text(html,encoding='utf-8')
print('Built offline simulator, bytes:',len(html.encode('utf-8')))
