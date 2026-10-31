SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 01

# SafeLock trong đời sống:
điều gì xảy ra khi người dùng rời xe?

Mô hình 3D toàn xe tay ga, người sử dụng, chìa khóa và điện thoại, kết hợp 14 tình huống để giải thích lợi ích, điều kiện hoạt động và giới hạn thực tế của đề tài.

![Cảnh 3D](anh/00_xe_may_va_safelock.png)

Xe là thiết kế tham chiếu, không sao chép một mẫu thương mại cụ thể. SafeLock dùng lại 50 chi tiết CAD R01, đặt theo tỷ lệ mét thật trên tay ga phải.

| Có trong trải nghiệm | Ý nghĩa khi trình bày |
| 14 kịch bản, mỗi kịch bản 4 bước | Người xem thấy tác nhân → sự kiện → phản hồi → giới hạn. |
| So sánh R01 và R02 | R01 là chức năng dự kiến của thiết kế GPS/4G; R02 thêm BLE/còi/app, chưa có trong BOM R01. |
| Đổi điều kiện điện, mạng, GNSS | Không hiển thị như đã gửi được cảnh báo khi không có đường truyền. |
| Xem gần, tua thời gian, quay 3D | Dùng để thuyết trình, thảo luận yêu cầu và chuẩn bị thử nghiệm. |

Phạm vi: mô phỏng hành vi bằng quy tắc được lập trình cho từng kịch bản. Không kết nối xe thật, không lấy GPS/Bluetooth thật, không phải app hoặc phần cứng đã hoạt động. Thời gian, rung và liên lạc trong cảnh đều được rút gọn/giả lập.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 02

# Ma trận 14 tình huống

| # | Tình huống | Phản hồi và điều kiện chính | Mốc |
| 1 | Đỗ đúng quy trình | Giữ cơ khí + giám sát sau khi lắp bằng tay. | R01 |
| 2 | Quên chìa xe | R02 nhắc kiểm tra chung khi điện thoại đi cùng người. | R02 |
| 3 | Quên chìa trên SafeLock | Nhắc kiểm tra chung; không suy ra vị trí chìa từ Hall. | R02 |
| 4 | Quên gắn khóa, còn trong cốp | Cần bật Chế độ đỗ và nhận trạng thái phù hợp. | R02 |
| 5 | Rung nhẹ, đơn lẻ | Minh họa lọc; không gửi cảnh báo khẩn trong ví dụ. | R01 |
| 6 | Tác động mạnh, cố dắt | Cơ khí tạo trở ngại; gửi rung nếu còn điện/mạng. | R01 |
| 7 | Nhấc cả xe | Khóa phanh không neo xe; theo dõi có điều kiện. | R01 |
| 8 | Mất 4G rồi phục hồi | Lưu cục bộ; đồng bộ muộn với hai thời điểm. | R01* |
| 9 | Hầm mất GNSS, còn 4G | Báo rung với vị trí cuối, không tạo tọa độ giả. | R01 |
| 10 | Pin cạn | Cơ khí vẫn giữ; không có dữ liệu điện tử mới. | R01 |
| 11 | Chuẩn bị đi, chưa tháo khóa | Nhắc sau thao tác Chuẩn bị đi; vẫn tháo bằng chìa. | R02 |
| 12 | Khóa bị tách khỏi xe | Điểm GPS nằm lại với khóa; xe không được theo dõi tiếp. | R01 |
| 13 | Điện thoại cũng để lại | BLE không mất kết nối; không biết người đã đi. | Giới hạn |
| 14 | Dắt xe hợp lệ | Xác nhận kết thúc đỗ, mở cơ khí, tháo khóa rồi di chuyển. | R01* |

* Bộ đệm bền, đồng hồ sự kiện, backend, xác thực và luồng app đều cần được triển khai. R01 hiện là hồ sơ CAD và kiến trúc đề xuất, không có firmware/app được thử nghiệm. R02 là nhánh tính năng mới để thảo luận, chưa được tích hợp thành phần cứng.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 03

# Quên chìa: nhắc thế nào cho hợp lý?

