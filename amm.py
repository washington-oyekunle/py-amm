"""Pure Python Constant Product Automated Market Maker (x * y = k)."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple


@dataclass
class AMM:
    """Constant product AMM with integer reserves and basis-point fees.

    Invariant: reserve_x * reserve_y = k (adjusted for fees on swaps).
    All amounts are integers. Fee is taken from the input side.
    """

    reserve_x: int
    reserve_y: int
    fee_bps: int = 30  # 0.30% default (30 basis points)

    def __post_init__(self) -> None:
        if self.reserve_x <= 0 or self.reserve_y <= 0:
            raise ValueError("Reserves must be positive")
        if not 0 <= self.fee_bps < 10_000:
            raise ValueError("fee_bps must be in [0, 10000)")

    @property
    def k(self) -> int:
        return self.reserve_x * self.reserve_y

    def get_price(self) -> float:
        """Spot price of X in terms of Y (Y per X)."""
        return self.reserve_y / self.reserve_x

    def _apply_fee(self, amount_in: int) -> int:
        """Return amount after fee deduction."""
        if amount_in <= 0:
            raise ValueError("amount_in must be positive")
        fee = (amount_in * self.fee_bps) // 10_000
        return amount_in - fee

    def swap_x_for_y(self, amount_x_in: int, min_y_out: int = 0) -> Tuple[int, Tuple[int, int]]:
        """Swap X for Y. Returns (amount_y_out, (new_reserve_x, new_reserve_y))."""
        amount_x_in_after_fee = self._apply_fee(amount_x_in)
        # (reserve_x + amount_x_in_after_fee) * (reserve_y - amount_y_out) = k
        # amount_y_out = reserve_y - k / (reserve_x + amount_x_in_after_fee)
        new_reserve_x = self.reserve_x + amount_x_in_after_fee
        amount_y_out = self.reserve_y - (self.k // new_reserve_x)
        if amount_y_out < min_y_out:
            raise ValueError(f"Slippage: got {amount_y_out}, wanted at least {min_y_out}")
        if amount_y_out <= 0:
            raise ValueError("Insufficient output")
        self.reserve_x = new_reserve_x
        self.reserve_y -= amount_y_out
        return amount_y_out, (self.reserve_x, self.reserve_y)

    def swap_y_for_x(self, amount_y_in: int, min_x_out: int = 0) -> Tuple[int, Tuple[int, int]]:
        """Swap Y for X. Returns (amount_x_out, (new_reserve_x, new_reserve_y))."""
        amount_y_in_after_fee = self._apply_fee(amount_y_in)
        new_reserve_y = self.reserve_y + amount_y_in_after_fee
        amount_x_out = self.reserve_x - (self.k // new_reserve_y)
        if amount_x_out < min_x_out:
            raise ValueError(f"Slippage: got {amount_x_out}, wanted at least {min_x_out}")
        if amount_x_out <= 0:
            raise ValueError("Insufficient output")
        self.reserve_y = new_reserve_y
        self.reserve_x -= amount_x_out
        return amount_x_out, (self.reserve_x, self.reserve_y)

    def add_liquidity(self, amount_x: int, amount_y: int) -> Tuple[int, int]:
        """Add liquidity proportionally. Returns actual amounts added.

        Caller should compute optimal ratio externally if desired.
        This version adds the given amounts and updates k.
        """
        if amount_x <= 0 or amount_y <= 0:
            raise ValueError("Amounts must be positive")
        self.reserve_x += amount_x
        self.reserve_y += amount_y
        return amount_x, amount_y

    def remove_liquidity(self, shares_bps: int) -> Tuple[int, int]:
        """Remove liquidity by basis points of the pool (e.g. 5000 = 50%).

        Returns (amount_x_out, amount_y_out).
        """
        if not 0 < shares_bps <= 10_000:
            raise ValueError("shares_bps must be in (0, 10000]")
        amount_x = (self.reserve_x * shares_bps) // 10_000
        amount_y = (self.reserve_y * shares_bps) // 10_000
        self.reserve_x -= amount_x
        self.reserve_y -= amount_y
        return amount_x, amount_y

    def __repr__(self) -> str:
        return f"AMM(x={self.reserve_x}, y={self.reserve_y}, fee={self.fee_bps}bps)"
