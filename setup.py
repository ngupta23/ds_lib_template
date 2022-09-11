"""
References
1. https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
2. pycaret setup file: https://github.com/pycaret/pycaret/blob/master/setup.py
3. sktime setup file: https://github.com/alan-turing-institute/sktime/blob/main/setup.py
"""

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

# with open("requirements-optional.txt") as f:
#     required_optional = f.read()

with open("requirements-test.txt") as f:
    required_test = f.read().splitlines()


setup(
    name="ds_lib_template",
    version="0.1.0",
    description="Data Science Library Template",
    author="Nikhil Gupta",
    license="MIT",
    packages=find_packages(include=["ds_lib_template"]),
    include_package_data=True,
    install_requires=required,
    tests_require=required_test,
    python_requires=">=3.7",
    setup_requires=["pytest-runner"],
)
