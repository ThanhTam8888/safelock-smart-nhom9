from pathlib import Path
import json
from build_model import PARTS, ROOT

def overlaps(a,b):
    x=a.BoundingBox();y=b.BoundingBox()
    return x.xmax>y.xmin+.001 and y.xmax>x.xmin+.001 and x.ymax>y.ymin+.001 and y.ymax>x.ymin+.001 and x.zmax>y.zmin+.001 and y.zmax>x.zmin+.001

upper=[p for p in PARTS if p['group']=='upper']
lower=[p for p in PARTS if p['group']=='lower']
findings=[]
for angle in [0,2,5,10,20,45,75]:
    clashes=[]
    for a in upper:
        sa=a['shape'].rotate((0,-53,0),(1,-53,0),angle)
        for b in lower:
            sb=b['shape']
            if angle and b['id']=='09_cam_bolt':sb=sb.translate((12,0,0))
            if not overlaps(sa,sb):continue
            v=sa.intersect(sb).Volume()
            if v>.1:clashes.append({'upper':a['id'],'lower':b['id'],'mm3':round(v,3)})
    findings.append({'angle_deg':angle,'interferences_over_0_1_mm3':clashes})
    print(angle,clashes,flush=True)
(ROOT/'research/motion_validation.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding='utf-8')
