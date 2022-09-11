import pandas as pd
import pytest


@pytest.fixture(scope="session", name="no_outlier_data")
def no_outlier_data():
    """Load dataset not containing any outliers."""
    return pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
