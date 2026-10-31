SAFELOCK SMART / NHÓM 9 / R01 · 01

# Một chiếc khóa có thể hình dung,
có cơ sở để làm mẫu.

# SAFELOCK SMART

Khóa kẹp tay ga – tay phanh tích hợp GNSS/GPS và 4G. Hồ sơ thiết kế 3D đề xuất cho dự án Nhóm 9, xây dựng từ báo cáo kinh doanh và bảng dự toán được cung cấp.

![Hình CAD](presentation/G9_product_render.png)

| Hình thức | Bản chất mô hình |
| 120 × khoảng 52 × 81 mm | Bao ngoài CAD; rộng thân kẹp 48 mm. |
| 50 chi tiết khóa + 6 chi tiết tham chiếu | STEP có chi tiết rời; GLB để trình chiếu; STL cho mẫu hình dáng. |
| Khóa cơ bằng chìa; GPS + SIM/4G | Đã dựng cấu tạo và chuyển động mô phỏng. Chưa có mẫu vật lý. |

Phạm vi: đây là thiết kế kỹ thuật sơ bộ R01 để trình bày và bắt đầu làm prototype. Hồ sơ chưa thay thế thiết kế ruột khóa của nhà cung cấp, mạch điện, firmware, bộ khuôn hoặc kết quả thử nghiệm sản phẩm.


---

SAFELOCK SMART / NHÓM 9 / R01 · 02

# Bám sát tài liệu, làm rõ điều còn thiếu

Trong hai tài liệu, sản phẩm được chọn là khóa tay ga chống trộm tích hợp định vị SafeLock Smart. Vì vậy, mô hình được phát triển thành khóa kẹp tay ga và giữ tay phanh; không phải một móc treo chìa khóa nhỏ.

| Nội dung trong tài liệu | Quyết định thiết kế R01 |
| Khóa tay ga, nhỏ gọn, thao tác nhanh | Cấu trúc hai nửa mở bản lề, ôm tay ga và giữ tay phanh đã bóp. |
| Định vị, cảnh báo rung, kết nối điện thoại | GNSS + LTE Cat 1bis, SIM, MCU và cảm biến gia tốc; không giả định Bluetooth truyền được đi xa. |
| Không cắt dây điện xe | Pin 1S riêng; USB-C 5 V; không điều khiển hệ thống đánh lửa/phanh của xe. |
| Vỏ ABS và càng cơ khí trong dự toán | Giữ vỏ nhựa cho khoang điện tử; đề xuất vỏ cơ khí PA6-GF30 và lõi thép. Đây là thay đổi cần báo giá lại. |
| Dễ dùng, có khả năng điều chỉnh | Bộ đệm theo cỡ tay ga; đệm tay phanh có thể thay. Không tuyên bố dùng được mọi xe. |

## Vì sao cần giữ tay phanh?

Một vòng kẹp chỉ bám lên tay ga có thể xoay cùng tay ga. Điểm giữ ở tay phanh tạo ràng buộc cơ học và duy trì phanh trước ở vị trí đã bóp. Mức giữ, độ trượt ngang và lực ép phải xác nhận trên xe thật; đây là lớp bảo vệ bổ sung, không chống trộm tuyệt đối.

![Hình CAD](presentation/G9_mounted_render.png)

Tay lái trong hình là bao hình tham chiếu: tay ga Ø34, tâm rãnh phanh cách tâm tay ga 54 mm; không đại diện riêng cho một hãng xe.


---

SAFELOCK SMART / NHÓM 9 / R01 · 03

# Kích thước và vị trí lắp

![Hình CAD](presentation/G9_ban_ve_ky_thuat.png)

Bản A3 riêng nằm tại CAD/Ban_ve_bo_tri_G9_A3.pdf. File STEP là nguồn kích thước khi phát triển tiếp.

