from unittest import TestCase

from miner_config.tests.test_parse_config import FIXTURES_PATH

# Test Candidates
from miner_config.generate_config import populate_template


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
