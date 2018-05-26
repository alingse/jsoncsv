# coding=utf-8
# author@alingse
# 2016.10.07
import io

from setuptools import setup


with io.open('README.rst', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='jsoncsv',
    version='2.0.9',
    url='https://github.com/alingse/jsoncsv',
    description='A command tool easily convert json file to csv or xlsx.',
    long_description=readme,
    author='alingse',
    author_email='alingse@foxmail.com',
    license='Apache 2.0',
    packages=['jsoncsv'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'xlwt',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jsoncsv = jsoncsv.main:jsoncsv',
            'mkexcel = jsoncsv.main:mkexcel',
        ],
    }
)
