"""Unit tests for the AMM."""

import unittest
from amm import AMM


class TestAMM(unittest.TestCase):
    def setUp(self) -> None:
        self.pool = AMM(reserve_x=1_000_000, reserve_y=1_000_000, fee_bps=30)

    def test_initial_state(self) -> None:
        self.assertEqual(self.pool.reserve_x, 1_000_000)
        self.assertEqual(self.pool.reserve_y, 1_000_000)
        self.assertAlmostEqual(self.pool.get_price(), 1.0)

    def test_swap_x_for_y(self) -> None:
        amount_out, _ = self.pool.swap_x_for_y(10_000)
        self.assertGreater(amount_out, 0)
        self.assertLess(amount_out, 10_000)  # due to fee and slippage
        self.assertEqual(self.pool.reserve_x, 1_000_000 + 10_000 - (10_000 * 30 // 10_000))

    def test_swap_round_trip_loses_to_fees(self) -> None:
        # Swap X->Y then Y->X should not profit
        y_out, _ = self.pool.swap_x_for_y(50_000)
        x_out, _ = self.pool.swap_y_for_x(y_out)
        self.assertLess(x_out, 50_000)

    def test_slippage_protection(self) -> None:
        with self.assertRaises(ValueError):
            self.pool.swap_x_for_y(10_000, min_y_out=20_000)

    def test_add_and_remove_liquidity(self) -> None:
        self.pool.add_liquidity(100_000, 100_000)
        self.assertEqual(self.pool.reserve_x, 1_100_000)
        x_out, y_out = self.pool.remove_liquidity(10_000)  # 100%
        self.assertEqual(x_out, 1_100_000)
        self.assertEqual(y_out, 1_100_000)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            AMM(0, 1000)
        with self.assertRaises(ValueError):
            self.pool.swap_x_for_y(0)


if __name__ == "__main__":
    unittest.main()
