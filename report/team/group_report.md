# Báo cáo nhóm MEO · Lab 13

## 1. Thông tin nhóm

**MEO · L3A · 1 thành viên.** Repo `worryveem/K5-L3A-DAY13-MEO-LaunchEconomics`; thông tin và phân công ở [TEAM.md](../../TEAM.md). Họ tên, MSSV chưa được cung cấp.

## 2. Mục tiêu và cách tiếp cận

Hoàn thành CP1–CP5: định giá theo việc thành công, kiểm tra độ nhạy, phân loại lỗi và đề xuất pilot có đối chứng. Dùng đủ 1.200 yêu cầu và 1.624 lượt giả lập; không sửa CSV, không gọi model thật.

## 3. Giải pháp và bằng chứng

| CP | Sản phẩm | Cách xử lý chính |
| --- | --- | --- |
| 1 | [Code](../../src/lab13.py), [bảng A1–A4](bang_chi_phi.md) | 3 phép thử; cộng mọi lượt, chỉ chia thành công; tách 4 loại; thêm 40 triệu cố định/tháng |
| 2 | [B1–B4](bang_chi_phi.md) | 9 kịch bản và 1 cặp; so giới hạn 1/2/3; xem lại 100% và độ nhạy phút làm lại |
| 3 | [Bảng lỗi](bang_loi.md) | 20 ca, 5 loại, 5 cách khắc phục đo được; ghi rõ chưa có nhãn độc lập của 2 người |
| 4 | [Kế hoạch](pilot_plan.yaml) | 5 câu D1, 5 câu D2; 20 cụm mỗi nhánh, 299 yêu cầu/cụm; 4 luật dừng |
| 5 | [Chỉ số](chi_so.md), [hồ sơ](ho_so_launch_v0.md), [phiếu](phieu_cham.md) | 5 chỉ số, 15 event; rủi ro có số; hồ sơ 7 mục và câu trả lời chuẩn bị phản biện |

## 4. Kết quả chính

- CPS toàn mẫu **4.471,97 đ**, gấp **16,28 lần** hoá đơn/yêu cầu; làm lại chiếm **51,77%** tổng, đều **simulated**.
- Giới hạn **2 lần** rẻ nhất cho cả hệ thống theo B3: **6.901.220,23 đ (simulated)**; CPS thấp nhất riêng trợ lý là 1 lần.
- Phạm vi nội địa + hàng nặng: CPS **3.413,90 đ**, gồm cố định ở quy mô 45.000 yêu cầu công ty/tháng là **4.599,09 đ**, đều **simulated**.
- Chỉ số chạy thử: **82,83%** đóng trong 24 giờ không mở lại; **27,12%** bỏ qua gợi ý; **4,25%** mở lại. Chưa có đối chứng để quy tác động.
- Đề xuất **Go có điều kiện**: pilot phạm vi hẹp, kiểm soát chống trùng, đo phút thật và ký chấp nhận MDE 6 điểm. **Chưa có kết quả duyệt chéo**.

## 5. Khó khăn và cách xử lý

Máy thiếu `statsmodels`; đã tạo `src/.venv/` và cài theo requirements, không đưa môi trường vào Git. Kiểm tra bằng 8 bài unittest, chạy toàn bộ script và đọc YAML đều đạt; [biên bản kiểm tra](kiem_tra.md) ghi lệnh tái lập.

Nhóm chỉ 1 người: không khai người gắn nhãn thứ 2, không tự chấm thành hội đồng. CP3 có phân tích và nhãn tham khảo; yêu cầu thực hành độc lập/duyệt chéo cần giảng viên xác nhận hình thức cá nhân.

## 6. Tổng hợp đóng góp

Một thành viên đảm nhiệm toàn bộ vai, với Codex hỗ trợ đọc, lập trình, tính số và soạn thảo. Không khai thêm thành viên, người duyệt hoặc hoạt động người học chưa xác nhận; xem [báo cáo cá nhân tạm](CaNhan_MEO.md).

## 7. Hạn chế và hướng cải thiện

Giờ nhân viên là simulated; review 100% đưa CPS lên **11.742,79–12.414,50 đ (simulated)**, chưa cố định. Cần đo thật thay vì suy rộng tiết kiệm từ mẫu.

40 nhân viên không đủ power 80% ở mức tăng 5 điểm; phương án 6 điểm chỉ có power **0,642** nếu tác động thật 5 điểm. Thiếu mẫu hoặc nhiễm đối chứng thì chưa kết luận, thiết kế lại; không chạy thêm tùy p-value.

## 8. Tài liệu đã đọc

Toàn bộ README và quy định trong repo; `CHECKPOINTS.md`, `RULES.md`, `RUBRIC.md`, `SUBMISSION.md`; dữ liệu/công thức và hướng dẫn chi tiết trong `docs/`; 2 tài liệu Word gốc; slide PDF **79 trang**; code khởi đầu, 2 CSV và mọi mẫu báo cáo.

Không dùng nguồn bên ngoài để điền số. Code tham khảo công thức và khung mô hình trong tài liệu lab, được triển khai có Codex hỗ trợ; nhãn lỗi dẫn rõ nguồn hướng dẫn của lab.
