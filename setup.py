#coding=utf-8
#author@alingse
#2016.10.07

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='jsoncsv',
    version='0.0.1',
    description='a tool convert json file to csv or xlsx',
    long_description=readme,
    author='alingse',
    author_email='alingse@foxmail.com',
    license=license,
    packages=find_packages(exclude=('tests'))
)