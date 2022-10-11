"""Minimally mimics sktime's BaseForecaster class
https://github.com/sktime/sktime/blob/main/sktime/forecasting/base/_base.py
"""

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class BaseForecaster(ABC):
    def __init__(self):
        self._is_fitted = False

        self._y = None
        self._X = None

        # forecasting horizon
        self._fh = None
        self._is_fitted = False

    @property
    def is_fitted(self):
        """Whether `fit` has been called.
        Ref: https://github.com/sktime/sktime/blob/v0.13.4/sktime/base/_base.py#L788
        """
        return self._is_fitted

    def fit(
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
            returns an instance of self for chaining
        """
        self._y = y
        self._X = X
        self._fh = fh

        self._fit(y, X, fh)

        self._is_fitted = True
        return self

    @abstractmethod
    def _fit(
        self, y: pd.Series, X: Optional[pd.DataFrame] = None, fh=None
    ) -> "BaseForecaster":
        """Fit to training data.

        Parameters
        ----------
        y : pd.Series
            Target time series to which to fit the forecaster.
        X : pd.DataFrame, optional
            Exogenous variables, by default None
        fh : _type_, optional
            The forecasters horizon with the steps ahead to to predict, by default None

        Returns
        -------
        BaseForecaster
            Returns an instance of self for chaining
        """

    def predict(
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
        self.check_is_fitted()
        y_pred = self._predict(fh=fh, X=X)
        return y_pred

    @abstractmethod
    def _predict(self, fh: Optional[int] = None, X: Optional[pd.DataFrame] = None):
        """Forecast time series at future horizon.

        Parameters
        ----------
        fh : Optional[int], optional
            The forecasters horizon with the steps ahead to to predict, by default None
        X : Optional[pd.DataFrame], optional
            Exogenous variables, by default None
        """

    def check_is_fitted(self):
        """Check if the estimator has been fitted.
        Raises
        ------
        NotFittedError
            If the estimator has not been fitted yet.
        """
        if not self.is_fitted:
            raise NotFittedError(
                f"This instance of {self.__class__.__name__} has not "
                f"been fitted yet; please call `fit` first."
            )


class NotFittedError(ValueError, AttributeError):
    """Exception class to raise if estimator is used before fitting.
    This class inherits from both ValueError and AttributeError to help with
    exception handling and backward compatibility.
    References
    ----------
    .. [1] Based on scikit-learn's NotFittedError
    """
