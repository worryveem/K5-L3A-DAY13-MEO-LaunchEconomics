# Chỉ số, event và rủi ro · CP5 · Nhóm MEO

Số đếm do `src/lab13.py` tính trên **1.200 yêu cầu giả lập**; chưa có đối chứng, chưa có kết quả pilot. Các ngưỡng bên dưới là đề xuất đã viết trước trong kế hoạch.

## E1 · Đặc tả 5 chỉ số

| Loại | Chỉ số | Tử số / mẫu số, cửa sổ | Tính thử |
| --- | --- | --- | --- |
| Chính | Đóng trong 24 giờ và không mở lại trong 7 ngày | Số request có `dong_trong_24h=1` và `mo_lai_trong_7_ngay=0` / toàn bộ request đủ thời gian theo dõi | **994/1.200 = 82,83%** |
| Dùng | Tỉ lệ bỏ qua gợi ý | Số request đã xem lại có quyết định `sua` hoặc `bo` / số request `duoc_xem_lai=1`; theo tuần | **48/177 = 27,12%** |
| An toàn | Mở lại trong 7 ngày, chỉ báo thay thế lỗi lọt | Số request `mo_lai_trong_7_ngay=1` / toàn bộ request trưởng thành | **51/1.200 = 4,25%**; phạm vi **39/982 = 3,97%** |
| Dùng, bổ sung | Độ sâu dùng trợ lý | Số request can thiệp đủ điều kiện có `agent_opened` / toàn bộ request can thiệp đủ điều kiện trong tuần, đếm request duy nhất | Chưa tính: CSV không có event mở trợ lý |
| An toàn, bổ sung | Sai tiền phát hiện qua audit | Số request mẫu audit có `actual_amount != expected_amount` / số request audit ngẫu nhiên mỗi tuần; báo riêng theo nhánh | Chưa tính: CSV không có kết quả đối soát tiền chuẩn |

Chỉ số trong đợt chạy thử là **82,83%**; không suy ra trợ lý tạo cải thiện so với baseline giả định 70%. Tỉ lệ mở lại 4,25% không bắt hết lỗi ngầm: ca 5 và 17 không ai phàn nàn nhưng tiền sai.

## Event cần ghi trong pilot

**Hợp đồng chung cho tất cả event:** `event_id`, `event_name`, `occurred_at` (ISO 8601, GMT+7), `request_id`, `trace_id`, `staff_id`, `depot`, `arm`, `schema_version`. Mỗi dòng dưới đây đều kế thừa `trace_id` và các trường chung.

`trace_id` gốc được tạo khi nhận yêu cầu cho cả đối chứng; mỗi lượt agent có thêm `run_trace_id`, nối về gốc bằng `request_id`. Trong CSV lịch sử, `trace_id` nằm ở cấp lượt chạy; không giả định 1 request chỉ có 1 trace lượt chạy.

| Event | Ai tạo | Thuộc tính riêng, kèm trace_id chung | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | Hệ thống ticket | `loai`, `eligible`, `amount_requested`, `assigned_staff_id`, `assigned_arm`, `assignment_version`, `created_at`, trace_id | Nhận request; không đổi nhánh sau kết quả |
| `agent_opened` | Giao diện CSKH | `access_granted`, `access_reason`, trace_id | Mỗi lần mở, kể cả tài khoản bị chặn |
| `agent_run_completed` | Agent runtime | `run_id`, `run_trace_id`, `attempt`, `tokens_in`, `tokens_out`, `tool_calls`, `status`, `policy_version`, trace_id | Sau mọi lượt, cả lỗi |
| `agent_suggestion_shown` | Giao diện CSKH | `suggestion_id`, `proposed_amount`, `policy_version`, trace_id | Gợi ý thực sự hiển thị |
| `staff_review_started` | Giao diện CSKH | `suggestion_id`, `review_id`, `started_at`, trace_id | Bắt đầu xem lại, dùng đồng hồ đo thật |
| `staff_review_decision` | Nhân viên | `review_id`, `suggestion_id`, `decision=giu/sua/bo`, `active_minutes`, `reason`, trace_id | Kết thúc review; loại thời gian tạm dừng |
| `staff_rework_completed` | Nhân viên | `rework_id`, `reason`, `active_minutes`, `review_id`, trace_id | Xử lý lại xong; tách phút review khỏi phút rework |
| `refund_ledger_write` | Dịch vụ sổ cái | `ledger_id`, `order_id`, `idempotency_key`, `amount`, `status`, trace_id | Mỗi lần thử ghi, đánh dấu lần được chấp nhận |
| `refund_message_sent` | Dịch vụ thông báo | `message_id`, `claim_refunded`, `ledger_id`, `channel`, trace_id | Gửi thông báo cho khách |
| `handoff_to_staff` | Agent / hàng đợi | `handoff_id`, `reason`, `summary`, `accepted_at`, `completed_at`, `active_minutes`, trace_id | Chuyển, nhận và hoàn tất phần thủ công |
| `input_validation_failed` | Form nhập | `field`, `reason`, `identifier_type`, trace_id | Phát hiện dữ liệu sai; không ghi nguyên số tài khoản |
| `ticket_closed` | Hệ thống ticket | `closed_at`, `resolution`, `first_close`, trace_id | Mỗi lần đóng; giữ lịch sử lần đầu |
| `ticket_reopened` | Hệ thống ticket | `reopened_at`, `reason`, `previous_closed_at`, trace_id | Khách hoặc nhân viên mở lại |
| `audit_sample_checked` | Kế toán / QA | `sample_id`, `random_seed`, `selection_probability`, `actual_amount`, `expected_amount`, `policy_version`, `error_type`, trace_id | Audit 100 request ngẫu nhiên/tuần; theo dõi riêng tiền đã gửi |
| `telemetry_completeness_checked` | Pipeline dữ liệu | `window_end`, `matured`, `missing_event_count`, `duplicate_event_count`, trace_id | Kiểm tra hằng ngày, xác nhận cửa sổ đủ theo dõi |

