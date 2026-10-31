# SafeLock trên xe máy — 14 tình huống

**R04:** bổ sung vật liệu/phản xạ, thân xe mượt hơn, người tham chiếu có khớp và bàn tay khi lắp khóa. Tab [Video cách vận hành](../video/Video_cach_van_hanh.html) có 4 video và ô giải thích đồng bộ theo bước. GLB toàn xe cũng đã xuất lại với hình học mới của xe/người; hình học CAD của khóa giữ nguyên.

Mở **[Mo_phong_SafeLock_tren_xe_may.html](Mo_phong_SafeLock_tren_xe_may.html)** bằng Chrome/Edge. HTML tự chứa, chạy ngoại tuyến. Chọn tình huống bên trái, bấm Phát hoặc kéo thời gian. Có góc cận chìa/khóa/điện thoại, xem toàn cảnh và tự xoay camera. Âm minh họa còi mặc định tắt.

Chuyển **R01 ↔ R02** để so sánh thiết kế GPS/4G hiện tại với đề xuất bổ sung BLE/còi/app. Mở “Thay đổi điều kiện mô phỏng” để tắt nguồn, 4G hoặc GNSS. Các điều kiện điều khiển bộ quy tắc của cảnh, không điều khiển thiết bị thật.

14 tình huống gồm: đỗ đúng quy trình; quên chìa xe; quên chìa SafeLock; quên gắn khóa; rung nhẹ; tác động mạnh/cố dắt; nhấc cả xe; mất 4G và có mạng lại; mất fix GPS trong hầm; pin cạn; chuẩn bị đi chưa tháo khóa; khóa bị tách khỏi xe; để quên cả điện thoại; mở khóa/dắt xe hợp lệ.

**Điểm kỹ thuật cần nói đúng:**

- R01 là mô hình CAD/kiến trúc, chưa phải phần cứng hay app vận hành được. R02 là đề xuất bổ sung, chưa đưa vào PCB/BOM sản xuất.
- BLE/app có thể được thiết kế để nhắc kiểm tra chung khi điện thoại rời khóa; không tự nhận biết chìa còn trong ổ. Muốn báo cụ thể cần thẻ/cảm biến phù hợp.
- Hall hai nửa áp sát không chứng minh chốt đã ăn hoặc thiết bị đang gắn lên xe. Không tự mở khóa, tự khóa phanh hoặc cắt động cơ.
- Hết pin không có GNSS/4G/BLE/còi. App chỉ có dữ liệu lần nhận cuối. Mất 4G không thể hiển thị như đã nhận cảnh báo tức thì.
- Khóa rời khỏi xe thì GPS theo chiếc khóa; điện thoại cùng để lại thì BLE không biết người đã đi.
- Khoảng cách, rung, thời gian, vị trí và thông báo trong cảnh đều giả lập. Các bài kiểm tra xác nhận tính nhất quán của mô phỏng, không phải thử nghiệm chống trộm ngoài đời.

Các file kèm:

- [Video 14 tình huống](SafeLock_14_tinh_huong_tren_xe.mp4), 84 giây, Full HD / 24 fps, không có lời đọc. Mở trong tab video để xem thêm chú thích tương tác.
- [Hồ sơ PDF](Ho_so_14_tinh_huong_SafeLock.pdf), [Word chỉnh sửa](Ho_so_14_tinh_huong_SafeLock.docx).
- [Mô hình GLB toàn xe](Xe_may_va_SafeLock_R02.glb), đơn vị mét. GLB là cảnh tĩnh; animation chạy trong HTML.
- [Bảng trình bày](Tong_quan_ung_dung_SafeLock.png); ảnh từng tình huống trong `anh/`.
- Mã nguồn dựng xe/người: `scene_builder.js`; bộ quy tắc: `simulation.js`; nội dung: `scenarios.json`.
- `kiem_tra_mo_phong.json` ghi kết quả kiểm tra giao diện và các điều kiện nguồn/mạng/quyền tính năng.

Không cần cài Python để mở HTML/video. Để dựng lại trong môi trường dự án, chạy `build_simulation.py`, `check_simulation.py`, `export_vehicle.py`, `render_simulation.py`, `make_scenario_report.py`; các script kiểm tra/render dùng Chrome và FFmpeg ở đường dẫn Windows của máy tạo hồ sơ.
