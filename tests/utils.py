import pandas as pd

from ds_lib_template.outlier.deviation import (
    MADOutlierDetection,
    StdDevOutlierDetection,
)


def _load_deviation_classes():
    """Load the various deviation classes."""
    return [StdDevOutlierDetection, MADOutlierDetection]


def _load_ll_ul_outlier_data():
    """Load data containing lower and upper outliers.
    Returns 2 lists, first one contains upper outlier and second one contains lower outlier.
    Outlier in last position of each list.
    """
    return [
        pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1000]),
        pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1000]),
    ]
