# Giao diện Liquid Glass — 31/10/2026

**Cập nhật R04:** cả hai trang có thêm tab [Video cách vận hành](../video/Video_cach_van_hanh.html). Nguồn `realism.js` bổ sung chất liệu, phản xạ và người có khớp; `nav.py`/`video-nav.css` đồng bộ ba tab trên desktop/điện thoại. Hướng dẫn và kiểm tra video nằm trong [video/README.md](../video/README.md).

Mở [Khám phá cấu tạo](../presentation/Mo_hinh_3D_SafeLock.html) hoặc [14 tình huống](../ung_dung_tren_xe/Mo_phong_SafeLock_tren_xe_may.html) bằng Chrome/Edge. Hai file vẫn tự chứa và chạy ngoại tuyến.

Thay đổi giao diện:

- Bố cục ưu tiên khung 3D; nền sáng, kính mờ, bóng nhẹ và các nhóm điều khiển nhất quán.
- Bấm chi tiết khóa để hiện **thẻ chú thích hình chữ nhật bên cạnh**: tên, công dụng, thông số và tên chi tiết thực. Đường nối bám theo vị trí được chọn khi xoay hoặc mở bản lề.
- Bấm ×, nhấn Esc hoặc bấm vùng trống để đóng. Kéo xoay không bị hiểu thành bấm chọn.
- Trang xe máy hỗ trợ chọn chi tiết ở cả khung chính lẫn góc cận; tạm dừng tình huống khi chọn để có thể đọc.
- Có tìm kiếm tiếng Việt không dấu, lọc nhóm và tab **Điện thoại / Giải thích**; có thể thu gọn cột tình huống.
- Trên điện thoại/máy tính bảng, danh sách tình huống mở thành bảng chọn; camera tự điều chỉnh theo màn hình dọc. Có hỗ trợ thao tác chạm, bàn phím và giảm chuyển động.
- Chỉ cập nhật nội dung DOM khi giá trị thay đổi, tránh phát lại thông báo truy cập và cập nhật thừa mỗi khung hình.

Nguồn giao diện dùng chung nằm trong thư mục `ui/`:

- `explore.html`, `simulation.html`: hai bố cục mới; các template cũ được giữ lại để tham khảo.
- `liquid-glass.css`, `readability.css`: hệ thống kính và độ tương phản chữ.
- `component_inspector.js`: chọn lưới 3D, làm nổi chi tiết và đặt chú thích bám vị trí.
- `simulation-ui.js`: chọn chi tiết trên xe, tab thông tin và bảng tình huống trên thiết bị nhỏ.
- `presentation/viewer.js`: logic trình chiếu khóa, được tách khỏi template cũ.

Dựng lại file HTML từ thư mục dự án:

```powershell
.\.venv\Scripts\python.exe G9_MotoKey_3D/scripts/build_viewer.py
.\.venv\Scripts\python.exe G9_MotoKey_3D/ung_dung_tren_xe/build_simulation.py
.\.venv\Scripts\python.exe G9_MotoKey_3D/ui/check_glass_ui.py
```

Kiểm tra dùng Chrome/Playwright và không gọi mạng ngoài. Kết quả lưu ở `validation_glass_ui.json`, hình xem trước ở `previews/`. Nguồn giao diện trước khi chỉnh được lưu tại `research/ui_before_20261031.zip`.

Giao diện liquid glass và bộ chọn chi tiết được xây ở R03, tiếp tục dùng trong R04. Thiết kế cơ khí R01, 50 chi tiết CAD và nội dung 14 tình huống R02 được giữ nguyên về chức năng; các giới hạn của mô phỏng vẫn áp dụng. Video đã được xuất lại ở R04; PDF/Word là tài liệu thiết kế R01/R02.
