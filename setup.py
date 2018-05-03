# coding=utf-8
# author@alingse
# 2016.10.07

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read().decode('utf-8')

setup(
    name='jsoncsv',
    version='2.0.8b',
    description='a command tool easily convert json file to csv or xlsx',
    long_description=readme,
    author='alingse',
    author_email='alingse@foxmail.com',
    url='https://github.com/alingse/jsoncsv',
    license='Apache 2.0',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'xlwt',
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'jsoncsv = jsoncsv.main:jsoncsv',
            'mkexcel = jsoncsv.main:mkexcel',
        ],
    }
)
