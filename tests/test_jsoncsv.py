# author@alingse
# 2016.08.09
import json
import unittest

from click.testing import CliRunner

from jsoncsv.main import jsoncsv


class Testjsoncsv(unittest.TestCase):
    def test_jsoncsv_expand(self):
        runner = CliRunner()
        args = ['-e', 'fixture/files/raw.0.json',
                'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code == 0

    def test_jsoncsv_expand_with_json_array(self):
        runner = CliRunner()
        args = ['-e', 'fixture/files/raw.1.json',
                'fixture/files/tmp.expand.1.json', '-A']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code == 0

    def test_jsoncsv_expand_restore(self):
        runner = CliRunner(echo_stdin=True)
        result = runner.invoke(jsoncsv,
                               args=['-e', 'fixture/files/raw.2.json',
                                     'fixture/files/tmp.expand.2.json'])
        assert result.exit_code == 0
        result = runner.invoke(jsoncsv,
                               args=['-r', 'fixture/files/tmp.expand.2.json',
                                     'fixture/files/tmp.restore.2.json'])
        assert result.exit_code == 0

        with open('fixture/files/raw.2.json') as f:
            input_data = [json.loads(line) for line in f]

        with open('fixture/files/tmp.restore.2.json') as f:
            resotre_data = [json.loads(line) for line in f]

        self.assertEqual(input_data, resotre_data)

    def test_jsoncsv_with_error_args(self):
        runner = CliRunner()
        args = ['-s', 'aa', '-e', 'fixture/files/raw.0.json',
                'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code != 0

    def test_jsoncsv_with_error_sep_args(self):
        runner = CliRunner()
        args = ['-s', '\\', '-e', 'fixture/files/raw.0.json',
                'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code != 0

    def test_jsoncsv_with_error_args_expand_and_restore(self):
        runner = CliRunner()
        args = ['-r', '-e', 'fixture/files/raw.0.json',
                'fixture/files/tmp.expand.0.json']
        result = runner.invoke(jsoncsv, args=args)
        assert result.exit_code != 0
