import mock
from unittest import TestCase

# Test Candidates
from miner_config.generate_config import main
from miner_config.generate_config import populate_template


FIXTURES_PATH = 'miner_config/tests/fixtures'


class TestMain(TestCase):

    @mock.patch('miner_config.generate_config.get_latest_snapshot_block')
    @mock.patch('miner_config.generate_config.populate_template')
    @mock.patch('miner_config.generate_config.output_config_file')
    def test_expected_functions_called(
            self,
            mock_output,
            mock_populate,
            mock_get
    ):
        main()
        mock_get.assert_called()
        mock_populate.assert_called()
        mock_output.assert_called()


class TestPopulateTemplate(TestCase):

    def test_populate_template(self):
        path = '%s/sample_output.txt' % FIXTURES_PATH
        conf_file = open(path).read()
        blessed_block = {
            'height': 500,
            'hash': 'HASH HERE'
        }
        base_url = 'https://helium-snapshots.nebra.com'
        i2c_bus = 'i2c-1'
        output = populate_template(blessed_block, base_url, i2c_bus)
        self.assertEqual(output, conf_file)
