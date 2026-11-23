# Bảng chi phí · CP1 và CP2 · Nhóm MEO

Sinh bằng `python lab13.py --write-cost-report` từ 2 CSV nguyên bản. Toàn bộ dữ liệu và bảng giá của lab là giả lập.
Mọi tổng, đơn giá, tỉ số hay phần trăm phụ thuộc phút nhân viên dưới đây đều mang nhãn **simulated**; chỉ làm tròn khi hiển thị.

## A1 · Ba phép thử

| Phép thử, p = 0,8 | Kết quả |
| --- | ---: |
| Trung bình, tối đa 2 lần | 1,20 · ĐẠT |
| Trung bình, đến khi đúng | 1,25 · ĐẠT |
| Hệ số chi phí, tối đa 3 lần | 1,25 · ĐẠT |

Giả định 3 phép thử: các lượt độc lập, cùng p; hệ số chi phí bằng 1/p, không suy diễn giả định này cho các lượt thử trong CSV.

## A2 · Mô hình từ trace

| Khoản | Giá trị | Nguồn | Nhãn |
| --- | ---: | --- | --- |
| Token | 245.585,13 | Token vào/ra mọi lượt | đo từ trace giả lập |
| Tool | 84.000,00 | 5.600 lượt × 15 đ | đo từ trace giả lập |
| Trong đó lượt 2 và 3 | 93.804,49 | attempt > 1; đã nằm trong token + tool | đo từ trace giả lập |
| Xem lại | 1.780.000,00 | 890 phút × 2.000 đ | simulated |
| Làm lại | 2.264.000,00 | 1.132 phút × 2.000 đ | simulated |
| Tổng chi phí | 4.373.585,13 | Token + tool + xem lại + làm lại | simulated |
| Số việc thành công | 978 | ket_qua == thanh_cong; đơn vị: yêu cầu | đếm từ CSV |
| Chi phí mỗi việc thành công | 4.471,97 | Tổng / 978 | simulated |
| Hoá đơn token + tool / yêu cầu | 274,65 | (Token + tool) / 1.200 | đo từ trace giả lập |

- Chi phí mỗi việc thành công / hoá đơn mỗi yêu cầu = **16,28 lần (simulated)**.
- Làm lại lớn nhất: **51,77% (simulated)**; xem lại 40,70%, tổng giờ nhân viên 92,46% (simulated).
- Mọi lượt lỗi vẫn phát sinh tiền nên thuộc tử số; chỉ 978 yêu cầu thành công thuộc mẫu số. Phần chạy lại không được cộng thêm lần thứ 2.

## A3 · Theo loại yêu cầu

| Loại | Yêu cầu | Thành công | Lượt/yêu cầu | CPS đ (simulated) | CPS/12.000 (simulated) |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 95,02% | 1,11 | 2.695,64 | 0,22× |
| hang_nang | 158 | 74,05% | 1,47 | 8.220,73 | 0,69× |
| quoc_te | 150 | 27,33% | 2,32 | 22.515,17 | 1,88× |
| doi_tac | 68 | 54,41% | 1,88 | 10.214,87 | 0,85× |

- Loại `quoc_te`: CPS 1,88× mức 12.000 đ (simulated), chỉ 27,33% thành công dù chạy 2,32 lần/yêu cầu; loại khỏi pilot.
- `doi_tac`: 54,41% thành công và điều khoản riêng; mức 0,85× (simulated) chưa đủ dư địa nên cũng loại. Chỉ chọn `noi_dia` + `hang_nang`.

| Loại | ok lượt 1 | ok lượt 2 | ok lượt 3 |
| --- | ---: | ---: | ---: |
| doi_tac | 51,47% | 18,18% | 14,81% |
| hang_nang | 70,89% | 39,13% | 17,86% |
| noi_dia | 91,02% | 75,68% | 38,89% |
| quoc_te | 30,00% | 11,43% | 2,15% |

- Với quốc tế, ok giảm từ 30,00% xuống 11,43% rồi 2,15%; chạy lại không chữa được nguyên nhân thiếu dữ liệu. Đây là tỉ lệ có điều kiện trên các ca còn phải thử, không phải tác động nhân quả của lượt chạy.

## A4 · Cộng cố định cho noi_dia + hang_nang

Theo quy ước đề: khối lượng là toàn bộ yêu cầu công ty; giữ cơ cấu mẫu, chỉ 982/1.200 vào phạm vi và 900/1.200 thành công trong phạm vi.
CPS biến đổi phạm vi = 3.072.513,27 / 900 = 3.413,90 đ (simulated); chi phí cố định giả định 40 triệu đ/tháng.

| Toàn công ty/tháng | Thành công trong phạm vi | Cố định/việc đ | CPS + cố định đ (simulated) | /12.000 (simulated) |
| --- | ---: | ---: | ---: | ---: |
| 45.000 | 33.750 | 1.185,19 | 4.599,09 | 0,38× |
| 22.500 | 16.875 | 2.370,37 | 5.784,27 | 0,48× |

- Cố định không đổi kết luận ở 45.000 hoặc 22.500 yêu cầu/tháng: CPS lần lượt 4.599 và 5.784 đ (simulated); chưa bao gồm nhân viên xử lý phần thất bại.

## B1 · Đổi từng yếu tố

