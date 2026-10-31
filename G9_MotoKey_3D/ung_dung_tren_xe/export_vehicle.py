from pathlib import Path
import json,numpy as np,trimesh
HERE=Path(__file__).resolve().parent
raw=json.loads((HERE/'scene_geometry.json').read_text(encoding='utf-8'))
scene=trimesh.Scene()
for i,p in enumerate(raw):
    v=np.array(p['v'],dtype=float).reshape(-1,3)
    f=np.array(p['f'] if p['f'] is not None else np.arange(len(v)),dtype=int).reshape(-1,3)
    m=trimesh.Trimesh(v,f,process=False)
    rgb=[int(p['color'][k:k+2],16) for k in [1,3,5]]
    material=trimesh.visual.material.PBRMaterial(name=p['name'],baseColorFactor=rgb+[255],metallicFactor=.15,roughnessFactor=.55)
    m.visual=trimesh.visual.TextureVisuals(material=material)
    scene.add_geometry(m,node_name=f'{i:03d}_{p["name"]}',geom_name=f'{i:03d}_{p["name"]}')
scene.export(str(HERE/'Xe_may_va_SafeLock_R02.glb'))
check=trimesh.load(str(HERE/'Xe_may_va_SafeLock_R02.glb'),force='scene')
assert len(check.geometry)==len(raw)
print('Exported vehicle + lock + owner:',len(raw),'meshes; units meters')
