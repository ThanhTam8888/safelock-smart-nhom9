# SafeLock Smart — mô hình 3D của Nhóm 9

**Bản nâng cấp R04:** [Video cách vận hành có chú thích đồng bộ](video/Video_cach_van_hanh.html). Bốn video Full HD / 24 fps, 35 bước: lắp/tháo, cơ cấu bên trong, quên chìa và 14 tình huống. Bấm phát hoặc chọn bước để hiện ô giải thích; có tua, tạm dừng, phụ đề và toàn màn hình. Mô hình tương tác được bổ sung chất liệu, phản xạ và tư thế tay/chân. Nhấp đúp `MO_VIDEO_VAN_HANH.cmd` để mở. [Hướng dẫn R04](video/README.md).

**Giao diện mới 31/10/2026:** phong cách liquid glass; bấm chi tiết khóa để hiện chú thích bên cạnh ở cả trang khám phá và mô phỏng trên xe. Có tìm kiếm tình huống, tab thông tin và bố cục cho điện thoại. [Cách dùng và nguồn giao diện](ui/README.md).

**Bản mở rộng R02:** [Mô phỏng SafeLock trên cả xe máy và người dùng, 14 tình huống](ung_dung_tren_xe/Mo_phong_SafeLock_tren_xe_may.html). Có quên chìa, tác động mạnh, nhấc xe, mất nguồn/mạng, quên điện thoại và giới hạn theo dõi. Nhấp đúp `MO_MO_PHONG_TREN_XE.cmd` hoặc mở HTML bằng Chrome/Edge. [Hồ sơ và cách dùng](ung_dung_tren_xe/README.md).

**Bắt đầu:** mở [bản xem 3D](presentation/Mo_hinh_3D_SafeLock.html) bằng Chrome hoặc Edge. File tự chứa, chạy ngoại tuyến, không cần cài CAD. Có thể nhấp đúp `MO_MO_HINH_3D.cmd` trong thư mục này.

Thiết kế R01 ngày 26/10/2026 dựa trên `Báo-cáo-nhóm-9-KHKD.docx` và `Dự toán ngân sách - NHÓM 9.xlsx`. Sản phẩm trong tài liệu là khóa kẹp tay ga tích hợp GPS/4G, vì vậy mô hình là khóa tay ga – tay phanh. Hai tài liệu gốc không bị chỉnh sửa.

## Nên xem theo thứ tự

1. [Mô hình 3D tương tác](presentation/Mo_hinh_3D_SafeLock.html): Sản phẩm → Gắn trên xe → Tách lớp → Bên trong → Mở khóa. Kéo để xoay, cuộn để phóng to, bấm chi tiết để xem tên. Ở Tách lớp/Mở khóa, kéo thanh điều khiển để thay đổi mức tách hoặc tiến trình mở.
2. [Thư viện video có giải thích theo bước](video/Video_cach_van_hanh.html): 4 video tổng 3 phút 24 giây. [Video cấu tạo MP4](presentation/SafeLock_G9_giai_thich_3D.mp4) đã nâng cấp thành 28 giây, Full HD / 24 fps, không có lời đọc.
3. [Bảng trình bày 4 góc nhìn](presentation/SafeLock_G9_bang_trinh_bay.png): dùng để chèn slide.
4. [Thuyết minh PDF 13 trang](Thuyet_minh_SafeLock_G9.pdf), [Word chỉnh sửa](Thuyet_minh_SafeLock_G9.docx): cấu tạo, vận hành, chế tạo, pin, chi phí, việc cần kiểm chứng và bài trình bày khoảng 90 giây.
5. [Bản vẽ A3](CAD/Ban_ve_bo_tri_G9_A3.pdf), [CAD STEP](CAD/SafeLock_G9_R01.step), [GLB](CAD/SafeLock_G9_R01.glb), [BOM](CAD/BOM_chi_tiet.csv).

## Thiết kế đã dựng

