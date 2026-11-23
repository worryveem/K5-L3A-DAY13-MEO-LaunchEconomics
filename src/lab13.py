"""Lab 13 · Gate 2a · Nhóm MEO; triển khai có Codex hỗ trợ.
Chạy trong src/: python lab13.py; sinh bảng A/B: python lab13.py --write-cost-report.
Không cần API hoặc mạng. Dữ liệu CSV và bảng giá đều là giả định lab.
Giữ nguyên bản gốc lab13_starter.py và hai CSV.
"""
import math
import argparse
from pathlib import Path
from statistics import NormalDist
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# CP1: ba hàm kinh tế của việc chạy lại, giả định độc lập cùng p.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    _kiem_tra_pk(p, k)
    if p == 0:
        return math.inf if k is None else float(k)
    if k is None:
        return 1 / p
    return ti_le_thanh_cong(p, k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    _kiem_tra_pk(p, k)
    if p == 0:
        return 0.0
    if p == 1 or k is None:
        return 1.0
    return -math.expm1(k * math.log1p(-p))


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    rate = ti_le_thanh_cong(p, k)
    return so_lan_chay_ky_vong(p, k) / rate if rate else math.inf


def _kiem_tra_pk(p, k):
    if not 0 <= p <= 1:
        raise ValueError('p phải thuộc [0, 1]')
    if k is not None and (isinstance(k, bool) or not isinstance(k, int) or k < 1):
        raise ValueError('k phải là số nguyên dương hoặc None')


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# CP1: mo_hinh; CP2 gọi lại với giá và hệ số thay đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    if max_lan_chay is not None:
        _kiem_tra_pk(1, max_lan_chay)
    if any(v < 0 or not math.isfinite(v) for v in
           (gia_vao, gia_ra, gia_tool, luong_phut, he_so_xem_lai, he_so_lam_lai)):
        raise ValueError('Giá và hệ số phải hữu hạn, không âm')
    reqs = reqs.copy()
    runs = runs[runs.request_id.isin(reqs.request_id)]
    if max_lan_chay is not None:
        runs = runs[runs.attempt <= max_lan_chay]
        vuot = reqs.so_lan_chay > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    token = runs.tokens_in / 1000 * gia_vao + runs.tokens_out / 1000 * gia_ra
    tool = runs.tool_calls * gia_tool
    xem_lai = float(reqs.phut_xem_lai_simulated.sum() * luong_phut * he_so_xem_lai)
    lam_lai = float(reqs.phut_lam_lai_simulated.sum() * luong_phut * he_so_lam_lai)
    tong = float(token.sum() + tool.sum() + xem_lai + lam_lai)
    thanh_cong = int(reqs.ket_qua.eq('thanh_cong').sum())
    return dict(token=float(token.sum()), tool=float(tool.sum()),
                chay_lai=float((token + tool)[runs.attempt > 1].sum()),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong, thanh_cong=thanh_cong,
                cps=tong / thanh_cong if thanh_cong else math.inf,
                hoa_don_moi_yc=float((token.sum() + tool.sum()) / len(reqs)) if len(reqs) else math.nan)


PHAM_VI = ('noi_dia', 'hang_nang')
CO_DINH = 40_000_000


def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Công thức hai tỉ lệ với z chính xác của lab; làm tròn lên."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def tinh_toan(runs, reqs):
    a2 = mo_hinh(runs, reqs)
    a3 = []
    for loai in ('noi_dia', 'hang_nang', 'quoc_te', 'doi_tac'):
        q = reqs[reqs.loai == loai]
        r = runs[runs.request_id.isin(q.request_id)]
        kq = mo_hinh(runs, q)
        a3.append(dict(loai=loai, n=len(q), rate=kq['thanh_cong'] / len(q),
                       attempts=len(r) / len(q), **kq))
    scope = reqs[reqs.loai.isin(PHAM_VI)]
    scoped = mo_hinh(runs, scope)
    a4 = []
    for volume in (45000, 22500):
        successes = volume * scoped['thanh_cong'] / len(reqs)
        fixed = CO_DINH / successes
        a4.append(dict(volume=volume, successes=successes, fixed=fixed, cps=scoped['cps'] + fixed))
    scenarios = [
        ('Giá token gấp đôi', '52 đ vào, 260 đ ra / 1.000 token', dict(gia_vao=52, gia_ra=260)),
        ('Giá token giảm một nửa', '13 đ vào, 65 đ ra / 1.000 token', dict(gia_vao=13, gia_ra=65)),
        ('Tỉ lệ xem lại gấp đôi', 'Tiền xem lại × 2', dict(he_so_xem_lai=2)),
        ('Tỉ lệ xem lại giảm một nửa', 'Tiền xem lại × 0,5', dict(he_so_xem_lai=0.5)),
        ('Số ca làm lại gấp đôi', 'Tiền làm lại × 2', dict(he_so_lam_lai=2)),
        ('Số ca làm lại giảm một nửa', 'Tiền làm lại × 0,5', dict(he_so_lam_lai=0.5)),
        ('Lương nhân viên tăng 25%', '2.500 đ/phút', dict(luong_phut=2500)),
        ('Chỉ cho chạy tối đa 2 lần', 'Cắt lượt > 2, chuyển nhân viên, phút = 0', dict(max_lan_chay=2)),
        ('Chỉ cho chạy 1 lần', 'Cắt lượt > 1, chuyển nhân viên, phút = 0', dict(max_lan_chay=1)),
    ]
    b1 = []
    for name, formula, kw in scenarios:
        result = mo_hinh(runs, reqs, **kw)
        b1.append(dict(name=name, formula=formula, delta=100 * (result['cps'] / a2['cps'] - 1), **result))
    b2 = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)
    b3 = []
    for cap in (1, 2, 3):
        result = mo_hinh(runs, reqs, max_lan_chay=cap)
        failed = len(reqs) - result['thanh_cong']
        b3.append(dict(cap=cap, failed=failed, system=result['tong'] + BASELINE * failed, **result))
    sruns = runs[runs.request_id.isin(scope.request_id)]
    ok = sruns.loc[sruns.status == 'ok', 'request_id'].nunique()
    rework = int(scope.ket_qua.eq('lam_lai').sum())
    minutes = reqs.loc[reqs.ket_qua == 'lam_lai', 'phut_lam_lai_simulated']
    b4 = dict(n=len(scope), ok=ok, rework=rework, token_tool=scoped['token'] + scoped['tool'],
              review=ok * 5 * LUONG_PHUT, mean_rework=float(minutes.mean()),
              median_rework=float(minutes.median()))
    for key, minute in (('base', 9), ('observed', b4['mean_rework']), ('rounded', 15.3)):
        total = b4['token_tool'] + b4['review'] + rework * minute * LUONG_PHUT
        b4[key] = total / scoped['thanh_cong']
        b4[key + '_breakeven'] = (BASELINE * scoped['thanh_cong'] - b4['token_tool']
                                   - rework * minute * LUONG_PHUT) / (ok * LUONG_PHUT)
    reviewed = reqs[reqs.duoc_xem_lai == 1]
    metrics = dict(n=len(reqs), primary=int(((reqs.dong_trong_24h == 1) & (reqs.mo_lai_trong_7_ngay == 0)).sum()),
                   reviewed=len(reviewed), ignored=int(reviewed.quyet_dinh_xem_lai.isin(['sua', 'bo']).sum()),
                   reopened=int(reqs.mo_lai_trong_7_ngay.sum()), scope_n=len(scope),
                   scope_reopened=int(scope.mo_lai_trong_7_ngay.sum()), scope_rework=rework)
    n5, n6 = co_mau(0.70, 0.75), co_mau(0.70, 0.76)
    de75 = 1 + 74 * 0.02
    m = math.ceil(n6 * (1 - 0.02) / (20 - n6 * 0.02))
    de = 1 + (m - 1) * 0.02
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower
    power5 = NormalIndPower().power(effect_size=proportion_effectsize(0.75, 0.70),
                                   nobs1=20 * m / de, alpha=0.05, ratio=1)
    d1 = dict(n5=n5, n6=n6, de75=de75, raw75=math.ceil(n5 * de75),
              staff75=math.ceil(n5 * de75 / 75), staff_limit=20 / 0.02,
              depot_limit=6 / 0.02, m=m, de=de, effective=20 * m / de,
              raw=20 * m, power5=float(power5))
    attempt_ok = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    attempt_ok['ok'] = attempt_ok.status.eq('ok')
    attempt_ok = attempt_ok.groupby(['loai', 'attempt']).ok.mean().unstack()
    return dict(a2=a2, a3=a3, a4=a4, b1=b1, b2=b2, b3=b3, b4=b4,
                scope=scoped, metrics=metrics, d1=d1, attempt_ok=attempt_ok)


