# Bảng lỗi và cách khắc phục · CP3 · Nhóm MEO

Nhóm chỉ có **1 người**. Bảng dưới là phân tích 20 ca có Codex hỗ trợ và đã đối chiếu hướng dẫn; không khai là hai bộ nhãn độc lập của học viên.
Nguồn: mục “Hai mươi ca lỗi” trong đề gốc Lab 13 và mục C của [hướng dẫn](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md).

## Phân loại 20 ca và căn cứ

| Ca | Tình huống rút gọn | Nhãn phân tích | Nhãn tham khảo trong hướng dẫn | Căn cứ nguyên nhân gốc |
| ---: | --- | --- | --- | --- |
| 1 | Tài khoản thiếu 2 chữ số | Do người dùng | Do người dùng | Đầu vào khách nhập thiếu, ngân hàng từ chối. |
| 2 | Kiện 28 kg bị tra bảng hàng thường | Hệ thống | Hệ thống | Chọn sai tham số tool, hoàn thiếu 45.000 đ. |
| 3 | Hoàn về ví nhưng khách chờ ngân hàng | Ngữ cảnh | Ngữ cảnh | Đúng thiết kế 5 phút, khác kỳ vọng nơi nhận tiền. |
| 4 | Chặng hãng nước ngoài không có dữ liệu | Giới hạn hệ thống | Giới hạn hệ thống | Thiếu dữ liệu; chuyển người là xử lý giới hạn đúng. |
| 5 | 14 đơn giảm giá bị hoàn thừa, chỉ audit thấy | Ngầm | Ngầm | Sai 12.000 đ/đơn nhưng khách và cảnh báo không phát hiện. |
| 6 | Chọn giao trễ nhưng mô tả hàng vỡ | Do người dùng | Do người dùng | Khách chọn nhầm mục; cần đối chiếu nội dung để hỗ trợ. |
| 7 | Sổ cái lỗi 503, vẫn báo hoàn thành | Hệ thống | Hệ thống | Thông báo thành công trái trạng thái ghi sổ sau 3 lần thử. |
| 8 | Viện dẫn điều 7.2 không tồn tại | Hệ thống | Hệ thống | Trích dẫn sai có thể nhìn thấy và kiểm chứng, dù tiền đúng. |
| 9 | Nhập mã sàn thay mã vận đơn | Do người dùng | Do người dùng | Khách dùng nhầm loại mã; thiếu gợi ý là điểm cần khắc phục. |
| 10 | Đúng bất khả kháng nhưng app hứa 24 giờ | Ngữ cảnh | Ngữ cảnh | Chính sách đúng, thông tin cam kết làm kỳ vọng lệch. |
| 11 | Tin nhắn thoại 40 giây không xử lý được | Giới hạn hệ thống | Giới hạn hệ thống | Không có khả năng nhận âm thanh. |
| 12 | D05 tốn token 3× suốt 3 tuần không ai thấy | Ngầm | Ngầm | Kết quả đúng nhưng sai về chi phí bị che khuất. |
| 13 | Bảo hiểm đối tác ngoài phạm vi | Giới hạn hệ thống | Giới hạn hệ thống | Gốc là ngoài phạm vi; trả lời chung chung là xử lý giới hạn kém. |
| 14 | Bấm nhầm xác nhận đã nhận tiền | Do người dùng | Do người dùng | Thao tác khách nhầm làm đóng yêu cầu. |
| 15 | Trễ 26 giờ, hoàn 100% thay vì 50% | Hệ thống | Hệ thống | Vi phạm chính sách; nhân viên bắt trước khi gửi nên không là ngầm. |
| 16 | Gửi Zalo lúc 2:14 sáng | Ngữ cảnh | Ngữ cảnh | Đúng quy tắc gửi ngay, không khớp giờ sinh hoạt. |
| 17 | Giá cache cũ, 212 đơn sai trong 9 ngày | Ngầm | Ngầm | Không ai mở lại; chỉ đối soát phiên bản mới tìm ra. |
| 18 | Đúng 15.000 đ, thiếu giải thích 30.000 × 50% | Ngữ cảnh | Ngữ cảnh | Khách hiểu khác; không có lỗi tính tiền. |
| 19 | Đơn 14 tháng, chỉ tra được 12 tháng | Giới hạn hệ thống | Giới hạn hệ thống | Ngoài cửa sổ dữ liệu; chuyển kèm tóm tắt là phù hợp. |
| 20 | Gửi lại sau 10 phút, hoàn trùng | Hệ thống | Hệ thống | Thiếu khóa chống trùng ở lệnh thứ 2. |

