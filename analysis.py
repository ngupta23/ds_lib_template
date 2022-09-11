import logging

import pandas as pd

from ds_lib_template.outlier.deviation import StdDevOutlierDetection

# Get data from your main data source (mocking it here)
data = pd.Series(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1000]
)

# Get your logger from your environment (mocking it here)
logger = logging.getLogger("my_logger")

# Run your main code
std_od = StdDevOutlierDetection(data=data, logger=logger)
corrected = std_od.run_workflow().get_corrected_data()
logger.info(f"Corrected data (STD DEV): {corrected}")

logger.info("DONE")