| Hạng mục | Kích thước / lựa chọn thiết kế |
| Thân kẹp / bao ngoài | Thân: dài 120, rộng 48. Bao cả đầu trục và mặt ổ khoảng 120 × 52 × 81 mm. |
| Bore và đệm tay ga | Bore cứng Ø40,6; đệm mẫu lòng Ø34, ngoài Ø40. Dự kiến cỡ lòng Ø30/32/34/36. |
| Rãnh tay phanh | Bore cứng 20 × 16; đệm mẫu còn passage 12 × 8; khoảng cách tâm 54. |
| Bản lề / chốt khóa | Trục Ø6; lỗ Ø6,3. Chốt khóa Ø6 × 16, hành trình rút 12; lỗ tai Ø6,6. |
| Khoang điện tử | Nắp 80 × 44; PCB 60 × 32 × 1,6; pin bao hình 60 × 30 × 8. |

Kích thước trên là giả định thiết kế mới, không phải số đo có sẵn trong báo cáo. Cần đo đường kính tay ga, tiết diện và hành trình tay phanh, vị trí gù, cùm công tắc, dây cáp và khoảng hở nhựa đầu xe. Đệm phải ép vừa, không dùng lực siết để bù sai hình học.


---

SAFELOCK SMART / NHÓM 9 / R01 · 04

# Cơ cấu chịu lực được tạo ra thế nào?

![Hình CAD](presentation/G9_exploded_render.png)

Tách lớp từ chính lưới CAD, không phải ảnh minh họa AI. Các chi tiết được dịch ra xa để dễ đọc cấu tạo.

| Cụm | Cấu tạo và vai trò |
| Khung trên và dưới | Mỗi nửa có hai má thép 40Cr dày 3 mm; giằng ngang nối hai má. Hai khung gắn qua bản lề thép. |
| Bản lề | Cối giữa của nửa trên, hai cối ngoài của nửa dưới, trục Ø6 và đầu tán. Gân thép nối cối trên vào giằng. |
| Khóa chốt | Tai thép có lỗ kín Ø6,6 đi vào hộp dẫn hướng; chốt Ø6 xuyên lỗ và có gối đỡ hai phía. Ruột khóa điều khiển rút chốt. |
| Vỏ và đệm | Vỏ giữ vị trí, bảo vệ bề mặt; đệm EPDM bám tay ga, đỡ tay phanh. Không giao chức năng chịu cắt chính cho nhựa. |
| Khoang điện tử | Khay, nắp, gioăng và PCB được bố trí phía trên; không dùng pin hoặc bo mạch như một phần của khung chịu lực. |

Đường truyền lực đề xuất: tay ga/tay phanh → đệm → hai má thép → giằng và tai khóa → chốt/hộp nhận hoặc cối bản lề → khung đối diện. Liên kết hàn/gia công của khung phải được hoàn thiện thành bản vẽ xưởng trước sản xuất.


---

SAFELOCK SMART / NHÓM 9 / R01 · 05

# Khóa, mở và tránh kẹt cơ khí

![Hình CAD](presentation/G9_open_render.png)

Nửa trên mở quanh trục X tại Y = −53, Z = 0. Góc 75° là góc minh họa, không phải giới hạn đã thử nghiệm.

## Trình tự chuyển động

1. Hai nửa áp sát, tai khóa đi vào hộp dẫn hướng. 2. Chốt xuyên lỗ kín trên tai, ăn vào gối nhận. 3. Khi mở, xoay chìa để cơ cấu trong ruột khóa rút chốt 12 mm. 4. Sau khi chốt đã ra khỏi tai, mới nâng nửa trên quanh bản lề.

Miệng hộp nhận được nới theo quỹ đạo cung của tai khi mở. Phần nhựa phía sau nửa trên dừng ở trục bản lề để tránh quét vào nửa dưới. Các mẫu kiểm tra số ở 0°, 2°, 5°, 10°, 20°, 45°, 75° không ghi nhận giao thể tích giữa hai nửa trên ngưỡng 0,1 mm³, khi chốt ở trạng thái rút.

## Điểm cần chốt với nhà cung cấp

