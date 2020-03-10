# coding=utf-8
# author@alingse
# 2020.03.10

import unittest
from click.testing import CliRunner

from jsoncsv.main import mkexcel


class Testmkexcel(unittest.TestCase):
    def test_mkexcel_csv(self):
        runner = CliRunner()
        args = ['fixture/files/expand.0.json',
                'fixture/files/tmp.expand.0.csv']
        result = runner.invoke(mkexcel, args=args)
        assert result.exit_code == 0

    def test_mkexcel_xls(self):
        runner = CliRunner()
        args = ['-t', 'xls', 'fixture/files/expand.0.json',
                'fixture/files/tmp.expand.0.xls']
        result = runner.invoke(mkexcel, args=args)
        assert result.exit_code == 0

    def test_mkexcel_with_error(self):
        runner = CliRunner()
        args = ['-t', 'xlsx', 'fixture/files/expand.0.json',
                'fixture/files/tmp.expand.0.xls']
        result = runner.invoke(mkexcel, args=args)
        assert result.exit_code == 2
