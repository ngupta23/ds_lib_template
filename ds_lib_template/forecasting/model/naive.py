from typing import Optional

import pandas as pd

from ds_lib_template.forecasting.model.base import BaseForecaster


class NaiveForecaster(BaseForecaster):
    def __init__(self, strategy: str = "last"):
        """Initializes the Naive Forecaster

        Parameters
        ----------
        strategy : str, optional
            The strategy to use for the Naive Forecaster, by default "last"
            "last": Forecast = last known value for all period
            "mean": Forecast = mean for all historical data
        """
        self.strategy = strategy

        super(NaiveForecaster, self).__init__()

    def _fit(
        self, y: pd.Series, X: Optional[pd.DataFrame] = None, fh: Optional[int] = None
    ) -> "BaseForecaster":
        """Fit to training data.

        Parameters
        ----------
        y : pd.Series
            Target time series to which to fit the forecaster.
        X : pd.DataFrame, optional
            Exogenous variables, by default None
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None

        Returns
        -------
        BaseForecaster
            Returns an instance of self for chaining
        """

        return self

    def _predict(
        self, fh: Optional[int] = None, X: Optional[pd.DataFrame] = None
    ) -> pd.Series:
        """Forecast time series at future horizon.

        Parameters
        ----------
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None
        X : Optional[pd.DataFrame], optional
            Exogenous variables, by default None

        Returns
        -------
        pd.Series
            Returns an predicted values
        """
        future_time_periods = pd.period_range(start=self._y.index[-1], periods=fh + 1)[
            1:
        ]
        if self.strategy == "last":
            y_pred = pd.Series([self._y[-1]] * fh, index=future_time_periods)
        elif self.strategy == "mean":
            y_pred = pd.Series([self._y.mean()] * fh, index=future_time_periods)
        return y_pred
