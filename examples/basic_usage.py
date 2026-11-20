"""Basic usage examples for py-amm."""

from amm import AMM


def main() -> None:
    print("=== py-amm Constant Product AMM Demo ===\n")

    pool = AMM(reserve_x=1_000_000, reserve_y=2_000_000, fee_bps=30)
    print(f"Initial pool: {pool}")
    print(f"Spot price (Y per X): {pool.get_price():.4f}\n")

    # Swap 10k X for Y
    y_out, _ = pool.swap_x_for_y(10_000, min_y_out=19_000)
    print(f"Swapped 10,000 X → {y_out} Y")
    print(f"New pool: {pool}\n")

    # Add liquidity
    pool.add_liquidity(50_000, 100_000)
    print(f"After adding liquidity: {pool}\n")

    # Remove 10% of liquidity
    x_out, y_out = pool.remove_liquidity(1_000)  # 10%
    print(f"Removed 10% liquidity: {x_out} X and {y_out} Y")
    print(f"Final pool: {pool}")


if __name__ == "__main__":
    main()
