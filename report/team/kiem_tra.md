# Biên bản kiểm tra · Lab 13 · MEO

Kiểm tra bằng công cụ trong phiên làm bài; không thay thế xác nhận của học viên, giảng viên hoặc hội đồng. Môi trường: Windows PowerShell, Python 3.13.7; thư viện cài trong `src/.venv` dùng requirements của repo.

## Tái lập trên PowerShell

Từ thư mục repo:

```powershell
cd src
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe lab13.py
.\.venv\Scripts\python.exe -m unittest -v test_lab13
.\.venv\Scripts\python.exe -c "from pathlib import Path; import yaml; p=yaml.safe_load(Path('../report/team/pilot_plan.yaml').read_text(encoding='utf-8')); print(len(p['pilot']['stop_rules']))"
```

Muốn sinh lại bảng A/B từ code, chạy thêm `python lab13.py --write-cost-report` bằng Python trong môi trường trên. Không cần API key hoặc mạng sau khi cài thư viện.

## Kết quả

| Kiểm tra | Kết quả |
| --- | --- |
| Chạy script đầu-cuối | Đạt; in A1–A4, B1–B4, D1 và E1 |
| A1 bắt buộc | Đạt 3/3: 1,20 · 1,25 · 1,25 |
| Bộ unittest | **8/8 đạt**: A1/biên, trace, lượt lỗi và lọc request, không sửa input, tuyến tính, retry, B4/chỉ số, cỡ mẫu |
| Cộng tiền độc lập bằng csv + Decimal | Token 245.585,132; tool 84.000; xem lại 1.780.000; làm lại 2.264.000 đ; 978 thành công; CPS 4.471,9684376 đ (**simulated**) |
| Tính cỡ mẫu | 1.251 cho 5 điểm; 859 cho 6 điểm; 42 nhân viên/nhánh nếu m=75; 299 yêu cầu/người với 20 cụm/nhánh |
| YAML | `yaml.safe_load` đọc được; **4 luật dừng**, đủ NẾU / TRONG / THÌ / KHÔNG THÌ; không còn dấu hỏi ngoài chú thích |
| Hồ sơ | Đủ 6 file bắt buộc; hồ sơ launch đủ 7 mục, dòng cuối Go có điều kiện |
| Dữ liệu gốc | 2 CSV, starter và mẫu `MSSV_HoTen.md` không đổi so với HEAD sau chuẩn hóa CRLF/LF |
| Nhãn | Chi phí và dẫn xuất phút có simulated; không dùng thuật ngữ bị cấm trong hồ sơ |

## Những việc chưa thể xác nhận

| Việc | Trạng thái thực tế |
| --- | --- |
| Thông tin học viên và tên báo cáo | Chờ họ tên, MSSV; đang dùng `CaNhan_MEO.md` |
| 2 người gắn nhãn độc lập | Không có vì nhóm 1 người; không ghi đồng thuận giả |
| Chạy trên máy thứ 2 | Chưa thực hiện; đã kiểm tra trên máy hiện tại |
| Hội đồng chấm 30 điểm | Chưa có; phiếu là phần chuẩn bị |
| Pilot và event ngoài thực tế | Mới là kế hoạch/đặc tả, chưa triển khai |
| Nộp LMS | Chưa thực hiện |

Deadline theo `SUBMISSION.md`: 23:59 GMT+7 ngày lab; ngày lab thực tế chưa được người học xác nhận, không tự gán bằng ngày soạn kế hoạch pilot.
