# Video cách vận hành — R04

Mở **[Video_cach_van_hanh.html](Video_cach_van_hanh.html)** bằng Chrome/Edge, hoặc nhấp đúp `MO_VIDEO_VAN_HANH.cmd` ở thư mục dự án. Tab **Video cách vận hành** cũng có ở cả hai trang 3D.

- Bấm video hoặc nút phát: ô giải thích hình chữ nhật xuất hiện theo bước đang xem, có điểm đánh dấu và đường nối đến chi tiết trong cảnh.
- Bấm bước ở cột bên phải để tua. Khi tua ngược, chú thích cập nhật lại đúng bước. Có thể tạm dừng để đọc, đóng ô rồi bấm điểm **i** để mở lại.
- Tắt **Chú thích tự động** nếu muốn xem liền mạch. Nút **CC** bật phụ đề tiếng Việt; có tốc độ 0,5–2× và toàn màn hình kèm chú thích.
- Trên điện thoại, ô giải thích nằm dưới video để dễ đọc và giữ hình ảnh rõ ràng.
- Giữ nguyên cấu trúc thư mục khi sao chép. Tất cả video, phụ đề, thư viện 3D và mã giao diện chạy ngoại tuyến.

| Video | Thời lượng | Nội dung |
|---|---:|---|
| Gắn và tháo khóa đúng trình tự | 56 giây | 8 bước: chuẩn bị, rút chốt, mở, đặt vào tay ga/phanh, đóng, kiểm tra, rời xe, quay lại tháo |
| Nhìn gần cơ cấu bên trong | 28 giây | 7 bước: khung thép, đệm, chốt, bản lề, pin, mạch và anten |
| Rời xe nhưng quên chìa | 36 giây | 6 bước: chìa để lại, người mang điện thoại đi, nhắc kiểm tra R02, so sánh R01, quay lại lấy chìa |
| 14 tình huống trên xe máy | 84 giây | Mỗi tình huống 6 giây; có rung nhẹ, di chuyển xe, mất mạng, mất GNSS, cạn pin và khóa bị tách khỏi xe |

Cả bốn video là MP4 H.264, **1920 × 1080 / 24 fps**, tổng 3 phút 24 giây, không có lời đọc. 35 chương và chú thích đồng bộ nằm trong trang HTML; mở MP4 trực tiếp chỉ có tiêu đề/bước được ghép vào hình. Các file `.vtt` có thể dùng riêng khi dựng slide/video.

R04 bổ sung phản xạ môi trường, chất liệu kim loại/cao su/nhựa, bề mặt sơn xe mượt hơn và người tham chiếu có khớp tay/chân, bàn tay/ngón tay. Chuyển động khóa giữ trình tự **rút chốt trước khi mở bản lề; khép nắp trước khi đưa chốt về**. Mẫu CAD 50 chi tiết vẫn dùng cùng hình học cơ khí.

Đây là thiết kế và mô phỏng tham chiếu để làm mẫu thử, chưa phải sản phẩm đã thử nghiệm ngoài đời. Hall chỉ nhận hai nửa áp sát; R02 BLE/app là đề xuất nhắc kiểm tra chung, chưa tự nhận biết chính xác chìa còn trong ổ. Không có tự mở khóa hoặc điều khiển phanh từ ứng dụng.

## Nguồn và dựng lại

- `library_source.json`: nội dung, mốc chương, điểm cần chú thích. Video 14 tình huống lấy nội dung từ `ung_dung_tren_xe/scenarios.json`.
- `director.js`: tư thế, camera, chuyển động cơ khí, vị trí chú thích ở từng khung hình.
- `render_videos.py`: xuất video bằng Chrome/WebGL và FFmpeg, đồng thời lấy tọa độ chú thích từ chính camera dựng phim.
- `build_library.py`, `page.html`, `player.css`, `player.js`: tạo trang video ngoại tuyến.
- `cues/`, `posters/`, `captions/`: dữ liệu đồng bộ và nội dung phụ trợ.
- `check_videos.py`: giải mã toàn bộ video, kiểm tra thời lượng/khung hình, phát/tua/chú thích/phụ đề/toàn màn hình, bố cục và liên kết tab.

Chạy từ thư mục workspace bằng Python đã cài Playwright; máy cần Chrome và FFmpeg:

```powershell
.\.venv\Scripts\python.exe G9_MotoKey_3D/scripts/build_viewer.py
.\.venv\Scripts\python.exe G9_MotoKey_3D/ung_dung_tren_xe/build_simulation.py
.\.venv\Scripts\python.exe G9_MotoKey_3D/video/render_videos.py
.\.venv\Scripts\python.exe G9_MotoKey_3D/video/check_videos.py
```

Chỉ sửa nội dung/giao diện thì chạy `build_library.py`. Nếu sửa camera/chuyển động, xuất lại phim tương ứng, ví dụ `render_videos.py operation`. Báo cáo kiểm tra nằm ở `validation_video.json` và `render_report.json`.
