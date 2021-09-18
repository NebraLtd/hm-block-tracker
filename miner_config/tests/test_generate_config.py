import mock
from unittest import TestCase
from binascii import Error

# Test Candidates
from miner_config.generate_config import main
from miner_config.generate_config import populate_template
from miner_config.generate_config import convert_snapshot_to_blessed_block


FIXTURES_PATH = 'miner_config/tests/fixtures'


class TestMain(TestCase):

    @mock.patch('miner_config.generate_config.get_latest_snapshot_block')
    @mock.patch(
        'miner_config.generate_config.convert_snapshot_to_blessed_block'
    )
    @mock.patch('miner_config.generate_config.populate_template')
    @mock.patch('miner_config.generate_config.output_config_file')
    def test_expected_functions_called(
            self,
            mock_output,
            mock_populate,
            mock_convert,
            mock_get
    ):
        main()
        mock_get.assert_called()
        mock_convert.assert_called()
        mock_populate.assert_called()
        mock_output.assert_called()


class TestConvertSnapshotToBlessedBlock(TestCase):

    def test_convert_snapshot_valid(self):
        snapshot = {
            "snapshot_hash": "l2MzQmuy27k7Hpl0Eyu8MD5-aKgE4eX5NH_HtPu2xvw",
            "block": 1014481
        }
        result = convert_snapshot_to_blessed_block(snapshot)
        integer_array = '<<151,99,51,66,107,178,219,185,59,30,153,116,19,43' \
            ',188,48,62,126,104,168,4,225,229,249,52,127,199,180,251,182,198' \
            ',252>>'
        expected_output = {
            'blessed_block': 1014481,
            'blessed_block_hash': integer_array
        }
        self.assertEqual(result, expected_output)

    def test_convert_snapshot_invalid(self):
        snapshot = {
            "snapshot_hash": "jkdsfhkjdhsfjkhfjkehwjkhrk",
            "block": 1014481
        }
        raised_exception = False
        try:
            convert_snapshot_to_blessed_block(snapshot)
        except Exception as err:
            raised_exception = True
            exception_type = err
        self.assertTrue(raised_exception)
        self.assertIsInstance(exception_type, Error)


class TestPopulateTemplate(TestCase):

    def test_populate_template(self):
        path = '%s/sample_output.txt' % FIXTURES_PATH
        conf_file = open(path).read()
        blessed_block = {
            'blessed_block': 500,
            'blessed_block_hash': 'HASH HERE'
        }
        output = populate_template(blessed_block)
        self.assertEqual(output, conf_file)
