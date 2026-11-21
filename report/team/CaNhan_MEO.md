# Báo cáo cá nhân · Thành viên duy nhất nhóm MEO

## 1. Thông tin

- Họ tên và MSSV: chưa được cung cấp; cần điền trước khi nộp.
- Email: chưa xác nhận email học viên; không lấy email cấu hình Git làm thông tin học tập.
- GitHub repo: `worryveem/K5-L3A-DAY13-MEO-LaunchEconomics`.
- Vai: viết code, kiểm số, phân tích lỗi và giữ hồ sơ; nhóm **1 thành viên**.
- Tên file hiện tại là tạm; đổi thành `MSSV_HoTenKhongDau.md` khi có thông tin thật. Giữ nguyên `MSSV_HoTen.md` là mẫu.

## 2. Phần việc

Toàn bộ CP1–CP5: A1–A4, B1–B4, phân tích 20 ca lỗi, D1–D2 và pilot YAML, chỉ số/event/rủi ro, hồ sơ và chuẩn bị phản biện. Các vai vận hành trong pilot là vai đề xuất cho LogiX-VN, không phải thành viên học tập bổ sung.

## 3. Sản phẩm đã chuẩn bị với AI hỗ trợ

| Phần | File | Bằng chứng |
| --- | --- | --- |
| Tính toán | `src/lab13.py`, `bang_chi_phi.md` | A1 1,20 / 1,25 / 1,25; A2 CPS 4.471,97 đ (simulated) |
| Kiểm tra | `src/test_lab13.py`, `kiem_tra.md` | 8 unittest; đối chiếu phép cộng Decimal riêng |
| Lỗi | `bang_loi.md` | 20 ca có căn cứ và nguồn; 5 biện pháp đo được |
| Pilot | `pilot_plan.yaml` | 5.980 yêu cầu thô/nhánh, hiệu dụng 859,20, DE 6,96 |
| Hồ sơ | `chi_so.md`, `ho_so_launch_v0.md`, `phieu_cham.md` | 5 chỉ số, 15 event; Go có điều kiện; chưa có hội đồng |

## 4. Bằng chứng kiểm tra bằng công cụ

Codex đã chạy `python lab13.py`, 8 unittest và `yaml.safe_load`, kiểm tra CSV và starter không đổi so với Git (bỏ khác biệt xuống dòng của checkout Windows). Chưa có xác nhận người học tự chạy hoặc giải thích trực tiếp; không ghi thay là đã hoàn thành bước đó.

## 5. Công cụ AI và cách tự kiểm tra cần thực hiện

**Công cụ đã dùng: OpenAI Codex**, hỗ trợ đọc tài liệu, triển khai Python, chạy kiểm tra và soạn báo cáo. Các số được tính từ CSV; bảng lỗi có tham khảo đáp án lab nên không được gọi là nhãn độc lập của học viên.

| Việc người học cần tự xác nhận | Phép kiểm tra cụ thể |
| --- | --- |
| Hiểu A2 | Tự cộng 245.585,132 + 84.000 + 1.780.000 + 2.264.000 rồi chia 978 = 4.471,97 đ (simulated); giải thích vì sao không chia 1.200 |
| Hiểu B3 | So 6.901.220,23 đ ở 2 lần với 7.449.780,64 đ ở 1 lần, đều simulated; chỉ ra phần việc chuyển người |
| Hiểu cụm | Tự tính DE=1+298×0,02=6,96 và 5.980/6,96=859,20; trần 20/0,02=1.000 dưới 1.251 |
| Hiểu đề xuất | Giải thích B4 vượt 12.000 đ với phút làm lại từ CSV (simulated) và power chỉ 0,642 tại 5 điểm |

Các bước xác nhận của học viên ở bảng trên **chưa được ghi nhận**, cần thực hiện trước bảo vệ.

## 6. Tự đánh giá dựa trên bằng chứng hiện có

Bộ code và hồ sơ tính toán đã được chuẩn bị; chưa tự nhận điểm hoặc tuyên bố đủ điều kiện nộp. Còn thiếu thông tin cá nhân, xác nhận hoạt động độc lập của CP3, duyệt chéo và thao tác nộp LMS. Nhóm một người cần giảng viên chấp nhận hình thức thực hiện tương ứng.
