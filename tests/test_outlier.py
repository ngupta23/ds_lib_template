"""Module to test outlier detection functionality
"""
import pytest
from pandas.testing import assert_series_equal

from ds_lib_template.outlier.deviation import (
    MADOutlierDetection,
    StdDevOutlierDetection,
)

from .utils import _load_deviation_classes, _load_ll_ul_outlier_data

##############################
#### Functions Start Here ####
##############################

# NOTE: Fixtures can not be used to parameterize tests
# https://stackoverflow.com/questions/52764279/pytest-how-to-parametrize-a-test-with-a-list-that-is-returned-from-a-fixture
# Hence, we have to create functions and create the parameterized list first
# (must happen during collect phase) before passing it to mark.parameterize.

deviation_classes = _load_deviation_classes()
datasets = _load_ll_ul_outlier_data()

############################
#### Functions End Here ####
############################

##########################
#### Tests Start Here ####
##########################


@pytest.mark.parametrize("detector_class", deviation_classes)
def test_no_outliers(detector_class, no_outlier_data):
    """Tests outlier detection when data has no outliers"""
    outlier_detector = detector_class(data=no_outlier_data)
    corrected = outlier_detector.run_workflow().get_corrected_data()

    #### Test points that are not outliers ----
    assert_series_equal(corrected, no_outlier_data)


@pytest.mark.parametrize("detector_class", deviation_classes)
@pytest.mark.parametrize("data", datasets)
def test_deviation(detector_class, data):
    """Tests the deviation based outlier methods with both positive and negative outliers."""
    outlier_detector = detector_class(data=data)
    corrected = outlier_detector.run_workflow().get_corrected_data()

    # General checks ----
    assert len(corrected) == len(data)

    # Test center and deviation ----
    if isinstance(outlier_detector, StdDevOutlierDetection):
        assert outlier_detector.center == data.mean()
        assert outlier_detector.deviation == data.std()
    elif isinstance(outlier_detector, MADOutlierDetection):
        assert outlier_detector.center == data.median()
        assert outlier_detector.deviation == data.mad()

    # Test points that are not outliers ----
    for i in range(len(data) - 1):
        assert corrected.iloc[i] == data.iloc[i]

    # Test outlier ----
    assert corrected.iloc[-1] != data.iloc[-1]