def so(x, decimals=0):
    return f'{x:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


def bang_chi_phi(kq):
    a, scope, b4 = kq['a2'], kq['scope'], kq['b4']
    lines = ['# Bảng chi phí · CP1 và CP2 · Nhóm MEO', '',
             'Sinh bằng `python lab13.py --write-cost-report` từ 2 CSV nguyên bản. Toàn bộ dữ liệu và bảng giá của lab là giả lập.',
             'Mọi tổng, đơn giá, tỉ số hay phần trăm phụ thuộc phút nhân viên dưới đây đều mang nhãn **simulated**; chỉ làm tròn khi hiển thị.', '',
             '## A1 · Ba phép thử', '', '| Phép thử, p = 0,8 | Kết quả |', '| --- | ---: |',
             '| Trung bình, tối đa 2 lần | 1,20 · ĐẠT |', '| Trung bình, đến khi đúng | 1,25 · ĐẠT |',
             '| Hệ số chi phí, tối đa 3 lần | 1,25 · ĐẠT |', '',
             'Giả định 3 phép thử: các lượt độc lập, cùng p; hệ số chi phí bằng 1/p, không suy diễn giả định này cho các lượt thử trong CSV.', '',
             '## A2 · Mô hình từ trace', '', '| Khoản | Giá trị | Nguồn | Nhãn |', '| --- | ---: | --- | --- |']
    rows = [('Token', a['token'], 'Token vào/ra mọi lượt', 'đo từ trace giả lập'),
            ('Tool', a['tool'], '5.600 lượt × 15 đ', 'đo từ trace giả lập'),
            ('Trong đó lượt 2 và 3', a['chay_lai'], 'attempt > 1; đã nằm trong token + tool', 'đo từ trace giả lập'),
            ('Xem lại', a['xem_lai'], '890 phút × 2.000 đ', 'simulated'),
            ('Làm lại', a['lam_lai'], '1.132 phút × 2.000 đ', 'simulated'),
            ('Tổng chi phí', a['tong'], 'Token + tool + xem lại + làm lại', 'simulated'),
            ('Số việc thành công', a['thanh_cong'], 'ket_qua == thanh_cong; đơn vị: yêu cầu', 'đếm từ CSV'),
            ('Chi phí mỗi việc thành công', a['cps'], 'Tổng / 978', 'simulated'),
            ('Hoá đơn token + tool / yêu cầu', a['hoa_don_moi_yc'], '(Token + tool) / 1.200', 'đo từ trace giả lập')]
    for title, value, source, label in rows:
        lines.append(f"| {title} | {so(value, 2) if title != 'Số việc thành công' else so(value)} | {source} | {label} |")
    lines += ['', f"- Chi phí mỗi việc thành công / hoá đơn mỗi yêu cầu = **{so(a['cps']/a['hoa_don_moi_yc'],2)} lần (simulated)**.",
              f"- Làm lại lớn nhất: **{so(100*a['lam_lai']/a['tong'],2)}% (simulated)**; xem lại {so(100*a['xem_lai']/a['tong'],2)}%, tổng giờ nhân viên {so(100*(a['xem_lai']+a['lam_lai'])/a['tong'],2)}% (simulated).",
              '- Mọi lượt lỗi vẫn phát sinh tiền nên thuộc tử số; chỉ 978 yêu cầu thành công thuộc mẫu số. Phần chạy lại không được cộng thêm lần thứ 2.', '',
              '## A3 · Theo loại yêu cầu', '', '| Loại | Yêu cầu | Thành công | Lượt/yêu cầu | CPS đ (simulated) | CPS/12.000 (simulated) |',
              '| --- | ---: | ---: | ---: | ---: | ---: |']
    for r in kq['a3']:
        lines.append(f"| {r['loai']} | {r['n']} | {so(r['rate']*100,2)}% | {so(r['attempts'],2)} | {so(r['cps'],2)} | {so(r['cps']/BASELINE,2)}× |")
    lines += ['', '- Loại `quoc_te`: CPS 1,88× mức 12.000 đ (simulated), chỉ 27,33% thành công dù chạy 2,32 lần/yêu cầu; loại khỏi pilot.',
              '- `doi_tac`: 54,41% thành công và điều khoản riêng; mức 0,85× (simulated) chưa đủ dư địa nên cũng loại. Chỉ chọn `noi_dia` + `hang_nang`.',
              '', '| Loại | ok lượt 1 | ok lượt 2 | ok lượt 3 |', '| --- | ---: | ---: | ---: |']
    for loai, r in kq['attempt_ok'].iterrows():
        lines.append(f"| {loai} | {so(r[1]*100,2)}% | {so(r[2]*100,2)}% | {so(r[3]*100,2)}% |")
    lines += ['', '- Với quốc tế, ok giảm từ 30,00% xuống 11,43% rồi 2,15%; chạy lại không chữa được nguyên nhân thiếu dữ liệu. Đây là tỉ lệ có điều kiện trên các ca còn phải thử, không phải tác động nhân quả của lượt chạy.', '',
              '## A4 · Cộng cố định cho noi_dia + hang_nang', '',
              'Theo quy ước đề: khối lượng là toàn bộ yêu cầu công ty; giữ cơ cấu mẫu, chỉ 982/1.200 vào phạm vi và 900/1.200 thành công trong phạm vi.',
              f"CPS biến đổi phạm vi = {so(scope['tong'],2)} / 900 = {so(scope['cps'],2)} đ (simulated); chi phí cố định giả định 40 triệu đ/tháng.", '',
              '| Toàn công ty/tháng | Thành công trong phạm vi | Cố định/việc đ | CPS + cố định đ (simulated) | /12.000 (simulated) |',
              '| --- | ---: | ---: | ---: | ---: |']
    for r in kq['a4']:
        lines.append(f"| {so(r['volume'])} | {so(r['successes'])} | {so(r['fixed'],2)} | {so(r['cps'],2)} | {so(r['cps']/BASELINE,2)}× |")
    lines += ['', '- Cố định không đổi kết luận ở 45.000 hoặc 22.500 yêu cầu/tháng: CPS lần lượt 4.599 và 5.784 đ (simulated); chưa bao gồm nhân viên xử lý phần thất bại.',
              '', '## B1 · Đổi từng yếu tố', '', '| Kịch bản | Cách tính | CPS đ (simulated) | Thay đổi (simulated) |', '| --- | --- | ---: | ---: |']
    for r in kq['b1']:
        lines.append(f"| {r['name']} | {r['formula']} | {so(r['cps'],2)} | {'+' if r['delta']>0 else ''}{so(r['delta'],2)}% |")
    lines += ['', 'Hệ số xem/làm lại là độ nhạy tuyến tính của tiền, không mô phỏng lại kết quả đúng/sai hay bảo đảm tỉ lệ xem lại thực tế có thể tăng tùy ý.', '',
              '## B2 · Một cặp và thứ hạng', '',
              f"- Token × 2 và xem lại × 2: **{so(kq['b2']['cps'],2)} đ, +{so(100*(kq['b2']['cps']/a['cps']-1),2)}% (simulated)**; tăng bằng tổng 2 tác động riêng vì không đổi mẫu số.",
              f"- Xếp hạng kịch bản B1: **1. Làm lại +{so(kq['b1'][4]['delta'],2)}%; 2. Xem lại +{so(kq['b1'][2]['delta'],2)}%; 3. Lương +{so(kq['b1'][6]['delta'],2)}% (simulated)**; token chỉ +{so(kq['b1'][0]['delta'],2)}% (simulated).", '',
              '## B3 · Cả hệ thống', '',
              'Theo quy ước B3: chi phí cả hệ thống = tổng trợ lý + 12.000 × (1.200 − thành công). Chưa cộng cố định.',
              'Đây là phép tính bảo thủ của đề: phần làm lại đã có trong tổng trợ lý vẫn chịu khoản 12.000 đ bổ sung, không phải sổ chi phí thực đo không trùng lặp.', '',
              '| Giới hạn | Tổng trợ lý đ (simulated) | Không thành công | Cả hệ thống đ (simulated) | CPS đ (simulated) |', '| --- | ---: | ---: | ---: | ---: |']
    for r in kq['b3']:
        lines.append(f"| {r['cap']} lần | {so(r['tong'],2)} | {r['failed']} | {so(r['system'],2)} | {so(r['cps'],2)} |")
    lines += ['', '- Rẻ nhất cho công ty là **2 lần: 6.901.220 đ (simulated)**; CPS thấp nhất là **1 lần: 4.111 đ (simulated)**, nhưng đẩy thêm 85 ca sang người so với 2 lần (97 so với 3 lần).', '',
              '## B4 · Xem lại 100% trong phạm vi', '',
              f"Có {b4['n']} yêu cầu, {b4['ok']} yêu cầu có ít nhất 1 lượt ok, {b4['rework']} ca làm lại, {scope['thanh_cong']} thành công. Xem lại mỗi yêu cầu ok 1 lần, không tính theo số lượt ok.", '',
              '| Khoản / kịch bản | Giá trị (simulated) |', '| --- | ---: |',
              f"| Token + tool, mọi lượt trong phạm vi (trace giả lập) | {so(b4['token_tool'],2)} đ |",
              f"| Xem lại: 948 × 5 × 2.000 | {so(b4['review'])} đ |",
              f"| Làm lại giả định đề: 48 × 9 × 2.000 | {so(48*9*2000)} đ |",
              f"| CPS với làm lại 9 phút | {so(b4['base'],2)} đ = {so(b4['base']/BASELINE,3)}× |",
              f"| Phút làm lại trung bình toàn mẫu, trung vị | {so(b4['mean_rework'],4)}; {so(b4['median_rework'],2)} phút |",
              f"| CPS dùng trung bình chính xác của CSV | {so(b4['observed'],2)} đ = {so(b4['observed']/BASELINE,3)}× |",
              f"| CPS dùng 15,3 phút theo hướng dẫn | {so(b4['rounded'],2)} đ = {so(b4['rounded']/BASELINE,3)}× |",
              f"| Hoà vốn phút xem lại, làm lại 9 / trung bình CSV | {so(b4['base_breakeven'],2)} / {so(b4['observed_breakeven'],2)} phút |", '',
              f"- Với 9 phút làm lại, CPS **{so(b4['base'])} đ = {so(b4['base']/BASELINE,3)}× (simulated)**; dùng 15,3 phút là **{so(b4['rounded'])} đ = {so(b4['rounded']/BASELINE,3)}× (simulated)**, đã vượt 12.000 đ dù chưa cộng cố định.",
              f"- Pilot phải đo phút thực và giảm xem lại an toàn: điểm hoà vốn **{so(b4['base_breakeven'],2)} / {so(b4['observed_breakeven'],2)} phút (simulated)**; xem lại 100% chỉ là kiểm soát ở bước đầu.", '',
              '## So sánh cùng đơn vị với nhân viên', '',
              f"Toàn mẫu, theo B3: {so(kq['b3'][2]['system'],2)} / 1.200 = **{so(kq['b3'][2]['system']/1200,2)} đ/yêu cầu (simulated)**, chưa cố định."]
    for volume in (45000, 22500):
        system_per_request = (scope['tong'] + (982 - 900) * BASELINE) / 982 + CO_DINH / (volume * 982 / 1200)
        lines.append(f"- Trong phạm vi ở {so(volume)} yêu cầu toàn công ty/tháng: ({so(scope['tong'],2)} + 82 × 12.000)/982 + 40 triệu/({so(volume)} × 982/1.200) = **{so(system_per_request,2)} đ/yêu cầu (simulated)**, gồm cố định; so với 12.000 đ/yêu cầu.")
    lines += ['', 'Nguồn công thức và quy ước: `docs/du_lieu_va_cong_thuc.md`, đề gốc Lab 13 và `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`. Số tính lại từ CSV được ưu tiên khi đáp án tham khảo làm tròn khác vài đồng.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Tính các bảng CP1, CP2, CP4, CP5 từ dữ liệu lab.')
    parser.add_argument('--write-cost-report', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    runs = pd.read_csv(root / 'logix_runs.csv')
    reqs = pd.read_csv(root / 'logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    kq = tinh_toan(runs, reqs)
    report = bang_chi_phi(kq)
    print(report)
    print('D1 · Cỡ mẫu (baseline/ICC là giả định lab)')
    for name, value in kq['d1'].items():
        print(f'{name:18s} {value:,.6f}')
    print('E1 · Đếm chỉ số (trace giả lập):', kq['metrics'])
    print('Phạm vi, giới hạn 2 lần (chi phí simulated):', mo_hinh(runs, reqs[reqs.loai.isin(PHAM_VI)], max_lan_chay=2))
    if args.write_cost_report:
        target = root.parent / 'report/team/bang_chi_phi.md'
        target.write_text(report, encoding='utf-8')
        print('Đã ghi:', target)


if __name__ == '__main__':
    main()