Ruột khóa Ø14 × 14 trong mô hình là bao hình dự kiến. Phải chọn hoặc đặt cụm có hành trình chốt 12 mm, phương án giữ chìa, liên kết cam, chống xoay và khả năng chịu lực phù hợp. Mô hình chưa dựng bi/tumbler hoặc truyền động bên trong; không được đem bao hình này đặt hàng như một mã khóa đã xác nhận.

Hall nhận biết hai nửa áp sát, không chứng minh chốt đã ăn hết. R01 dùng chìa để quản lý khóa cơ; app chỉ hiển thị trạng thái cảm biến. Nếu muốn báo “đã khóa chốt”, cần bổ sung cảm biến hành trình chốt riêng.


---

SAFELOCK SMART / NHÓM 9 / R01 · 06

# Điện tử và đường truyền vị trí

![Hình CAD](presentation/G9_inside_render.png)

Chế độ bên trong ẩn vỏ ngoài để thấy bố trí khung, PCB, pin và anten.

| Khối | Chức năng và ràng buộc |
| GNSS / GPS | Lấy tọa độ vệ tinh. SIM7670G có bao hình hãng 24 × 24 × 2,4 mm; phải chọn đúng biến thể có GNSS. Không phải mọi SKU đều có. |
| 4G và nano-SIM | Gửi sự kiện/tọa độ qua mạng di động tới backend rồi điện thoại. Chọn băng tần và xác nhận hoạt động với SIM/nhà mạng thực tế. |
| MCU + gia tốc + Hall | MCU quản lý ngủ/thức. Gia tốc đánh thức khi rung. Hall nhận hai nửa áp sát; nam châm đặt nửa dưới. Dây Hall đi hoàn toàn trong nửa trên. |
| Pin + sạc + nguồn | Li-Po 1S có bảo vệ và NTC; USB-C 5 V. Mục tiêu cell khoảng 1.500 mAh trong bao hình đã dành, phải xác nhận cell mua được. |
| Anten và che chắn | Patch GNSS 18 × 18 × 4 trên ground plane riêng; LTE FPC dọc thành nhựa. Hai bao hình cần chọn linh kiện, đi coax và đo RF thực tế. |

Luồng dữ liệu: rung → MCU lọc/đánh thức → GNSS lấy vị trí nếu có tín hiệu → modem 4G/SIM → backend có xác thực → app thông báo. Mất GNSS: gửi vị trí cuối kèm thời điểm và trạng thái. Mất mạng: lưu sự kiện, gửi lại khi kết nối phục hồi. Không giả lập “tọa độ mới” khi chưa có fix.


---

SAFELOCK SMART / NHÓM 9 / R01 · 07

# Nguồn pin: tính bằng giả định minh bạch

Dung lượng khoảng 1.500 mAh là mục tiêu lựa chọn cell, chưa phải số đo. Với tỷ lệ sử dụng 80% giả định, lượng điện để tính sơ bộ là 1.200 mAh. Thời lượng ≈ 1.200 / dòng trung bình; chưa tính nhiệt độ, lão hóa và điều kiện sóng.

| Dòng trung bình giả định | Kết quả phép tính | Ý nghĩa |
| 1,5 mA | 800 giờ ≈ 33 ngày | Chỉ là kịch bản ngủ sâu tốt, ít gửi. |
| 5 mA | 240 giờ = 10 ngày | Kịch bản tiêu thụ tăng do kết nối và cập nhật. |
| 25 mA | 48 giờ = 2 ngày | Theo dõi thường xuyên hơn. |
| 80 mA | 15 giờ | Ví dụ hoạt động nặng; không quảng cáo định vị liên tục một tháng. |

## Kiến trúc nguồn phải được làm đúng

USB-C 5 V → bảo vệ đầu vào và bộ sạc 1S có NTC/power-path → nguồn hệ thống → buck-boost khoảng 3,8 V đủ dòng xung modem; nhánh nguồn riêng cho MCU/cảm biến. Ví dụ BQ24074 có power-path, nhưng OUT danh định 4,4 V không được nối thẳng vào modem có dải cấp 3,4–4,2 V.

