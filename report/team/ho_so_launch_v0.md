# Hồ sơ launch v0 · LogiX-VN · Gate 2a

**Nhóm MEO · L3A.** Đề xuất pilot, chưa có phê duyệt. Dữ liệu lab giả lập; các số phụ thuộc phút nhân viên ghi **simulated**.

| Mục | Con số chính và bằng chứng | Trạng thái | Vai phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí/việc thành công | Toàn mẫu **4.471,97 đ**; phạm vi **3.413,90 đ**, chưa cố định; **simulated** ([A2–A3](bang_chi_phi.md)) | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | Làm lại **+51,77%**, xem lại **+40,70%**, lương **+23,12%**, toàn mẫu B1; **simulated** | Giả lập | PM trợ lý hoàn phí |
| 3 · So với tự làm | Chỉ nội địa + hàng nặng; CPS gồm cố định **4.599,09 đ** ở 45.000 yêu cầu toàn công ty/tháng; cùng đơn vị toàn hệ thống **5.217,09 đ/yêu cầu** so 12.000 đ; **simulated** | Giả lập | Giám đốc vận hành |
| 4 · Chỉ số chính / dùng / an toàn | **994/1.200=82,83%**; bỏ qua **48/177=27,12%**; mở lại **51/1.200=4,25%**; 15 event đã đặc tả, chưa triển khai ([chỉ số](chi_so.md)) | Xong, có bằng chứng | Trưởng phân tích |
| 5 · Lỗi và khắc phục | Phân tích **20 ca, 5 loại**, 5 biện pháp; chờ 2 bộ nhãn độc lập và duyệt chéo ([bảng lỗi](bang_loi.md)) | Chưa | QA nghiệp vụ |
| 6 · Pilot plan | **20+20 nhân viên**, **299** yêu cầu/người, **5.980** thô/nhánh, DE **6,96**, hiệu dụng **859,20**; MDE **6 điểm**, power ở 5 điểm chỉ **0,642**; quyết định **05/01/2027** ([kế hoạch](pilot_plan.yaml)) | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Xem lại 100%: **11.742,79–12.414,50 đ/việc**, chưa cố định, **simulated**; luật dừng CPS >8.000 đ/2 tuần, mở lại >6% hoặc chênh ≥2 điểm/3 lần kiểm tra; hoàn trùng ≥1 ca dừng ngay | Giả lập | Trưởng nhóm CSKH |

**Điều kiện trước pilot:** Kỹ sư trưởng chứng minh chống hoàn trùng, ledger trước xác nhận và rollback ≤30 phút; GĐ vận hành ký chấp nhận MDE 6 điểm và xác minh đủ 40 nhân viên; hạn **27/11/2026**. Nếu không đủ điều kiện thì chưa mở pilot.

**Điều kiện dữ liệu:** Trưởng phân tích bật event, khóa ngưỡng/seed trước **27/11/2026**; Trưởng CSKH thay phút simulated bằng đo thật, kiểm tra kinh tế và gate giảm review trước **07/12/2026**. Thiếu mẫu hoặc không đủ theo dõi thì chưa kết luận; không tự xem hiệu quả để dừng sớm.

**Đề xuất: Go có điều kiện** cho pilot `noi_dia` + `hang_nang`; loại `quoc_te` CPS 1,88× và `doi_tac` thành công 54,41% (CPS simulated); chỉ thực hiện sau khi các điều kiện trên được xác nhận.
