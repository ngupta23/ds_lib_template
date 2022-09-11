# ds_lib_template
A standard data science library template


# Advantages

1. Serves as a common repository for common tasks in workflows
2. Unit tested to ensure confidence in functionality
    - unit tests can be parameterized to speed up testing without the need for boiler plate code
    - fixtures & utils allow for writing common test code and testing with a variety of settings

```
> pytest tests -v
```

```
tests/test_outlier.py::test_no_outliers[StdDevOutlierDetection] PASSED                                                                                                               [ 16%]
tests/test_outlier.py::test_no_outliers[MADOutlierDetection] PASSED                                                                                                                  [ 33%]
tests/test_outlier.py::test_deviation[data0-StdDevOutlierDetection] PASSED                                                                                                           [ 50%]
tests/test_outlier.py::test_deviation[data0-MADOutlierDetection] PASSED                                                                                                              [ 66%]
tests/test_outlier.py::test_deviation[data1-StdDevOutlierDetection] PASSED                                                                                                           [ 83%]
tests/test_outlier.py::test_deviation[data1-MADOutlierDetection] PASSED                                                                                                              [100%]

==================================================================================== 6 passed in 0.08s ====================================================================================
```

3. Includes tools to assist developers in day to day tasks
    - Formatting is consistent and automatically applied by `black`
    - Inconsistencies in code are automatically pointed out by `flake8`
    - Order of imports is consistent and automatically applied by `isort`

```
black .
```

```
All done! ✨ 🍰 ✨
14 files left unchanged.
```

```
flake8 .
```

```
.\analysis.py:9:80: E501 line too long (81 > 79 characters)
.\setup.py:3:80: E501 line too long (82 > 79 characters)
.\setup.py:5:80: E501 line too long (88 > 79 characters)
.\ds_lib_template\outlier\base.py:8:80: E501 line too long (81 > 79 characters)
.\ds_lib_template\outlier\base.py:75:80: E501 line too long (84 > 79 characters)
.\ds_lib_template\outlier\deviation.py:61:80: E501 line too long (86 > 79 characters)
.\ds_lib_template\outlier\deviation.py:88:80: E501 line too long (86 > 79 characters)
.\tests\conftest.py:18:80: E501 line too long (92 > 79 characters)
.\tests\test_outlier.py:12:1: E266 too many leading '#' for block comment
.\tests\test_outlier.py:24:1: E266 too many leading '#' for block comment
.\tests\test_outlier.py:28:1: E266 too many leading '#' for block comment
.\tests\test_outlier.py:35:80: E501 line too long (90 > 79 characters)
.\tests\test_outlier.py:40:5: E266 too many leading '#' for block comment
.\tests\test_outlier.py:43:5: E266 too many leading '#' for block comment
.\tests\test_outlier.py:51:5: E266 too many leading '#' for block comment
.\tests\test_outlier.py:55:5: E266 too many leading '#' for block comment
.\tests\utils.py:15:80: E501 line too long (92 > 79 characters)
```

```
isort .
```

```
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\analysis.py
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\ds_lib_template\outlier\base.py
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\ds_lib_template\outlier\deviation.py
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\tests\conftest.py
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\tests\test_outlier.py
Fixing C:\Users\Nikhil\OneDrive\my_libraries\my_python_libraries\ds_lib_template\tests\utils.py
Skipped 1 files
```

4. Flow in a task (e.g. outlier detection) can be enforced using Abstract Base Classes.
    - Specific implementations of task simply inherit the base class and implement it concretely.
    - Common code does not have to be repeated between competing implementation. Provides ease of maintaining code over long run, e.g.
        - fixes to base class get applied to all children automatically
        - unit tests do not have to be repeated across children
