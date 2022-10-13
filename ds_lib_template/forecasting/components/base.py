import logging
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

import pandas as pd


class BaseComponentSplitter(ABC):
    def __init__(
        self,
        model: Any,
        drivers: Optional[List[str]] = None,
        holidays: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """Initializes the Forecast Component Splitter class. This class is used
        to break a forecast into its individual components such as trend, seasonality,
        impact of drivers, holidays, etc.

        Parameters
        ----------
        model : Any
            A fitted model which will be used to get the predictions and the
            prediction components.
        drivers : Optional[List[str]]
            The names of all the drivers (columns) in the dataset. These columns
            will need to be provided at the time of prediction, by default None
        holidays : Optional[List[str]]
            The names of all the holiday columns in the dataset. These columns
            will need to be provided at the time of prediction, by default None
        logger : Optional[logging.Logger], optional
            Logger object, by default None
        """

        self.model = model
        self.drivers = drivers
        self.holidays = holidays
        self.logger = logger or logging.getLogger()

        self.component_trend: Optional[pd.Series] = None
        self.component_seasonality: Optional[pd.Series] = None
        self.component_drivers: Optional[pd.DataFrame] = None
        self.component_holidays: Optional[pd.DataFrame] = None
        self.component_others: Optional[pd.DataFrame] = None

        total_drivers = len(drivers) if drivers is not None else 0
        total_holidays = len(holidays) if holidays is not None else 0
        # Trend + Seasonality + Drivers + Holidays + Others
        self.total_components = 2 + total_drivers + total_holidays

    def predict(
        self, fh: Optional[int] = None, X: Optional[pd.DataFrame] = None
    ) -> Tuple[pd.Series, pd.DataFrame]:
        """Predicts the future values of the target variable along with its constituent components.

        Parameters
        ----------
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None
        X : Optional[pd.DataFrame]
            Exogenous variables, by default None

        Returns
        -------
        pd.Series
            The predictions
        """
        y_pred = self._predict(fh=fh, X=X)

        self._set_component_trend()
        self._set_component_seasonality()
        self._set_component_drivers()
        self._set_component_holidays()
        self._set_component_others()

        components = self.get_all_components()

        return y_pred, components

    @abstractmethod
    def _predict(
        self, fh: Optional[int] = None, X: Optional[pd.DataFrame] = None
    ) -> pd.Series:
        """Predicts the future values of the target variable.

        Parameters
        ----------
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None
        X : Optional[pd.DataFrame]
            Exogenous variables, by default None

        Returns
        -------
        pd.Series
            The predictions
        """

    @abstractmethod
    def _set_component_trend(self):
        """Sets the trend component of the forecast (self.component_trend)"""

    @abstractmethod
    def _set_component_seasonality(self):
        """Sets the seasonal component of the forecast (self.component_seasonality)"""

    @abstractmethod
    def _set_component_drivers(self):
        """Sets the driver components of the forecast (self.component_drivers)"""

    @abstractmethod
    def _set_component_holidays(self):
        """Sets the holiday components of the forecast (self.component_holidays)"""

    @abstractmethod
    def _set_component_others(self):
        """Sets the other (unknown and/or model specific) components of the
        forecast (self.component_others)"""

    def get_component_trend(self) -> pd.Series:
        """Returns the trend component of the forecast

        Returns
        -------
        pd.Series
            The trend component
        """
        if self.component_trend is None:
            raise ValueError(
                "Trend component has not been set. Please run `predict` before "
                "fetching the components of the forecast."
            )

        return self.component_trend

    def get_component_seasonality(self):
        """Returns the seasonal component of the forecast

        Returns
        -------
        pd.Series
            The seasonal component
        """
        if self.component_seasonality is None:
            raise ValueError(
                "Seasonality component has not been set. Please run `predict` "
                "before fetching the components of the forecast."
            )

        return self.component_seasonality

    def get_component_drivers(self):
        """Returns the driver components of the forecast

        Returns
        -------
        pd.DataFrame
            The driver components
        """
        if self.component_drivers is None:
            raise ValueError(
                "Driver components have not been set. Please run `predict` "
                "before fetching the components of the forecast."
            )

        return self.component_drivers

    def get_component_holidays(self):
        """Returns the holiday components of the forecast

        Returns
        -------
        pd.DataFrame
            The holiday components
        """
        if self.component_holidays is None:
            raise ValueError(
                "Holiday components have not been set. Please run `predict` "
                "before fetching the components of the forecast."
            )

        return self.component_holidays

    def get_component_others(self):
        """Returns the other (unknown and/or model specific) components of the
        forecast

        Returns
        -------
        pd.DataFrame
            The other components
        """
        if self.component_others is None:
            raise ValueError(
                "Other components have not been set. Please run `predict` "
                "before fetching the components of the forecast."
            )

        return self.component_others

    def get_all_components(self):
        """Returns all the components of the forecast

        Returns
        -------
        pd.DataFrame
            All the components
        """
        return pd.concat(
            [
                self.get_component_trend(),
                self.get_component_seasonality(),
                self.get_component_drivers(),
                self.get_component_holidays(),
                self.get_component_others(),
            ],
            axis=1,
        )
