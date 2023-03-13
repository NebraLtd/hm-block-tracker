import os
import re
import mock
from unittest import TestCase

# Test Candidates
from miner_config.generate_config import main
from miner_config.generate_config import populate_template
from miner_config.generate_config import get_latest_snapshot_block
from miner_config.generate_config import parse_i2c_address
from miner_config.generate_config import output_config_file
from miner_config.generate_config import is_production_fleet
from miner_config.generate_config import is_device_type

FIXTURES_PATH = 'miner_config/tests/fixtures'


class TestMain(TestCase):

    @mock.patch('miner_config.generate_config.get_latest_snapshot_block')
    @mock.patch('miner_config.generate_config.populate_template')
    @mock.patch('miner_config.generate_config.output_config_file')
    @mock.patch('miner_config.generate_config.parse_i2c_address')
    def test_expected_functions_called(
            self,
            mock_parse,
            mock_output,
            mock_populate,
            mock_get
    ):
        main()
        mock_get.assert_called()
        mock_populate.assert_called()
        mock_output.assert_called()
        mock_parse.assert_called()


class TestPopulateTemplate(TestCase):

    def test_populate_template(self):
        path = '%s/sample_output.txt' % FIXTURES_PATH
        conf_file = open(path).read()
        blessed_block = {
            'height': 500,
            'hash': 'HASH HERE'
        }
        base_url = 'https://helium-snapshots.nebracdn.com'
        i2c_bus = 'i2c-1'
        i2c_address = 60
        key_slot = 0
        onboarding_key_slot = 0
        output = populate_template(blessed_block, base_url, i2c_bus, key_slot,
                                   i2c_address, onboarding_key_slot)
        self.assertEqual(output, conf_file)

    def test_populate_template_staging(self):
        path = '%s/sample_output_staging.txt' % FIXTURES_PATH
        conf_file = open(path).read()
        blessed_block = {
            'height': 500,
            'hash': 'HASH HERE'
        }
        base_url = 'https://helium-snapshots-stage.nebracdn.com'
        i2c_bus = 'i2c-1'
        i2c_address = 60
        key_slot = 0
        onboarding_key_slot = 0
        output = populate_template(blessed_block, base_url, i2c_bus, key_slot,
                                   i2c_address, onboarding_key_slot, 'config-stage.template')
        self.assertEqual(output, conf_file)


class TestParseI2CAddress(TestCase):

    def test_parse_i2c_address(self):
        port = 96
        output = parse_i2c_address(port)
        hex_i2c_address = '60'

        self.assertEqual(output, hex_i2c_address)


class TestIsProductionFleet(TestCase):

    @mock.patch.dict(os.environ, {"PRODUCTION": "1"})
    def test_is_production_fleet(self):
        output = is_production_fleet()

        self.assertTrue(output, "Test failed - value not true")


class TestIsDeviceType(TestCase):

    @mock.patch.dict(os.environ, {"ROCKPI": "1"})
    def test_is_device_type(self):
        device_type = "ROCKPI"
        output = is_device_type(device_type)

        self.assertTrue(output, "Test failed - value not true")


class TestGetLatestSnapshotBlock(TestCase):

    def test_get_latest_snapshot_block(self):
        base_url = 'https://helium-snapshots.nebracdn.com'
        latest_snapshot = get_latest_snapshot_block(base_url)

        # Adapted from file
        # https://github.com/NebraLtd/hm-block-tracker/blob/master/snapshotter/base64url_encoder.py

        byte_array = latest_snapshot["hash"]
        byte_array = re.sub('[<>]', '', byte_array)
        byte_array = byte_array.split(",")

        def char_to_int(num):
            return int(num)
        byte_array = map(char_to_int, byte_array)
        byte_array = bytearray(list(byte_array))

        self.assertIn("height", latest_snapshot)
        self.assertIn("hash", latest_snapshot)
        self.assertIsInstance(latest_snapshot["height"], int)
        self.assertIsInstance(latest_snapshot["hash"], str)
        self.assertIsInstance(byte_array, bytearray)

    def test_get_latest_snapshot_block_failure(self):
        base_url = 'https://helium-snapshots.fakedthisdomain.nebra'

        with self.assertRaises(Exception) as e:
            get_latest_snapshot_block(base_url)

        self.assertEqual(str(e.exception), "Error fetching latest.json from Nebra Google Cloud")


class TestOutputConfigFile(TestCase):

    def test_output_config_file(self):
        path = "docker.config.test"
        config = "test"
        output_config_file(config, path)
        output = open(path).read()

        self.assertEqual(output, "test")