Đây là **đặc tả cần triển khai**, chưa khẳng định các event đã có trong hệ thống. Không suy diễn các event thiếu từ dữ liệu CSV.

## Kiểm tra mỗi chỉ số có event để tính

| Chỉ số | Event nối theo request_id và trace_id | Quy tắc tính |
| --- | --- | --- |
| Chính | `refund_request_created`, `ticket_closed`, `ticket_reopened`, `telemetry_completeness_checked` | Đóng đầu tiên − tạo ≤24 giờ; không mở lại trong 7 ngày sau đóng; chờ đủ 24 giờ +7 ngày với mọi request, kể cả chưa đóng |
| Bỏ qua gợi ý | `staff_review_started`, `staff_review_decision` | 1 quyết định cuối/request, mẫu số gồm request đã review; không lấy mọi 1.200 request làm mẫu số |
| Mở lại 7 ngày | `refund_request_created`, `ticket_closed`, `ticket_reopened`, `telemetry_completeness_checked` | Request trưởng thành bị mở trong 7 ngày sau đóng; theo nhánh và cohort tạo request, không so hai cohort khác độ chín |
| Độ sâu dùng | `refund_request_created`, `agent_opened` | Chỉ nhánh can thiệp, eligible=true; distinct request, không đếm số lần bấm |
| Sai tiền audit | `audit_sample_checked`, `refund_ledger_write` | So tiền thực gửi với tiền đúng theo phiên bản chính sách; 1 kết quả audit/request; lấy mẫu ngẫu nhiên để tránh chỉ xem ca bị khiếu nại |

Theo dõi thêm kinh tế: cộng `agent_run_completed` theo giá có phiên bản; phút thật từ review/rework/handoff không trùng khoảng thời gian. “Thành công” dùng outcome 7 ngày và đối soát tiền; nếu chưa xác minh tiền của toàn bộ request thì báo giới hạn của CPS, không coi không mở lại là chắc chắn không sai tiền.

Khử trùng bằng `event_id`, kiểm tra thiếu outcome trước khóa dữ liệu. Giữ yêu cầu ở nhánh được bốc thăm (ITT), kể cả không dùng trợ lý; không loại các ca lỗi để làm đẹp tỉ lệ.

## E2 · Rủi ro kinh tế

Nguồn số: [bảng A/B](bang_chi_phi.md). Các kết quả chứa phút nhân viên đều là **simulated**, chưa là chi phí đo thật. Rủi ro toàn mẫu và phạm vi được ghi tách rõ.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động đề xuất | Vai phụ trách |
| --- | --- | --- | --- | --- |
| Làm lại tăng gấp đôi, toàn mẫu B1 | 4.471,97 → **6.786,90 đ, +51,77% (simulated)** | Tỉ lệ rework phạm vi hiện 48/982=4,89%; cảnh báo >7%/tuần và CPS đo thật >8.000 đ trong 2 tuần | Rà 20 trace, chặn mở rộng; PM đề xuất thu về nội địa, GĐ duyệt kế hoạch mới | PM trợ lý hoàn phí |
| Xem lại tăng gấp đôi, toàn mẫu B1 | 4.471,97 → **6.292,01 đ, +40,70% (simulated)** | % review và phút thật theo tuần; không đạt gate giảm review cuối bước 25% | Giữ kiểm soát an toàn, sửa gợi ý; không giảm review chỉ để đạt giá | Trưởng nhóm CSKH |
| Xem lại 100% kéo dài, phạm vi B4 | **11.742,79 đ** với 9 phút làm lại; **12.414,50 đ** dùng trung bình CSV 15,2973 phút; đều **simulated**, chưa cố định | Review còn >50% cuối bước 25%, phút review gần/vượt 4,80 (simulated là mốc ước tính) | Dừng tăng bước nếu chưa đủ audit; đo phút thật tuần 1 và duyệt lại kinh tế | Trưởng nhóm CSKH |
| Khối lượng chỉ bằng một nửa, A4 | Cố định **1.185,19 → 2.370,37 đ/việc**, CPS gồm cố định **4.599,09 → 5.784,27 đ (simulated)** | Thành công theo tuần <50% kế hoạch | Không coi chi phí cố định đã được hấp thụ ở pilot nhỏ; xem lại ngân sách và hợp đồng | Giám đốc vận hành |

Giờ tiết kiệm chỉ tạo giá trị tiền mặt nếu tránh tuyển mới hoặc được phân sang việc khác. Trưởng CSKH phải xác nhận phương án sử dụng giờ; lab chưa có bằng chứng giảm bảng lương.
