"""Kiểm tra mô hình số: độc lập với bảng Markdown và không cần mạng."""
import math
import unittest
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal
from lab13 import (mo_hinh, so_lan_chay_ky_vong, ti_le_thanh_cong,
                   he_so_chi_phi_moi_viec_thanh_cong, co_mau, tinh_toan)


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parent
        cls.runs = pd.read_csv(root / 'logix_runs.csv')
        cls.reqs = pd.read_csv(root / 'logix_requests.csv', keep_default_na=False)
        cls.kq = tinh_toan(cls.runs, cls.reqs)

    def test_a1_and_boundaries(self):
        self.assertAlmostEqual(so_lan_chay_ky_vong(0.8, 2), 1.2)
        self.assertAlmostEqual(so_lan_chay_ky_vong(0.8), 1.25)
        self.assertAlmostEqual(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3), 1.25)
        self.assertEqual(so_lan_chay_ky_vong(0, 3), 3)
        self.assertEqual(ti_le_thanh_cong(0, 3), 0)
        self.assertEqual(ti_le_thanh_cong(1, 3), 1)
        self.assertTrue(math.isinf(he_so_chi_phi_moi_viec_thanh_cong(0, 3)))
        for p, k in ((-0.1, 2), (1.1, 2), (0.5, 0), (0.5, 1.5)):
            with self.assertRaises(ValueError):
                so_lan_chay_ky_vong(p, k)

    def test_known_trace_totals(self):
        a = self.kq['a2']
        self.assertEqual((len(self.runs), len(self.reqs)), (1624, 1200))
        self.assertAlmostEqual(a['token'], 245585.132, places=3)
        self.assertEqual(a['tool'], 84000)
        self.assertEqual(a['xem_lai'], 1780000)
        self.assertEqual(a['lam_lai'], 2264000)
        self.assertEqual(a['thanh_cong'], 978)
        self.assertAlmostEqual(a['tong'], 4373585.132, places=3)

    def test_failed_runs_paid_without_double_counting_retry(self):
        runs = pd.DataFrame(dict(request_id=['A', 'A', 'B'], attempt=[1, 2, 1],
                                 tokens_in=[1000, 1000, 1000], tokens_out=[0, 0, 0],
                                 tool_calls=[0, 0, 0], status=['loi', 'ok', 'ok']))
        reqs = pd.DataFrame(dict(request_id=['A'], so_lan_chay=[2], ket_qua=['thanh_cong'],
                                 phut_xem_lai_simulated=[0], phut_lam_lai_simulated=[0]))
        result = mo_hinh(runs, reqs)
        self.assertEqual(result['tong'], 52)  # 2 × 26; B excluded, retry not added twice.
        self.assertEqual(result['chay_lai'], 26)
        self.assertEqual(result['cps'], 52)
        cut = mo_hinh(runs, reqs, max_lan_chay=1)
        self.assertEqual(cut['tong'], 26)
        self.assertEqual(cut['thanh_cong'], 0)
        self.assertTrue(math.isinf(cut['cps']))

    def test_scenarios_do_not_mutate_input_and_partition_adds_up(self):
        before_r, before_q = self.runs.copy(deep=True), self.reqs.copy(deep=True)
        mo_hinh(self.runs, self.reqs, max_lan_chay=1)
        assert_frame_equal(self.runs, before_r)
        assert_frame_equal(self.reqs, before_q)
        self.assertAlmostEqual(sum(r['tong'] for r in self.kq['a3']), self.kq['a2']['tong'])
        self.assertEqual(sum(r['thanh_cong'] for r in self.kq['a3']), 978)

    def test_linearity_and_half_double_symmetry(self):
        a = self.kq['a2']['cps']
        b = self.kq['b1']
        for double, half in ((0, 1), (2, 3), (4, 5)):
            self.assertAlmostEqual(b[double]['cps'] - a, 2 * (a - b[half]['cps']))
        self.assertAlmostEqual(self.kq['b2']['cps'] - a,
                               (b[0]['cps'] - a) + (b[2]['cps'] - a))

    def test_retry_system_optimum_is_different(self):
        b = self.kq['b3']
        self.assertEqual([r['thanh_cong'] for r in b], [881, 966, 978])
        self.assertEqual(min(b, key=lambda r: r['system'])['cap'], 2)
        self.assertEqual(min(b, key=lambda r: r['cps'])['cap'], 1)

    def test_b4_and_metrics(self):
        b4, e = self.kq['b4'], self.kq['metrics']
        self.assertEqual((b4['n'], b4['ok'], b4['rework']), (982, 948, 48))
        self.assertAlmostEqual(b4['base'], (224513.274 + 9480000 + 864000) / 900, places=3)
        self.assertGreater(b4['observed'], 12000)
        self.assertEqual((e['primary'], e['ignored'], e['reviewed'], e['reopened']), (994, 48, 177, 51))

    def test_sample_size_and_cluster_ceiling(self):
        d = self.kq['d1']
        self.assertEqual((co_mau(.70, .75), co_mau(.70, .76)), (1251, 859))
        self.assertEqual((d['raw75'], d['staff75'], d['m']), (3103, 42, 299))
        self.assertGreater(d['effective'], 859)
        self.assertLess(20 * 298 / (1 + 297 * .02), 859)
        self.assertLess(d['staff_limit'], d['n5'])
        self.assertLess(d['power5'], .65)


if __name__ == '__main__':
    unittest.main()
