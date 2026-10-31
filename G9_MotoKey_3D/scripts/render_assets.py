from pathlib import Path
import math,json,subprocess
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'presentation'
FONT=Path(r'C:\Windows\Fonts\arial.ttf');BOLD=Path(r'C:\Windows\Fonts\arialbd.ttf')
def font(size,b=False):return ImageFont.truetype(str(BOLD if b else FONT),size)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',headless=True,args=['--no-sandbox','--allow-file-access-from-files','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=browser.new_page(viewport={'width':1600,'height':1200},device_scale_factor=1)
    page.goto((P/'Mo_hinh_3D_SafeLock.html').as_uri());page.wait_for_function('G9.ready')
    renders=[('product',{'distance':270,'az':.68,'elev':.5,'targetY':12}),('mounted',{'distance':330,'az':.76,'elev':.62,'targetY':13}),('exploded',{'distance':430,'az':.65,'elev':.28,'targetY':65}),('inside',{'distance':280,'az':.65,'elev':.65,'targetY':13}),('open',{'distance':390,'az':.65,'elev':.36,'targetY':45})]
    for name,args in renders:
        page.evaluate('(a)=>G9.capture(a)',dict(m=name,clean=True,**args));page.wait_for_timeout(150)
        page.screenshot(path=str(P/f'G9_{name}_render.png'))
        print('Render',name,flush=True)
    # Self-contained illustrated 3D walkthrough MP4: frames rendered from actual CAD meshes.
    frame_dir=ROOT/'research/video_frames';frame_dir.mkdir(exist_ok=True)
    page.set_viewport_size({'width':1280,'height':800})
    clips=[('product',50,'01 / HÌNH DÁNG SẢN PHẨM','Khóa kẹp tay ga và tay phanh · SafeLock Smart / Nhóm 9'),('mounted',40,'02 / VỊ TRÍ LẮP TRÊN XE','Minh họa trên tay lái mẫu · Cần đo kích thước xe thật'),('open',60,'03 / MỞ KHÓA BẰNG CHÌA','Rút chốt trước · Sau đó xoay nửa trên quanh trục bản lề'),('exploded',55,'04 / CẤU TẠO TÁCH LỚP','Vỏ, lõi thép, đệm, chốt khóa và cụm GPS + 4G'),('inside',40,'05 / BỐ TRÍ CỤM ĐIỆN TỬ','Pin 1S, PCB, SIM, GNSS, anten LTE · Bao hình thiết kế')]
    ffmpeg=r'C:\Users\88\AppData\Local\Microsoft\WinGet\Packages\yt-dlp.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-N-126374-g089a48eb36-win64-gpl\bin\ffmpeg.exe'
    proc=subprocess.Popen([ffmpeg,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','1280x800','-r','12','-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'SafeLock_G9_giai_thich_3D.mp4')],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=(ROOT/'research/video_render.log').open('w'))
    import io
    for name,count,title,subtitle in clips:
        for i in range(count):
            t=i/max(1,count-1)
            args={'m':name,'clean':True,'az':.52+t*.45,'elev':.48,'distance':330,'targetY':12}
            if name=='open':args.update(distance=415,targetY=42,elev=.36,open=t)
            elif name=='exploded':args.update(distance=490,targetY=60,elev=.26,explode=.25+.75*t)
            elif name=='inside':args.update(elev=.65,distance=310)
            page.evaluate('(a)=>G9.capture(a)',args)
            im=Image.open(io.BytesIO(page.screenshot())).convert('RGB');draw=ImageDraw.Draw(im)
            draw.rectangle((0,0,1280,98),fill='#f1f0e9');draw.text((35,22),title,font=font(25,True),fill='#243039');draw.text((35,59),subtitle,font=font(16),fill='#68736c')
            draw.rectangle((0,755,1280,800),fill='#243039');draw.text((35,770),'SAFELOCK SMART  /  G9  /  CONCEPT R01',font=font(12,True),fill='white');draw.text((745,770),'Mô hình số · Chưa phải thử nghiệm sản phẩm thật',font=font(13),fill='#e6e8df')
            proc.stdin.write(im.tobytes())
        print('Video section',name,flush=True)
    proc.stdin.close();returncode=proc.wait()
    if returncode:raise RuntimeError('FFmpeg render failed')
    browser.close()

# A presentation board made from rendered CAD, with independent explanatory panels.
board=Image.new('RGB',(2400,1800),'#f1f0e9');d=ImageDraw.Draw(board)
d.text((80,55),'SAFELOCK SMART',font=font(45,True),fill='#243039');d.text((80,113),'NHÓM 9  /  THIẾT KẾ CƠ KHÍ + ĐỊNH VỊ  /  R01',font=font(18),fill='#d85d22')
d.text((80,171),'Chiếc khóa trông thế nào, được tạo ra và vận hành ra sao?',font=font(31),fill='#243039');d.line((80,232,2320,232),fill='#cbd0c5',width=2)
panels=[('product','01  HÌNH DÁNG & KÍCH THƯỚC','Thân dài 120 mm · Rộng thân 48 mm · Cao tổng thể khoảng 81 mm'),('mounted','02  KẸP TAY GA VÀ TAY PHANH','Đệm mẫu Ø34 · Giữ phanh đã bóp · Khóa phải còn gắn trên xe'),('exploded','03  CÁC CỤM CHI TIẾT','Lõi thép và bản lề chịu lực; vỏ nhựa bảo vệ, đệm bảo vệ bề mặt'),('inside','04  CỤM ĐIỆN TỬ BỐ TRÍ RIÊNG','GNSS lấy tọa độ → 4G / SIM → máy chủ → điện thoại')]
for i,(name,title,sub) in enumerate(panels):
    x=80+(i%2)*1160;y=270+(i//2)*710
    im=Image.open(P/f'G9_{name}_render.png');im.thumbnail((1090,570));board.paste(im,(x+(1090-im.width)//2,y))
    d.text((x,y+580),title,font=font(24,True),fill='#243039');d.text((x,y+625),sub,font=font(17),fill='#68736c')
d.line((80,1700,2320,1700),fill='#cbd0c5',width=2);d.text((80,1725),'THIẾT KẾ ĐỂ PHÁT TRIỂN MẪU THỬ · Chưa xác nhận độ bền, thời lượng pin, độ kín và tương thích xe bằng thử nghiệm.',font=font(19),fill='#68736c')
board.save(P/'SafeLock_G9_bang_trinh_bay.png')
print('Presentation board and video complete',flush=True)