Cổng Type-C cần điện trở CC phù hợp, ESD và giới hạn dòng; pin có bảo vệ quá sạc/quá xả/ngắn mạch. Chừa thể tích cho mạch bảo vệ, dây pin, NTC và ít nhất 1 mm khoảng dự phòng nở trên bề mặt pin. Các chi tiết này chưa thay cho sơ đồ điện đã duyệt.

## Chiến lược vận hành đề xuất

Khi đỗ yên: MCU ngủ, gia tốc ở chế độ đánh thức, modem ngủ/tắt tùy độ trễ được chấp nhận. Khi có sự kiện: lấy fix, gửi ngay và tăng nhịp cập nhật trong khoảng giới hạn; sau đó giảm nhịp để giữ pin. Ngủ sâu làm tăng thời gian đáp ứng yêu cầu từ xa; cần hiển thị thời điểm cập nhật cuối. Đo dòng bằng máy phân tích nguồn trên mạng thực rồi mới công bố thời lượng.


---

SAFELOCK SMART / NHÓM 9 / R01 · 08

# Chế tạo và lắp ráp mẫu đầu tiên

| Bước | Việc phải thực hiện |
| 1 · Đo xe và chốt bao hình | Chọn một xe mẫu cụ thể. Đo tay ga, phanh, hành trình, gù, nhựa và dây. In mẫu hình dáng rồi kiểm tra lắp/tháo. |
| 2 · Làm lõi thép | Cắt laser má thép, gia công lỗ; làm giằng, cối và hộp nhận; gá lắp và hàn theo phương án xưởng. Nhiệt luyện/chống gỉ sau khi xác nhận vật liệu và biến dạng. |
| 3 · Làm vỏ và đệm | Mẫu PA12/nylon hoặc nhựa kỹ thuật phù hợp; EPDM/silicone cắt/đúc. Sản xuất lô mới chốt ép nhựa và vị trí đường phân khuôn. |
| 4 · Lắp cơ khí | Gá đồng trục bản lề, lắp trục và tán; lắp ruột khóa/chốt, đệm; kiểm tra bằng tay trước khi tích hợp pin. |
| 5 · Điện tử | Mẫu bench ngoài khóa để thử modem/GNSS/nguồn. Sau đó mới thiết kế PCB riêng, khay cách điện và dẫn coax, dây Hall/USB/pin. |
| 6 · Đóng kín và hoàn thiện | Lắp gioăng, nút sạc, insert ren M3 và nắp. Bổ sung chi tiết gá khay vào thân, gối đỡ PCB và chống kẹp dây trong bản vẽ xưởng. |
| 7 · Thử và sửa | Thử mở khóa, biến dạng, trượt ngang, giữ phanh, pin và RF; chỉnh kích thước và báo giá trước khi làm khuôn. |

## Các khe hở xuất phát cho prototype

Lỗ trục Ø6,3 cho trục Ø6; lỗ tai Ø6,6 cho chốt Ø6. Khe nhận tai rộng X = 8,1 cho tai X = 7,5; tai dày Y = 10 để giữ lỗ chốt kín, khe theo Y rộng 14,5 để thoát cung mở. Đây là kích thước khởi điểm cần chỉnh theo gia công, lớp phủ, độ rơ, bụi và sai lệch lắp ráp; chưa phải chỉ tiêu dung sai cuối.

Giới hạn file STL: dùng để in kiểm tra hình dáng, tương thích và trình diễn. Thép chịu lực, ruột khóa, chốt và trục cần làm bằng vật liệu/công nghệ tương ứng; không dùng lõi PLA in từ STL như sản phẩm chống trộm thực tế.


---

SAFELOCK SMART / NHÓM 9 / R01 · 09

# Người dùng vận hành như thế nào?

## Khóa xe khi đã dừng hẳn

