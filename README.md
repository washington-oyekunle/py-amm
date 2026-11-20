# py-amm

Pure Python implementation of a Constant Product Automated Market Maker (x * y = k).

Features:
- Liquidity provision and removal
- Token swaps with configurable fee
- Slippage protection
- Integer-safe arithmetic (no floats for core math)
- Comprehensive unit tests
- Zero external dependencies for the core engine

## Why this project?

Demonstrates deep understanding of DeFi primitives, invariant-based pricing, and careful handling of precision in financial code — all in pure Python so the logic is fully auditable.

## Installation

```bash
git clone https://github.com/washington-oyekunle/py-amm.git
cd py-amm
python -m pytest tests/   # if pytest is installed
```

Or just copy `amm.py`.

## Quick Example

```python
from amm import AMM

pool = AMM(reserve_x=1_000_000, reserve_y=1_000_000, fee_bps=30)  # 0.3% fee
print(pool.get_price())  # 1.0

# Swap 10_000 of X for Y
amount_out, new_reserves = pool.swap_x_for_y(10_000, min_out=9900)
print(amount_out)
```

## Architecture

- `AMM` class maintains two reserves and a fee in basis points.
- All calculations use integers to avoid floating-point precision issues.
- Fee is deducted from the input amount before applying the constant product formula.
- Supports both directions of swaps and proportional liquidity operations.

## Running Tests

```bash
python -m unittest tests.test_amm
```

Or with pytest if available.

## License

MIT
