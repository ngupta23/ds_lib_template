import pandas as pd
import pytest

from ds_lib_template.outlier.deviation import (MADOutlierDetection,
                                               StdDevOutlierDetection)


@pytest.fixture(scope="session", name="deviation_classes")
def deviation_classes():
    """Load the various deviation classes."""
    return [StdDevOutlierDetection, MADOutlierDetection]


@pytest.fixture(scope="session", name="ll_ul_outlier_data")
def ll_ul_outlier_data():
    """Load data containing lower and upper outliers.
    Returns 2 lists, first one contains upper outlier and second one contains lower outlier.
    Outlier in last position of each list.
    """
    return [
        pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 1000]),
        pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, -1000]),
    ]
