from pathlib import Path

import numpy as np
import pandas as pd

CSV_PATH = Path(__file__).with_name("monthly_sales.csv")


def load_monthly_sales() -> pd.DataFrame:
    """Load monthly sales and add month-over-month growth as a decimal."""
    sales = pd.read_csv(CSV_PATH, parse_dates=["month"])
    sales["revenue"] = pd.to_numeric(sales["revenue"], errors="raise")
    sales = sales.sort_values("month").reset_index(drop=True)

    revenue = sales["revenue"].to_numpy(dtype=float)
    growth = np.full(revenue.size, np.nan, dtype=float)
    if revenue.size > 1:
        previous = revenue[:-1]
        growth[1:] = np.divide(
            np.diff(revenue),
            previous,
            out=np.zeros(previous.size, dtype=float),
            where=previous != 0,
        )
    sales["growth"] = growth
    return sales
