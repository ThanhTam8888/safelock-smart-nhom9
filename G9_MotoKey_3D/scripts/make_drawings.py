from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb

ROOT=Path(__file__).resolve().parents[1]
parts=json.loads((ROOT/'presentation/model_data.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'Arial','font.size':10,'svg.fonttype':'none'})
fig=plt.figure(figsize=(16.54,11.69),facecolor='#fbfaf6')
fig.text(.05,.95,'SAFELOCK SMART / G9',fontsize=23,weight='bold',color='#243039')
fig.text(.05,.915,'BẢN VẼ BỐ TRÍ TỔNG THỂ — CONCEPT R01',fontsize=12,color='#d85d22')
fig.text(.95,.94,'Đơn vị: mm\nKhông đo kích thước từ bản in',ha='right',va='top',fontsize=10,color='#68736c')
def project(ax,uv,depth,title):
    polys=[];colors=[];ds=[]
    for p in parts:
        if p['group']=='context':continue
        v=np.array(p['v']).reshape(-1,3);f=np.array(p['f']).reshape(-1,3)
        tri=v[f];n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);length=np.linalg.norm(n,axis=1);good=length>1e-8;n[good]/=length[good,None]
        # View from positive depth axis. Backfaces excluded, painter depth resolves cutouts.
        keep=n[:,depth]>.000001
        light=np.clip(.65+.35*n[:,depth],.35,1)
        c=np.array(to_rgb(p['color']))
        col=np.clip(c[None,:]*light[:,None]*.85+.14,0,1)
        polys.extend(tri[keep][:,:,uv]);colors.extend(col[keep]);ds.extend(np.mean(tri[keep,:,depth],axis=1))
    order=np.argsort(ds)
    ax.add_collection(PolyCollection(np.array(polys)[order],facecolors=np.array(colors)[order],edgecolors='none',rasterized=True))
    ax.autoscale();ax.set_aspect('equal');ax.set_title(title,loc='left',fontsize=12,weight='bold',pad=15,color='#243039');ax.axis('off')
def dim(ax,a,b,text,offset=0):
    a=np.array(a,dtype=float);b=np.array(b,dtype=float)
    if abs(a[1]-b[1])<.01:
        aa=a+[0,offset];bb=b+[0,offset];label=(aa+bb)/2+[0,2.3]
    else:aa=a+[offset,0];bb=b+[offset,0];label=(aa+bb)/2+[2.5,0]
    for v,w in [(a,aa),(b,bb)]:ax.plot([v[0],w[0]],[v[1],w[1]],c='#929c95',lw=.65)
    ax.annotate('',xy=aa,xytext=bb,arrowprops={'arrowstyle':'<->','color':'#52685d','lw':.9,'shrinkA':0,'shrinkB':0})
    ax.text(*label,text,ha='center',va='bottom',fontsize=9,color='#243039',bbox={'facecolor':'#fbfaf6','edgecolor':'none','pad':1.8})
ax=fig.add_axes([.05,.47,.56,.37]);project(ax,[1,2],0,'A / MẶT BÊN — trục tay ga vuông góc hình')
dim(ax,(-60,-27),(60,-27),'120',-13);dim(ax,(60,-27),(60,54.1),'≈81',15);dim(ax,(-25,0),(29,0),'54 · tâm tay ga → tâm rãnh',-57)
ax.annotate('Lòng đệm Ø34\nBore cứng Ø40,6',xy=(-25,0),xytext=(-76,39),fontsize=9,arrowprops={'arrowstyle':'->','color':'#52685d'},color='#243039')
ax.annotate('Chốt Ø6 × 16\nRút 12 trước khi mở',xy=(48,-11),xytext=(67,27),fontsize=9,arrowprops={'arrowstyle':'->','color':'#52685d'},color='#243039')
ax.set_xlim(-88,92);ax.set_ylim(-64,70)
ax=fig.add_axes([.67,.50,.27,.34]);project(ax,[0,2],1,'B / MẶT ĐẦU')
dim(ax,(-24,-27),(24,-27),'48 · thân kẹp',-13);ax.set_xlim(-45,45);ax.set_ylim(-47,68)
ax=fig.add_axes([.06,.10,.45,.27]);project(ax,[1,0],2,'C / MẶT TRÊN')
dim(ax,(-37,22),(43,22),'80 · nắp điện tử',10);dim(ax,(43,-22),(43,22),'44',12);ax.set_xlim(-76,83);ax.set_ylim(-43,45)
text='THÔNG SỐ VÀ RÀNG BUỘC THIẾT KẾ\n\n• Bao ngoài xấp xỉ 120 × 52 × 81, tính cả đầu trục và mặt ổ khóa.\n• Tay ga thử nghiệm: Ø34; dự kiến đệm Ø30 / 32 / 34 / 36.\n• Trục bản lề: Ø6; ruột khóa chỉ là bao hình mua hàng.\n• PCB riêng: 60 × 32 × 1,6; pin: bao hình 60 × 30 × 8.\n• Khe lắp trục Ø6 vào lỗ Ø6,3 là khởi điểm, cần chốt dung sai.\n• Bản vẽ bố trí, chưa phải bộ bản vẽ gia công có GD&T.\n• Mức mở minh họa 75°; thiết kế chặn mở phải chốt khi làm mẫu.\n• Kiểm tra tay phanh, gù, dây ga và nhựa đầu xe trước chốt mẫu.'
fig.text(.56,.355,text,va='top',fontsize=10,linespacing=1.65,color='#243039')
fig.text(.05,.035,'R01 / 26.10.2026  |  Nguồn hình: lưới từ CAD tham số  |  Tỷ lệ hiển thị thay đổi theo khổ giấy  |  Chưa xác nhận bằng thử nghiệm vật lý',fontsize=9,color='#68736c')
fig.savefig(ROOT/'CAD/Ban_ve_bo_tri_G9_A3.pdf',facecolor=fig.get_facecolor())
fig.savefig(ROOT/'CAD/Ban_ve_bo_tri_G9.svg',facecolor=fig.get_facecolor())
fig.savefig(ROOT/'presentation/G9_ban_ve_ky_thuat.png',dpi=160,facecolor=fig.get_facecolor())
print('Technical drawings generated')
