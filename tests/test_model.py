"""Module to test modeling capability
"""
import numpy as np
import pandas as pd
import pytest

from ds_lib_template.forecasting.model.naive import NaiveForecaster


@pytest.mark.parametrize("strategy", ["last", "mean"])
def test_model(strategy):
    """Basic tests for models."""
    forecaster = NaiveForecaster(strategy=strategy)
    index = pd.period_range(start="2017-01-01", end="2017-12-01", freq="M")
    data = pd.Series(np.arange(12), index=index)
    forecaster.fit(y=data)
    y_pred = forecaster.predict(fh=5)

    assert len(y_pred) == 5

    if strategy == "last":
        assert np.all(y_pred == data[-1])
    if strategy == "mean":
        assert np.all(y_pred == data.mean())
