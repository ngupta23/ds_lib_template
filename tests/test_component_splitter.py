"""Module to test prediction component splitter functionality
"""

import numpy as np
import pandas as pd

from ds_lib_template.forecasting.components.dummy import DummyForecastingComponent
from ds_lib_template.forecasting.model.naive import NaiveForecaster


def test_component_splitter():
    """Basic tests for component splitters."""
    index = pd.period_range(start="2017-01-01", end="2017-12-01", freq="M")
    data = pd.Series(np.arange(12), index=index)

    model = NaiveForecaster()
    model.fit(y=data)

    # Only returns "trend" & "seasonality" ----
    component_splitter = DummyForecastingComponent(model=model)
    y_pred, components = component_splitter.predict(fh=4)
    assert len(y_pred) == 4
    assert components.shape[0] == 4
    assert components.shape[1] == 2

    # Only returns "trend", "seasonality", and impact of drivers ----
    component_splitter = DummyForecastingComponent(model=model, drivers=["A", "B", "C"])
    y_pred, components = component_splitter.predict(fh=4)
    assert len(y_pred) == 4
    assert components.shape[0] == 4
    assert components.shape[1] == 5

    # Only returns "trend", "seasonality", and impact of holidays ----
    component_splitter = DummyForecastingComponent(model=model, holidays=["USHols"])
    y_pred, components = component_splitter.predict(fh=4)
    assert len(y_pred) == 4
    assert components.shape[0] == 4
    assert components.shape[1] == 3

    # Only returns "trend", "seasonality", and impact of drivers and holidays ----
    component_splitter = DummyForecastingComponent(
        model=model, drivers=["A", "B", "C"], holidays=["USHols"]
    )
    y_pred, components = component_splitter.predict(fh=4)
    assert len(y_pred) == 4
    assert components.shape[0] == 4
    assert components.shape[1] == 6
