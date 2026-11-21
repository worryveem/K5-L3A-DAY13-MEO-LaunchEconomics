# Báo cáo cá nhân — Đỗ Minh Hoàng — 2A202603554

## 1. Thông tin thành viên

- Họ tên: **Đỗ Minh Hoàng**.
- MSSV: **2A202603554**.
- Nhóm: **MEO** · Lớp: **L3A** · **1 thành viên**.
- Vai trong nhóm: viết code, kiểm số, phân tích lỗi, giữ hồ sơ và chuẩn bị phản biện.

## 2. Phần việc phụ trách

Toàn bộ CP1–CP5: mô hình chi phí A1–A4, độ nhạy B1–B4, phân tích 20 ca lỗi, tính cỡ mẫu và kế hoạch pilot, chỉ số/event/rủi ro, hồ sơ launch và chuẩn bị phản biện.

## 3. Đóng góp cụ thể

| CP | Sản phẩm | Nội dung |
| --- | --- | --- |
| CP1 | `src/lab13.py`, `bang_chi_phi.md` | 3 hàm A1, mô hình A2, 4 loại yêu cầu và chi phí cố định A4 |
| CP2 | `bang_chi_phi.md` | 9 kịch bản, 1 cặp, giới hạn chạy 1/2/3 và xem lại 100% |
| CP3 | `bang_loi.md` | Phân tích 20 ca có căn cứ và nguồn, 5 biện pháp khắc phục |
| CP4 | `pilot_plan.yaml` | D1–D2, 20 cụm mỗi nhánh, 299 yêu cầu/người, 4 luật dừng |
| CP5 | `chi_so.md`, `ho_so_launch_v0.md`, `phieu_cham.md` | 5 chỉ số, 15 event, rủi ro và đề xuất Go có điều kiện |

## 4. Bằng chứng

- A1 đạt **1,20 · 1,25 · 1,25**; A2 CPS **4.471,97 đ (simulated)**.
- B3: giới hạn **2 lần** có chi phí cả hệ thống thấp nhất, **6.901.220,23 đ (simulated)**.
- D1: **5.980** yêu cầu thô/nhánh, DE **6,96**, hiệu dụng **859,20**; power cho mức tăng 5 điểm chỉ **0,642**.
- Kiểm tra bằng công cụ: script chạy đầu-cuối, **8/8 unittest đạt**, YAML đọc được; 2 CSV và starter được giữ nguyên.

## 5. Công cụ AI đã dùng và cách kiểm tra

**OpenAI Codex** hỗ trợ đọc tài liệu, triển khai Python, tính lại số và soạn hồ sơ. Số liệu lấy từ 2 CSV; nhãn lỗi đối chiếu hướng dẫn của lab và được ghi nguồn.

Các kiểm tra đã chạy bằng công cụ:

```powershell
cd src
.\.venv\Scripts\python.exe lab13.py
.\.venv\Scripts\python.exe -m unittest -v test_lab13
.\.venv\Scripts\python.exe -c "from pathlib import Path; import yaml; yaml.safe_load(Path('../report/team/pilot_plan.yaml').read_text(encoding='utf-8'))"
```

Phép đối chiếu A2: (245.585,132 + 84.000 + 1.780.000 + 2.264.000) / 978 = **4.471,97 đ (simulated)**. Cỡ mẫu hiệu dụng: 5.980 / (1 + 298 × 0,02) = **859,20**. Học viên cần tự chạy và giải thích các phép tính trước bảo vệ; các kết quả kiểm tra bằng công cụ không thay thế bước này.

## 6. Tự đánh giá

Code và hồ sơ CP1–CP5 đã được chuẩn bị với AI hỗ trợ. Nhóm chỉ 1 người nên chưa có 2 người gắn nhãn độc lập, chưa có kết quả hội đồng duyệt chéo; các phần này được ghi đúng trạng thái trong hồ sơ. Pilot và event mới là kế hoạch, chưa triển khai; chưa nộp LMS.