| Kịch bản | Cách tính | CPS đ (simulated) | Thay đổi (simulated) |
| --- | --- | ---: | ---: |
| Giá token gấp đôi | 52 đ vào, 260 đ ra / 1.000 token | 4.723,08 | +5,62% |
| Giá token giảm một nửa | 13 đ vào, 65 đ ra / 1.000 token | 4.346,41 | -2,81% |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | 6.292,01 | +40,70% |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại × 0,5 | 3.561,95 | -20,35% |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | 6.786,90 | +51,77% |
| Số ca làm lại giảm một nửa | Tiền làm lại × 0,5 | 3.314,50 | -25,88% |
| Lương nhân viên tăng 25% | 2.500 đ/phút | 5.505,71 | +23,12% |
| Chỉ cho chạy tối đa 2 lần | Cắt lượt > 2, chuyển nhân viên, phút = 0 | 4.237,29 | -5,25% |
| Chỉ cho chạy 1 lần | Cắt lượt > 1, chuyển nhân viên, phút = 0 | 4.110,99 | -8,07% |

Hệ số xem/làm lại là độ nhạy tuyến tính của tiền, không mô phỏng lại kết quả đúng/sai hay bảo đảm tỉ lệ xem lại thực tế có thể tăng tùy ý.

## B2 · Một cặp và thứ hạng

- Token × 2 và xem lại × 2: **6.543,12 đ, +46,31% (simulated)**; tăng bằng tổng 2 tác động riêng vì không đổi mẫu số.
- Xếp hạng kịch bản B1: **1. Làm lại +51,77%; 2. Xem lại +40,70%; 3. Lương +23,12% (simulated)**; token chỉ +5,62% (simulated).

## B3 · Cả hệ thống

Theo quy ước B3: chi phí cả hệ thống = tổng trợ lý + 12.000 × (1.200 − thành công). Chưa cộng cố định.
Đây là phép tính bảo thủ của đề: phần làm lại đã có trong tổng trợ lý vẫn chịu khoản 12.000 đ bổ sung, không phải sổ chi phí thực đo không trùng lặp.

| Giới hạn | Tổng trợ lý đ (simulated) | Không thành công | Cả hệ thống đ (simulated) | CPS đ (simulated) |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | 3.621.780,64 | 319 | 7.449.780,64 | 4.110,99 |
| 2 lần | 4.093.220,23 | 234 | 6.901.220,23 | 4.237,29 |
| 3 lần | 4.373.585,13 | 222 | 7.037.585,13 | 4.471,97 |

- Rẻ nhất cho công ty là **2 lần: 6.901.220 đ (simulated)**; CPS thấp nhất là **1 lần: 4.111 đ (simulated)**, nhưng đẩy thêm 85 ca sang người so với 2 lần (97 so với 3 lần).

## B4 · Xem lại 100% trong phạm vi

Có 982 yêu cầu, 948 yêu cầu có ít nhất 1 lượt ok, 48 ca làm lại, 900 thành công. Xem lại mỗi yêu cầu ok 1 lần, không tính theo số lượt ok.

| Khoản / kịch bản | Giá trị (simulated) |
| --- | ---: |
| Token + tool, mọi lượt trong phạm vi (trace giả lập) | 224.513,27 đ |
| Xem lại: 948 × 5 × 2.000 | 9.480.000 đ |
| Làm lại giả định đề: 48 × 9 × 2.000 | 864.000 đ |
| CPS với làm lại 9 phút | 11.742,79 đ = 0,979× |
| Phút làm lại trung bình toàn mẫu, trung vị | 15,2973; 14,50 phút |
| CPS dùng trung bình chính xác của CSV | 12.414,50 đ = 1,035× |
| CPS dùng 15,3 phút theo hướng dẫn | 12.414,79 đ = 1,035× |
| Hoà vốn phút xem lại, làm lại 9 / trung bình CSV | 5,12 / 4,80 phút |

- Với 9 phút làm lại, CPS **11.743 đ = 0,979× (simulated)**; dùng 15,3 phút là **12.415 đ = 1,035× (simulated)**, đã vượt 12.000 đ dù chưa cộng cố định.
- Pilot phải đo phút thực và giảm xem lại an toàn: điểm hoà vốn **5,12 / 4,80 phút (simulated)**; xem lại 100% chỉ là kiểm soát ở bước đầu.

## So sánh cùng đơn vị với nhân viên

Toàn mẫu, theo B3: 7.037.585,13 / 1.200 = **5.864,65 đ/yêu cầu (simulated)**, chưa cố định.
- Trong phạm vi ở 45.000 yêu cầu toàn công ty/tháng: (3.072.513,27 + 82 × 12.000)/982 + 40 triệu/(45.000 × 982/1.200) = **5.217,09 đ/yêu cầu (simulated)**, gồm cố định; so với 12.000 đ/yêu cầu.
- Trong phạm vi ở 22.500 yêu cầu toàn công ty/tháng: (3.072.513,27 + 82 × 12.000)/982 + 40 triệu/(22.500 × 982/1.200) = **6.303,31 đ/yêu cầu (simulated)**, gồm cố định; so với 12.000 đ/yêu cầu.

Nguồn công thức và quy ước: `docs/du_lieu_va_cong_thuc.md`, đề gốc Lab 13 và `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`. Số tính lại từ CSV được ưu tiên khi đáp án tham khảo làm tròn khác vài đồng.
