# author@alingse
import unittest

from click.testing import CliRunner

from jsoncsv.main import jsoncsv


class TestBlankLines(unittest.TestCase):
    def test_expand_skips_blank_lines(self):
        runner = CliRunner()
        result = runner.invoke(
            jsoncsv, args=["-e", "-", "-"], input='{"a": 1}\n\n   \n{"b": 2}\n'
        )
        assert result.exit_code == 0, result.output
        assert result.output.splitlines() == ['{"a": 1}', '{"b": 2}']

    def test_blank_only_input_produces_no_output(self):
        runner = CliRunner()
        result = runner.invoke(jsoncsv, args=["-e", "-", "-"], input="\n\n")
        assert result.exit_code == 0, result.output
        assert result.output == ""
