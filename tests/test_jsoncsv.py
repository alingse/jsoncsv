# coding=utf-8
# author@alingse
# 2016.08.09

import unittest
from click.testing import CliRunner

from jsoncsv.main import jsoncsv


class Testjsoncsv(unittest.TestCase):

    def test_jsoncsv_expand(self):
        runner = CliRunner()
        args = ['-e', 'fixture/files/raw.0.json', 'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code == 0
