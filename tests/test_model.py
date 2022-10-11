"""Module to test modeling capability
"""

# import pytest
# from pandas.testing import assert_series_equal

import numpy as np
import pandas as pd
from ds_lib_template.forecasting.model.naive import NaiveForecaster

# from .utils import _load_deviation_classes, _load_ll_ul_outlier_data


def test_model():
    """Tests the deviation based outlier methods with both positive and negative outliers."""
    forecaster = NaiveForecaster()
    index = pd.period_range(start="2017-01-01", end="2017-12-01", freq="M")
    data = pd.Series(np.arange(12), index=index)
    forecaster.fit(y=data)
    y_pred = forecaster.predict(fh=5)

    assert len(y_pred) == 5
    assert np.all(y_pred == data[-1])
