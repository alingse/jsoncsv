# coding=utf-8
# author@alingse
# 2016.08.09
import io
import json
import unittest
from click.testing import CliRunner

from jsoncsv.main import jsoncsv


class Testjsoncsv(unittest.TestCase):

    def test_jsoncsv_expand(self):
        runner = CliRunner()
        args = ['-e', 'fixture/files/raw.0.json', 'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code == 0

    def test_jsoncsv_expand_with_json_array(self):
        runner = CliRunner()
        args = ['-e', 'fixture/files/raw.1.json', 'fixture/files/tmp.expand.1.json', '-A']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code == 0

    def test_jsoncsv_expand_restore(self):
        runner = CliRunner(echo_stdin=True)
        result = runner.invoke(jsoncsv, args=['-e', 'fixture/files/raw.2.json', 'fixture/files/tmp.expand.2.json'])
        assert result.exit_code == 0
        result = runner.invoke(jsoncsv, args=['-r', 'fixture/files/tmp.expand.2.json', 'fixture/files/tmp.restore.2.json'])
        assert result.exit_code == 0

        with io.open('fixture/files/raw.2.json', 'r') as f:
            input_data = [json.loads(line) for line in f]

        with io.open('fixture/files/tmp.restore.2.json', 'r') as f:
            resotre_data = [json.loads(line) for line in f]

        self.assertEqual(input_data, resotre_data)
