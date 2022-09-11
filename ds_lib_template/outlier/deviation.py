import logging
from abc import abstractmethod
from typing import Optional

import pandas as pd

from ds_lib_template.outlier.base import BaseOutlierDetection


class BaseDeviationDetection(BaseOutlierDetection):
    def __init__(
        self,
        data: pd.Series,
        multiplier: int = 3,
        logger: Optional[logging.Logger] = None,
    ):
        """Initializes the outlier detection class which used a deviation based
        approach for outlier detection.

        Parameters
        ----------
        data : pd.Series
            Data whose outliers needed to be detected
        multiplier : int, optional
            Multiplier for deviation calculations, by default 3
        logger : Optional[logging.Logger], optional
            Logger object, by default None
        """
        self.multiplier = multiplier
        self.center: Optional[float] = None
        self.deviation: Optional[float] = None
        super().__init__(data=data, logger=logger)

    @abstractmethod
    def set_center(self) -> "BaseOutlierDetection":
        """Sets the center of the data. Sets the `center` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """

    @abstractmethod
    def set_deviation(self) -> "BaseOutlierDetection":
        """Sets the deviation of the data. Sets the `deviation` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """

    def set_limits(self) -> "BaseOutlierDetection":
        """Detect the outlier limits. Sets the `ul` and `ll` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        if self.center is None:
            self.logger.warning("Center has not been calculated. Calculating it now.")
            self.set_center()
        if self.deviation is None:
            self.logger.warning(
                "Deviation has not been calculated. Calculating it now."
            )
            self.set_deviation()

        self.ul = self.center + self.multiplier * self.deviation
        self.ll = self.center - self.multiplier * self.deviation

    def correct_outliers(self) -> "BaseOutlierDetection":
        """Corrects outliers in the data. Sets the `corrected` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining

        Raises
        ------
        ValueError
            When method is called before `set_limits` method
        """
        self.corrected = self.data.copy()
        if self.ul is None or self.ll is None:
            raise ValueError(
                "Upper and Lower limits not available. Please run `set_limits` first."
            )
        self.corrected[self.corrected > self.ul] = self.ul
        self.corrected[self.corrected < self.ll] = self.ll

        return self


class StdDevOutlierDetection(BaseDeviationDetection):
    def set_center(self) -> "BaseOutlierDetection":
        """Sets the center of the data. Sets the `center` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        self.center = self.data.mean()

    def set_deviation(self) -> "BaseOutlierDetection":
        """Sets the deviation of the data. Sets the `deviation` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        self.deviation = self.data.std()


class MADOutlierDetection(BaseDeviationDetection):
    def set_center(self) -> "BaseOutlierDetection":
        """Sets the center of the data. Sets the `center` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        self.center = self.data.median()

    def set_deviation(self) -> "BaseOutlierDetection":
        """Sets the deviation of the data. Sets the `deviation` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        self.deviation = self.data.mad()