- 50 chi tiết khóa và 6 chi tiết tay lái tham chiếu. Khung có hai má thép mỗi nửa, giằng, bản lề thép, tai khóa, hộp nhận và chốt. Đệm EPDM ngăn tiếp xúc cứng lên tay ga/tay phanh.
- Thân kẹp dài 120 mm, rộng 48 mm; bao ngoài khoảng 120 × 52 × 81 mm gồm đầu trục/mặt ruột khóa. Mẫu tay ga Ø34, định hướng đệm Ø30/32/34/36. Không khẳng định phù hợp mọi xe.
- Chốt Ø6 × 16 được rút 12 mm trước khi nửa trên mở quanh bản lề. Chìa cơ làm việc khi hết pin. Ruột khóa là bao hình mua hàng, chưa có thiết kế tumbler/cam bên trong được nhà cung cấp xác nhận.
- Cụm điện tử riêng: PCB, modem tùy chọn có GNSS, SIM, MCU, gia tốc, Hall, pin, sạc USB-C, gioăng và hai anten. Bao hình pin và linh kiện phải được xác nhận theo linh kiện mua thật.
- GPS nhận tọa độ, 4G gửi dữ liệu tới backend/app. Chưa triển khai mạch điện, firmware, backend hoặc app hoạt động. Hall nhận biết hai nửa áp sát; chưa xác nhận chốt khóa đã ăn hết.
- Anten nằm phía nhựa, phía trên khung; pin và bo mạch không nhận tải khóa cơ. Cần chốt ground plane, coax và đo RF.

## Kiểm tra đã thực hiện

- Các chi tiết CAD hợp lệ hình học; 6 cặp khe hở quan trọng không giao thể tích.
- Kiểm tra hai nửa ở 0°, 2°, 5°, 10°, 20°, 45°, 75°, chốt đã rút khi mở: không giao thể tích >0,1 mm³. Đây là lấy mẫu các góc, không chứng minh cả quỹ đạo liên tục hoặc dung sai thực tế.
- Bản HTML chạy ngoại tuyến, 5 chế độ, không lỗi JavaScript trong lượt kiểm tra; có kiểm tra bố cục desktop/mobile. Kết quả ở `research/cad_validation.json`, `motion_validation.json`, `viewer_validation.json`.
- Hình và video được dựng từ lưới CAD, không phải ảnh AI thay thế mô hình.

## Phần cần làm trước sản xuất

Đo và chọn xe mẫu; chốt ruột khóa/chốt mua được; hoàn thiện liên kết hàn và gá khay/PCB, dung sai, gioăng, chặn mở, dây/đầu nối và mạch điện. Làm prototype rồi thử lực giữ, độ bền, RF, pin, kín nước và khả năng thao tác trên xe. Chưa có kết quả FEA hay thử nghiệm vật lý, chưa có chứng nhận IP/chống phá. Giá và thời lượng pin trong báo cáo là giả định, không phải cam kết.

GPS tích hợp chỉ hỗ trợ theo dõi xe khi khóa còn gắn trên xe. Khi tháo khóa mang theo, thiết bị theo dõi vị trí chiếc khóa. Khóa phải tháo hoàn toàn trước khi chạy; kiểm tra phanh nhả và tay ga hồi tự do.

## Đơn vị và phần mềm

- **STEP, STL: mm.** STEP giữ các chi tiết rời, mở bằng FreeCAD/Fusion/phần mềm CAD hỗ trợ STEP.
- **GLB: mét**, theo quy ước glTF. Chẳng hạn chiều dài thân 120 mm tương ứng 0,12 m.
- `STL/` có từng chi tiết; `CAD/SafeLock_G9_lap_rap.stl` là lưới lắp ráp tham khảo, có tiếp xúc/liên kết hàn, không phải một khối đã union để in. STL dùng thử hình dáng; bộ phận chịu lực thật cần làm bằng vật liệu và công nghệ thích hợp.
- Thư viện xem Three.js r128 sử dụng giấy phép MIT, kèm ở `presentation/vendor/LICENSE_three.txt`. Toàn bộ thư viện và lưới đã nhúng vào HTML.

## Dựng lại từ mã nguồn

Môi trường đã sử dụng: Python 3.12, CadQuery 2.8.0. Cài thư viện theo `requirements-model.txt` trong môi trường riêng. Mã đọc hai tài liệu gốc nằm ở `scripts/read_sources.py`; đường dẫn cần đổi nếu chuyển sang máy khác. Bản báo cáo và render đã có sẵn nên không bắt buộc chạy lại.

```powershell
python scripts/check_motion.py
python scripts/build_viewer.py
python scripts/make_drawings.py
python scripts/render_assets.py
python scripts/make_report.py
python scripts/check_viewer.py
python scripts/validate_delivery.py
```

`check_motion.py` đồng thời dựng lại CAD và xuất lưới. `render_assets.py` và `check_viewer.py` hiện dùng Chrome/FFmpeg ở đường dẫn Windows của máy tạo hồ sơ; chỉnh đường dẫn khi chuyển máy. Các module hình học, điện tử và giá mua được trình bày rõ phạm vi trong thuyết minh.