Tổng: **4 do người dùng + 5 hệ thống + 4 ngữ cảnh + 4 giới hạn + 3 ngầm = 20 ca**. Khớp tài liệu tham khảo 20/20 sau đối chiếu; con số này không phải đồng thuận liên chủ thể.

## Hai bộ nhãn độc lập và tỉ lệ đồng thuận

- Bộ nhãn học viên 1: chưa thu thập độc lập; bảng trên là tài liệu hỗ trợ có tham khảo đáp án.
- Bộ nhãn học viên 2: không có, vì nhóm chỉ 1 thành viên.
- Đồng thuận: **N/A**, không có 2 bộ nhãn để tính; không ghi 100% và không tạo người gắn nhãn thứ 2.
- Phương án hoàn tất theo quy chế: giảng viên chấp nhận bài cá nhân, hoặc bố trí 1 người phản biện gắn mới 20 ca mà chưa xem bảng; lưu nguyên 2 bộ rồi đếm trùng/20, mục tiêu ít nhất 16/20.

## Quy tắc phân biệt

| Ca dễ lẫn | Quy tắc áp dụng |
| --- | --- |
| 6, 9 | Gắn theo đầu vào khách sai; việc phải sửa giao diện không biến nguyên nhân gốc thành lỗi hệ thống. |
| 13 | Ngoài phạm vi là giới hạn; phải thêm thông báo giới hạn và chuyển người thay vì trả lời chung chung. |
| 8, 15 | Sai đã lộ hoặc bị người xem lại bắt là hệ thống; ngầm chỉ dùng khi không ai biết cho đến audit. |
| 12 | Chi phí tăng 3× mà không ai thấy cũng là lỗi ngầm, dù câu trả lời đúng. |
| 18 | Tiền đúng 30.000 × 50% = 15.000 đ nhưng thiếu giải thích là ngữ cảnh. |

Chưa có bất đồng giữa 2 người để ghi biên bản; không giả lập các ca bất đồng.

## Khắc phục 5 ca, đủ 5 loại

Các vai dưới đây là vai vận hành được đề xuất cho LogiX-VN, không phải thêm thành viên nhóm học tập.

| Ca | Loại | Phát hiện đo được | Khắc phục | Vai chịu trách nhiệm |
| ---: | --- | --- | --- | --- |
| 9 | Do người dùng | `input_validation_failed`, `reason=wrong_identifier_type`; >2% yêu cầu/ngày thì cảnh báo PM | Nhận diện mã sàn, tra ánh xạ; thất bại thì gợi ý mã đúng và chuyển nhân viên | PM trợ lý hoàn phí |
| 7 | Hệ thống | Mỗi giờ nối `refund_message_sent` và `refund_ledger_write` theo `trace_id`; ≥1 tin “đã hoàn” thiếu ledger ok thì dừng gửi tự động | Chỉ gửi xác nhận sau ledger ok; lỗi thì báo đang xử lý và chuyển người; thêm khóa chống trùng cho ca 20 | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | `ticket_reopened.reason=amount_dispute` nhưng audit xác nhận tiền đúng; ≥2 ca/tuần thì sửa mẫu tin | Ghi rõ 30.000 đ × 50% = 15.000 đ và điều khoản; kiểm tra khách hiểu | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | `handoff_to_staff.reason=foreign_leg_missing_data`; theo dõi số ca/ngày và thời gian nhận; >15 phút chưa nhận thì báo trưởng ca | Loại quốc tế khỏi pilot, thông báo giới hạn, chuyển kèm tóm tắt để khách không nhập lại | PM trợ lý hoàn phí |
| 17 | Ngầm | Audit ngẫu nhiên 100 đơn/tuần đối chiếu giá hiện hành; ≥1/100 sai tiền hoặc phiên bản cũ thì khóa rule liên quan | Xóa cache khi giá đổi, ghi `policy_version`, sửa chênh tiền cho khách bị ảnh hưởng | Kế toán trưởng |

Các event và trường nối được đặc tả trong [chi_so.md](chi_so.md). Ngưỡng là đề xuất cho pilot, chưa phải kết quả vận hành.
