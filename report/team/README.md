# Hồ sơ Lab 13 · Nhóm MEO

Bắt đầu từ [hồ sơ launch v0](ho_so_launch_v0.md) và [báo cáo nhóm](group_report.md). Kết luận đề xuất là **Go có điều kiện** cho pilot nội địa + hàng nặng.

| CP | Sản phẩm | Trạng thái |
| --- | --- | --- |
| CP1 | [A1–A4](bang_chi_phi.md), [code](../../src/lab13.py) | Đã tính từ CSV; 3 phép thử bắt buộc đạt |
| CP2 | [B1–B4](bang_chi_phi.md) | Đủ 9 kịch bản, 1 cặp, giới hạn chạy và xem lại 100% |
| CP3 | [20 ca và 5 cách khắc phục](bang_loi.md) | Đã phân tích có nguồn; chưa có 2 người gắn nhãn độc lập |
| CP4 | [pilot_plan.yaml](pilot_plan.yaml) | Đủ D1–D2, 4 luật dừng; YAML đọc được |
| CP5 | [chỉ số/event/rủi ro](chi_so.md), [hồ sơ 7 mục](ho_so_launch_v0.md) | Đã soạn; pilot/event mới là đề xuất |
| Duyệt chéo | [phiếu và câu hỏi bảo vệ](phieu_cham.md) | Đã chuẩn bị; chưa có điểm hoặc quyết định hội đồng |

Thành viên: **Đỗ Minh Hoàng — 2A202603554**. Thông tin nhóm ở [TEAM.md](../../TEAM.md); [báo cáo thành viên](2A202603554_DoMinhHoang.md) đã được đặt tên theo quy định. `MSSV_HoTen.md` là file mẫu.

Code đã qua **8 unittest**, CSV và starter giữ nguyên. Lệnh kiểm tra có trong [báo cáo thành viên](2A202603554_DoMinhHoang.md). Bảng chi phí sinh lại bằng `python lab13.py --write-cost-report` trong `src/` sau khi cài `requirements.txt`.

Cần hoàn tất hai bộ nhãn độc lập và tỉ lệ đồng thuận ở CP3, kết quả duyệt chéo Gate 2a, sau đó push bản chốt và nộp link repo trên LMS.