![Cảnh 3D](anh/02_ignition_key_canh_3D.png)

Kịch bản chính: chủ xe gắn SafeLock nhưng để chìa xe trong ổ, mang điện thoại đi. Sau một khoảng trễ giả lập khi BLE suy yếu/mất liên lạc, app R02 nhắc: “Hãy kiểm tra chìa xe, rút chìa khóa cơ và kiểm tra đã gắn khóa”. Người mô hình quay lại kiểm tra.

| Cấp nhận biết | Điều có thể nói |
| Khóa R01 GPS/4G | Không biết chìa còn trong ổ; định vị chiếc khóa không xác định sự hiện diện của người/chìa. |
| Bổ sung BLE + app R02 | Có thể thiết kế nhắc kiểm tra khi điện thoại tách khỏi khóa, với điều kiện quyền nền và ghép đôi phù hợp. Đây là nhắc chung. |
| Muốn nói riêng “quên chìa” | Cần thẻ BLE trên chùm chìa và logic phù hợp hoặc cảm biến ổ chìa; phải thiết kế, cấp nguồn, thử trên xe và xử lý việc tháo/thay chìa. |

Cùng nguyên tắc áp dụng khi quên chìa khóa cơ trên SafeLock. Hall chỉ đo hai nửa áp sát; không nhận ra chìa còn cắm. Nếu quên gắn khóa trong cốp, chỉ nhắc trong ví dụ đã chủ động bật Chế độ đỗ và khóa còn mở; khóa đóng rời trong túi vẫn là trường hợp khó phân biệt.

Không dùng RSSI như thước đo mét. Cảnh không triển khai thuật toán BLE thật; mốc nhắc phụ thuộc tiến trình kịch bản. Thực tế cần lọc nhiễu, trễ, chống nhắc dồn, quyền chạy nền, màn hình khóa và tiết kiệm pin.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 04

# Bảo vệ cơ khí và theo dõi là hai lớp khác nhau

![Cảnh 3D](anh/07_lift_canh_3D.png)

| Tác động | Cơ khí | Điện tử và giới hạn |
| Cố dắt/rung lặp lại | Giữ tay phanh tạo trở ngại; cần thử lực giữ và trượt. | Gia tốc có thể phát hiện rung; không nhận diện ý định hoặc danh tính. |
| Nhấc cả xe | Không có điểm neo đất, nên vẫn có thể bị di chuyển cả khối. | GNSS/4G theo dõi khi khóa còn trên xe, có điện và có tín hiệu. |
| Khóa bị tách khỏi xe | Cảnh bỏ qua thao tác tháo/phá; không dựng cách vượt khóa. | GPS xác định chiếc khóa. Xe đi còn khóa nằm lại thì không thể tiếp tục theo dõi xe bằng thiết bị đó. |

Lớp định vị không thay thế khóa, và khóa tay phanh không thay thế điểm neo. Nếu nhóm muốn theo dõi ngay cả khi khóa bị tách ra, hướng phát triển là tracker ẩn độc lập trên xe. Đây là một kiến trúc khác, cần thêm chi phí, lắp đặt và kế hoạch nguồn riêng.

Vòng màu trong cảnh là dấu hiệu trực quan của sự kiện, không phải khẳng định R01 có còi. Còi chỉ được giả lập ở R02 khi còn nguồn; không tác động vào đánh lửa, không cắt động cơ và không tự siết phanh.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 05

# Mất mạng, mất GPS, hết pin: giao diện phải nói thật

