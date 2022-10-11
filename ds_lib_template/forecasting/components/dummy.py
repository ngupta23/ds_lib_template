from typing import Optional

import numpy as np
import pandas as pd

from ds_lib_template.forecasting.components.base import BaseComponentSplitter


class DummyForecastingComponent(BaseComponentSplitter):
    """Equally splits the forecast into the components."""

    def _predict(
        self, fh: Optional[int] = None, X: Optional[pd.DataFrame] = None
    ) -> pd.Series:
        """Predicts the future values of the target variable.

        Parameters
        ----------
        X : Optional[pd.DataFrame]
            Optional[int]
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None

        Returns
        -------
        pd.Series
            The predictions
        """
        self.y_pred = self.model.predict(fh=fh, X=X)
        return self.y_pred

    def _set_component_trend(self):
        """Sets the trend component of the forecast (self.component_trend)"""
        self.component_trend = self.y_pred / self.total_components
        self.component_trend.name = "trend"

    def _set_component_seasonality(self):
        """Sets the seasonal component of the forecast (self.component_seasonality)"""
        self.component_seasonality = self.y_pred / self.total_components
        self.component_seasonality.name = "seasonality"

    def _set_component_drivers(self):
        """Sets the driver components of the forecast (self.component_drivers)"""
        if self.drivers is not None:
            shape = (len(self.y_pred), len(self.drivers))
            self.component_drivers = pd.DataFrame(
                np.ones(shape), columns=self.drivers, index=self.y_pred.index
            )
            component = self.y_pred / self.total_components
            self.component_drivers.loc[:] = pd.concat(
                [component] * self.component_drivers.columns.size, axis=1
            )
        else:
            self.component_drivers = pd.DataFrame(index=self.y_pred.index)

    def _set_component_holidays(self):
        """Sets the holiday components of the forecast (self.component_holidays)"""
        if self.holidays is not None:
            shape = (len(self.y_pred), len(self.holidays))
            self.component_holidays = pd.DataFrame(
                np.ones(shape), columns=self.holidays, index=self.y_pred.index
            )
            component = self.y_pred / self.total_components
            self.component_holidays.loc[:] = pd.concat(
                [component] * self.component_holidays.columns.size, axis=1
            )
        else:
            self.component_holidays = pd.DataFrame(index=self.y_pred.index)

    def _set_component_others(self):
        """Sets the other (unknown and/or model specific) components of the
        forecast (self.component_others)"""
        self.component_others = pd.DataFrame(index=self.y_pred.index)