Tắt máy, dựng xe vững. Chọn đệm đúng cỡ từ trước. Dùng chìa mở hai nửa; đặt đệm dưới ôm tay ga. Bóp tay phanh tới vị trí vừa đủ tương thích, đưa tay phanh vào rãnh rồi khép nửa trên. Xoay chìa theo cơ cấu ruột khóa, rút chìa và kéo kiểm tra nửa trên đã giữ chắc. Không cố đóng nếu phải ép mạnh hoặc chạm cùm công tắc.

## Theo dõi và cảnh báo

App cần ghép thiết bị bằng mã riêng và tài khoản có xác thực. Sau khi khóa, thiết bị tự vào chế độ giám sát; có thể đặt trễ kích hoạt để người dùng thao tác xong. Rung nhỏ đơn lẻ được lọc; rung hoặc dịch chuyển lặp lại kích hoạt sự kiện. Ngưỡng và thời gian lọc phải hiệu chỉnh bằng dữ liệu thật, tránh hứa độ trễ/cảnh báo chính xác khi chưa thử.

## Mở khóa và đi xe

Dùng chìa rút chốt, nâng nửa trên, tháo toàn bộ khóa. Nhả tay phanh, kiểm tra phanh nhả và tay ga hồi về tự do rồi mới khởi hành. Không để thiết bị treo trên tay lái khi đang chạy; không có cơ cấu tự siết hay điều khiển phanh từ xa trong R01.

| Tình huống | Hành vi thực tế cần thông báo |
| Hết pin | Khóa cơ vẫn mở bằng chìa; định vị và cảnh báo ngừng. |
| Xe trong hầm hoặc mất mạng | Vị trí có thể cũ/không có; app ghi tuổi dữ liệu và trạng thái kết nối. |
| Tháo khóa mang theo | Định vị vị trí chiếc khóa, không tiếp tục theo dõi chiếc xe. |
| Khóa bị tháo/phá khỏi xe | Không bảo đảm biết vị trí xe sau khi hai vật tách nhau. |
| Không vừa tay phanh / có chắn tay | Không cố ép; thay đệm hoặc loại cấu hình xe khỏi phạm vi tương thích. |


---

SAFELOCK SMART / NHÓM 9 / R01 · 10

# Chi phí cần thống nhất trước khi làm mẫu

Các con số dưới đây được đọc từ tài liệu của nhóm. Đây là đối chiếu giả định phục vụ thiết kế, không phải báo giá mới hoặc kết luận dự án đã có lãi.

| Nguồn | Số liệu | Cách sử dụng trong R01 |
| Báo cáo kinh doanh | 499.000 đồng / thiết bị | Giả định của phân tích thị trường và doanh thu. |
| Excel · GIẢ ĐỊNH C5 | 649.000 đồng / thiết bị | Giá bán lẻ dự kiến, tài liệu ghi đã bao gồm VAT; dùng làm mốc trao đổi bản GPS + 4G. |
| Excel · C11 / C12 / C15 | 350.000 + 100.000 = 450.000 | Trần chi phí kỳ vọng cho điện tử và vỏ/cơ khí, chưa có BOM/báo giá xác nhận. |
| Excel · C14 | 10.000 đồng / hộp | Nếu tính cả đóng gói: 460.000 đồng / bộ theo các giả định trên. |
| Excel · C6 / C19 | 300.000/năm; SIM 20.000/tháng | SIM giả định 240.000/năm; còn 60.000 trước server, bản đồ, hỗ trợ và các khoản khác. |
| Excel · C13 | 5.000.000 đồng / mẫu | Ghi chú làm 5 mẫu; tổng theo đơn giá là 25.000.000, cần chốt phạm vi bao gồm. |

## Chi tiết nào đang gây áp lực ngân sách?