| Trạng thái thực của thiết bị | Giao diện / phản hồi hợp lý |
| Có nguồn, GNSS, 4G | Nhận sự kiện và vị trí theo chu kỳ đã chốt, kèm thời điểm. Không định vị từng khung hình như video. |
| Có nguồn + GNSS, mất 4G | Ghi sự kiện cục bộ; điện thoại chỉ có dữ liệu lần liên lạc trước. Khi mạng về, gửi kèm lúc phát sinh và lúc nhận. |
| Có nguồn + 4G, mất GNSS | Vẫn gửi được sự kiện rung. Hiển thị Vị trí cuối và tuổi dữ liệu; không tạo fix mới trong hầm. |
| Pin thấp nhưng còn gửi được | Nhắc sạc trước khi tắt; số phần trăm trong mô hình chỉ là ví dụ. |
| Đã mất nguồn | Không có GNSS/4G/BLE/còi. App chỉ biết pin cuối đã nhận và lần liên lạc cuối, không biết chính xác nguyên nhân im lặng. |
| Cả điện thoại và khóa ở lại xe | Liên kết BLE vẫn gần; không thể suy ra con người đã rời xe từ hai thiết bị này. |

![Cảnh 3D](anh/13_phone_left_canh_3D.png)

Việc không cảnh báo ở tình huống để quên điện thoại là một kết quả cần trình bày. Muốn cải thiện phải có thứ đi cùng người, ví dụ thiết bị đeo/thẻ phù hợp, hoặc bước xác nhận khác. Không nên phát minh một cảnh báo không có dữ liệu đầu vào.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 06

# Cần bổ sung gì để biến R02 thành prototype?

| Hạng mục | Công việc cần làm |
| Phần cứng BLE | Chọn MCU có BLE hoặc module phù hợp, anten/keep-out RF, mạch nguồn và kiểm thử tương thích điện thoại. Không gắn nhãn BLE cho module GPS/4G vốn chưa được xác nhận có chức năng này. |
| Còi tại khóa | Buzzer + driver, đường âm và mức tiêu thụ; thiết kế lại vỏ/vent âm và kiểm tra độ kín. Không công bố độ lớn âm khi chưa đo. |
| Firmware | Máy trạng thái đỗ, Hall, gia tốc, lọc rung, lưu sự kiện, ID chống trùng, thời gian, gửi lại, giới hạn gửi và ngủ/thức. |
| App | Ghép đôi có xác thực; chế độ đỗ chủ động; thông báo nền; nhắc chung; chuẩn bị đi; trạng thái cũ; tắt nhắc có xác nhận. |
| Quên chìa chính xác | Nghiên cứu thẻ BLE hoặc cảm biến chìa. Cần thêm logic để phân biệt rời xe, chìa để lại, hết pin thẻ, chia sẻ chìa và mất liên lạc. |
| Cảm biến chốt / gắn trên xe | Hall hai nửa không thay cho cảm biến chốt. Nếu cần khẳng định chốt ăn hoặc khóa đang kẹp lên xe, phải bổ sung cách đo phù hợp. |
| Chi phí và thời lượng | Cập nhật BOM, pin, PCBA, RF, ứng dụng, backend và báo giá. Các mục tiêu giá/pin R01 không mặc nhiên giữ nguyên cho R02. |

Thứ tự đề xuất: (1) Chốt khóa cơ trên một xe mẫu; (2) chạy rung + GNSS/4G trên bench; (3) thêm BLE nhắc chung; (4) thử nghiệm việc phát hiện chìa với cảm biến/thẻ; (5) đo pin, RF, kín nước và chi phí. Không ghép tất cả lời hứa vào MVP trước khi từng phần có bằng chứng.

BLE ở gần không đủ để tự mở khóa hoặc tự ngắt giám sát. Luồng hợp lệ trong mô phỏng luôn có xác nhận của người dùng và thao tác chìa cơ. Mô phỏng không chứa cơ chế xác thực thật; đây là yêu cầu cần triển khai.


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 07

# Dùng mô hình để làm đề tài mạnh hơn

