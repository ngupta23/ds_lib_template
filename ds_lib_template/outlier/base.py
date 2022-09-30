import logging
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class BaseOutlierDetection(ABC):
    def __init__(self, data: pd.Series, logger: Optional[logging.Logger] = None):
        """Initializes the outlier detection class.

        Parameters
        ----------
        data : pd.Series
            Data whose outliers needed to be detected
        logger : Optional[logging.Logger], optional
            Logger object, by default None
        """
        self.data = data
        self.logger = logger or logging.getLogger()
        self.ul: Optional[float] = None
        self.ll: Optional[float] = None
        self.outliers: Optional[pd.Series] = None
        self.corrected: Optional[pd.Series] = None

    @abstractmethod
    def set_limits(self) -> "BaseOutlierDetection":
        """Detect the outlier limits. Sets the `ul` and `ll` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """

    def detect_outliers(self) -> "BaseOutlierDetection":
        """Detect outliers in the data. Sets the `outliers` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        if self.ul is None or self.ll is None:
            self.logger.warning("Limits have not been set. Setting them now.")
            self.set_limits()

        self.outlier = (self.data > self.ul) | (self.data < self.ll)
        return self

    @abstractmethod
    def correct_outliers(self) -> "BaseOutlierDetection":
        """Corrects outliers in the data. Sets the `corrected` attribute.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """

    def run_workflow(self) -> "BaseOutlierDetection":
        """Runs the entire workflow.

        Returns
        -------
        BaseOutlierDetection
            Class object for chaining
        """
        self.set_limits().detect_outliers().correct_outliers()
        return self

    def get_corrected_data(self) -> pd.Series:
        """Returns the corrected data.

        Returns
        -------
        pd.Series
            Corrected data

        Raises
        ------
        ValueError
            When method is called before `detect_outliers` method
        """
        if self.corrected is None:
            raise ValueError(
                "Corrected data not available. Please run `correct_outliers` first."
            )
        return self.corrected