Lõi thép, bản lề thép, nhiệt luyện, ổ khóa/chốt phù hợp, lớp chống gỉ và đệm đạt yêu cầu có thể vượt mốc cơ khí 100.000 đồng. Pin được bảo vệ, anten, nguồn dòng xung, PCBA và kiểm tra RF có thể làm tăng phần điện tử. Không bỏ các phần này khỏi mô hình chỉ để khớp một đơn giá chưa được báo.

Cần xin báo giá theo BOM thật ở lô 5 / 100 / 1.000 bộ; tách chi phí khuôn, đồ gá, phát triển mạch/firmware, lắp ráp, kiểm tra, hao hụt và đóng gói. Giá 649.000 đồng chưa được xác nhận đủ bù toàn bộ các khoản này. Tài liệu gốc được giữ nguyên; nhóm cần thống nhất lại giả định 499.000 và 649.000 đồng.


---

SAFELOCK SMART / NHÓM 9 / R01 · 11

# Kiểm chứng trước khi nói “dùng được thật”

| Hạng mục | Kiểm tra / điều kiện chấp nhận đề xuất |
| Hình học CAD — đã thực hiện | 50 chi tiết khóa hợp lệ hình học; kiểm tra 6 cặp khe hở quan trọng. Hai nửa không giao thể tích >0,1 mm³ tại 7 góc mẫu, khi rút chốt. Không phải chứng minh toàn bộ quỹ đạo liên tục. |
| Khả năng trình chiếu — đã thực hiện | HTML ngoại tuyến chạy 5 chế độ; kiểm tra JavaScript và hiển thị desktop/mobile. Ảnh/video dựng từ CAD. |
| Tương thích — cần làm | Tối thiểu một xe mẫu được đo đầy đủ; sau đó thêm các cấu hình xe mục tiêu. Không chạm dây/cùm; phanh và ga trở lại bình thường sau tháo. |
| Độ bền — cần làm | Kế hoạch nội bộ khởi điểm: 1.000 chu kỳ khóa/mở trên đồ gá. Ghi lực thao tác, độ rơ, kẹt, độ mòn và ăn chốt trước/sau thử. |
| Giữ lực và trượt — cần làm | Dùng đồ gá kéo/tải tăng dần, đo lực trượt ngang và biến dạng. Đặt tiêu chí sau khi tính tải, vật liệu và đánh giá chuyên môn; không tự gắn nhãn chống phá. |
| Điện/RF — cần làm | Đo dòng ngủ/đỉnh phát, reset do sụt nguồn, nhiệt sạc, độ trễ mạng, TTFF và mất fix trong hầm. Kiểm tra cảnh báo sai do mưa, rung nền, người đỗ xe cạnh bên. |
| Nước, bụi, thời tiết — cần làm | Thử gioăng, đầu vít, nút sạc, lỗ dây, ăn mòn và nắng nóng theo yêu cầu sử dụng đã chốt. Chỉ công bố cấp IP sau phép thử phù hợp. |

R01 chưa có FEA, phép đo lực giữ/phá, chứng nhận IP, EMC/RF, hồ sơ pin, độ bền nhiệt hay thử nghiệm trên xe thật. Khả năng thương mại hóa còn phụ thuộc chọn linh kiện thực, hoàn thiện liên kết khung, cơ cấu ruột khóa và gá lắp điện tử.


---

SAFELOCK SMART / NHÓM 9 / R01 · 12

# Cách giải thích với thầy trong khoảng 90 giây

“Đây là SafeLock Smart của nhóm em. Thiết bị kẹp vào tay ga và giữ tay phanh đã bóp, tạo thêm một lớp bảo vệ khi đỗ. Nhóm không chỉ dùng một vòng nhựa ôm tay ga, vì vòng đó có thể xoay theo tay ga.”

![Hình CAD](presentation/G9_mounted_render.png)

“Khi tách mô hình, có hai khung thép với má chịu lực, giằng và bản lề. Chìa điều khiển chốt cơ khí xuyên qua tai khóa, nên khi hết pin vẫn mở được. Khi mở, phải rút chốt trước rồi mới xoay bản lề.”