| Nhóm kiểm chứng | Việc cần đo trên prototype, chưa phải kết quả |
| Nhắc rời xa | Điện thoại trong túi, qua tường, màn hình tắt, quyền nền bị chặn, Bluetooth tắt; ghi tỷ lệ nhắc đúng/sai và độ trễ. |
| Quên chìa | Phân biệt nhắc kiểm tra chung với cảm biến chìa thật. Thử chìa ở xe/ở túi, người mang/không mang điện thoại, thẻ hết pin. |
| Cảnh báo rung | Rung nền, mưa, chạm nhẹ, dắt hợp lệ, tác động lặp lại; ghi ma trận nhầm lẫn và số thông báo gây phiền. |
| Dữ liệu khi gián đoạn | Mất 4G, không có GNSS, thiết bị reset; kiểm tra dấu thời gian, sự kiện trùng, dung lượng bộ đệm và tuổi vị trí. |
| Cơ khí và thao tác | Đệm vừa, chốt vào đủ, trượt ngang, phanh/ga trở lại bình thường sau tháo. Không thử cưỡi xe khi khóa còn gắn. |
| Khả dụng | Cho người dùng thử đỗ/lấy xe với mẫu hình dáng; đo thời gian thao tác và lỗi quên bước. Không coi video đẹp là bằng chứng thị trường. |

Bài trình bày khoảng 3 phút: 30 giây xem cả xe và thao tác đỗ; 45 giây mở tình huống quên chìa, chuyển R01 ↔ R02 để thấy phần cần bổ sung; 35 giây tác động mạnh và mất 4G; 30 giây xem xe bị nhấc/khóa bị tách; 20 giây kết luận kế hoạch làm mẫu và tiêu chí kiểm chứng.

Câu trả lời ngắn với thầy: “Nhóm đã tách rõ ba việc: khóa cơ tạo trở ngại, định vị/cảnh báo hỗ trợ từ xa, và nhắc hành vi cần BLE/cảm biến thêm. Nhóm không khẳng định chiếc khóa biết mọi tình huống. Mỗi tình huống có đầu vào, phản hồi có điều kiện và một phép thử để kiểm chứng.”


---

SAFELOCK SMART / G9 / ỨNG DỤNG TRÊN XE / R02 · 08

# Bàn giao và giới hạn của phép mô phỏng

| File | Cách dùng |
| Mo_phong_SafeLock_tren_xe_may.html | Mở bằng Chrome/Edge. 14 tình huống, 4 bước mỗi tình huống, thanh thời gian, xem gần và so sánh R01/R02. Chạy ngoại tuyến. |
| SafeLock_14_tinh_huong_tren_xe.mp4 | Video khoảng 70 giây từ cùng mô hình và quy tắc; có chú thích tiếng Việt, không có lời đọc. |
| Xe_may_va_SafeLock_R02.glb | Mô hình toàn xe + khóa + người ở tư thế tham chiếu, đơn vị mét. GLB là cảnh tĩnh; chuyển động/tình huống chạy trong HTML. |
| Tong_quan_ung_dung_SafeLock.png | Bảng trình bày để chèn slide. |
| scenarios.json / simulation.js | Nội dung 14 kịch bản và bộ quy tắc mô phỏng, không phải thuật toán đọc cảm biến thật. |
| kiem_tra_mo_phong.json | Kết quả kiểm tra giao diện, ranh giới khả năng, mất nguồn/mạng và không gọi dịch vụ mạng ngoài. |

Đã kiểm tra 14 tình huống, thao tác chọn/phát/tua/xem gần, bố cục điện thoại, R01 không nhắc BLE, R02 có điều kiện, mất nguồn không có còi, không có mạng không gửi được sự kiện và GNSS mất fix không tạo vị trí mới. Những kiểm tra này chứng minh phần mềm mô phỏng nhất quán với quy tắc đã viết; không xác nhận hành vi phần cứng ngoài đời.

Mô hình dùng lại dữ liệu CAD R01 của khóa và thư viện Three.js MIT trong hồ sơ trước. Không thay thế CAD gia công mới cho các tính năng R02; chưa bổ sung BLE/còi vào bản vẽ mạch hay thử RF, pin, nước hoặc độ bền.

Tham khảo kỹ thuật sơ cấp: Bluetooth SIG — Core 6.0 feature overview về RSSI và giới hạn suy khoảng cách; Android — Communicate in the background về BLE nền; Apple — Core Bluetooth và hướng dẫn xử lý nền. Các ràng buộc nền phụ thuộc phiên bản hệ điều hành và cấu hình; cần thử trên thiết bị mục tiêu. Truy cập phục vụ hồ sơ 26/10/2026.
