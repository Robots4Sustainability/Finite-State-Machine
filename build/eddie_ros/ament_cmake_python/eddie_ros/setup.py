from setuptools import find_packages
from setuptools import setup

setup(
    name='eddie_ros',
    version='0.0.1',
    packages=find_packages(
        include=('eddie_ros', 'eddie_ros.*')),
)