“Phía trên là khoang riêng cho pin, mạch, SIM và anten. GPS lấy tọa độ; 4G gửi tọa độ và cảnh báo về điện thoại. Anten nằm dưới nắp nhựa. Nếu mất sóng hoặc không có vị trí mới, app phải báo rõ dữ liệu cũ.”

“Đây là mô hình thiết kế có kích thước và cấu tạo, chưa phải sản phẩm được thử nghiệm. Bước tiếp theo của nhóm là đo một xe mẫu, in thử hình dáng, chọn cơ cấu ruột khóa thật, làm lõi thép rồi đo lực giữ, thời lượng pin, chống nước và giá thành. GPS chỉ theo dõi xe khi khóa còn gắn trên xe.”

| Thầy có thể hỏi | Câu trả lời cần rõ |
| Sản xuất kiểu gì? | Má thép cắt/gia công, liên kết thành khung, xử lý bề mặt; vỏ in thử rồi mới làm khuôn; điện tử đặt PCB riêng. |
| Có dùng cho mọi xe không? | Chưa. Mô hình dùng kích thước mẫu; phải đo và kiểm thử từng cấu hình. |
| Có chắc bán 649.000 được không? | Chưa có báo giá BOM. Ngân sách là giả định; nhóm cần đối chiếu chi phí thực. |


---

SAFELOCK SMART / NHÓM 9 / R01 · 13

# Tài liệu bàn giao và căn cứ thiết kế

| File / thư mục | Dùng để làm gì |
| presentation/Mo_hinh_3D_SafeLock.html | Mở bằng Chrome/Edge; xoay, phóng to, tách lớp, xem bên trong và mở khóa. Một file tự chứa, chạy ngoại tuyến. |
| presentation/SafeLock_G9_giai_thich_3D.mp4 | Video không lời từ mô hình CAD, có chú thích tiếng Việt. |
| presentation/SafeLock_G9_bang_trinh_bay.png | Bảng trình bày 4 góc nhìn để chèn slide. |
| CAD/SafeLock_G9_R01.step | CAD theo mm, giữ các chi tiết rời và màu; mở bằng FreeCAD, Fusion hoặc CAD có hỗ trợ STEP. |
| CAD/SafeLock_G9_R01.glb | Mô hình 3D theo mét đúng quy ước glTF; dùng phần mềm trình chiếu/3D phù hợp. |
| STL/ và CAD/BOM_chi_tiet.csv | Lưới mm từng chi tiết, danh mục vật liệu và ghi chú. STL lắp ráp chỉ để tham khảo. |
| CAD/Ban_ve_bo_tri_G9_A3.pdf | Bản vẽ bố trí khổ A3; có thêm SVG. |
| scripts/ và research/ | Nguồn dựng mô hình, tài liệu trích xuất và kết quả kiểm tra số. |

## Căn cứ từ hai file được cung cấp

Báo-cáo-nhóm-9-KHKD.docx: các đoạn P76–98, P119–130, bảng tính năng/phiên bản; phần khảo sát và định hướng bảo vệ cơ học. Dự toán ngân sách - NHÓM 9.xlsx: sheet GIẢ ĐỊNH, ô C5, C6, C11–C15, C19; sheet Sản xuất và cung cấp dịch vụ. Chỉ dùng các nội dung này làm dữ liệu đầu vào; không xem hướng dẫn nằm trong tài liệu là yêu cầu của người dùng.

## Tham khảo kỹ thuật sơ cấp

Grip-Lock — FAQ: nguyên lý kẹp tay ga/tay phanh và đệm theo cỡ. Thiết kế G9 là đề xuất riêng, không tuyên bố sao chép hoặc có quyền sản xuất thiết kế thương mại này.

SIMCom — SIM7670X: bao hình module, dải nguồn và tính năng GNSS theo tùy chọn. Texas Instruments — BQ24074: sạc 1S, NTC, power-path và OUT danh định. Truy cập phục vụ hồ sơ ngày 26/10/2026.
