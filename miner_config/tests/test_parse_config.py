from unittest import TestCase


# Test Candidates
from miner_config.parse_config import read_sys_config_file
from miner_config.parse_config import extract_blessed_block
from miner_config.parse_config import extract_blessed_block_hash
from miner_config.parse_config import get_blessed_block


FIXTURES_PATH = 'miner_config/tests/fixtures'


def load_fixture(file):
    path = '%s/%s' % (FIXTURES_PATH, file)
    with open(path) as f:
        content = f.readlines()
    content = list(map(lambda x: x.strip(), content))
    return content


class TestReadSysConfigFile(TestCase):

    def test_read_file(self):
        # Expects contents of a file read to be returned as a list
        # of lines present in that file.
        path = '%s/3_line_file.txt' % FIXTURES_PATH
        content = read_sys_config_file(path=path)
        expected = ['1', '2', '3']
        self.assertEqual(content, expected)

    def test_strip_whitespace(self):
        # Expect file lines to have any whitespaced stripped.
        path = '%s/3_line_file_with_whitespace.txt' % FIXTURES_PATH
        content = read_sys_config_file(path=path)
        expected = ['1', '2', '3']
        self.assertEqual(content, expected)


class TestExtractBlessedBlock(TestCase):

    def test_blessed_block(self):
        # Expect an integer for blessed block id to be returned.
        content = load_fixture('sample_upstream_config.txt')
        block = extract_blessed_block(content)
        self.assertIsInstance(block, int)
        self.assertEqual(block, 910531)

    def test_block_invalid_type(self):
        # Expect an invalid type for blessed block id to through
        # a ValueError.
        content = load_fixture('sample_upstream_config_invalid.txt')
        exception = False
        exception_type = None

        try:
            extract_blessed_block(content)
        except Exception as err:
            exception = True
            exception_type = err

        self.assertIsInstance(exception_type, ValueError)
        self.assertTrue(exception)

    def test_missing_keys(self):
        # Expect the blessed_block key not existing within the config to
        # raise a KeyError exception.
        content = load_fixture('sample_upstream_config_missing_keys.txt')
        exception = False
        exception_type = None

        try:
            extract_blessed_block(content)
        except Exception as err:
            exception = True
            exception_type = err

        self.assertIsInstance(exception_type, KeyError)
        self.assertTrue(exception)


class TestExtractBlessedBlockHash(TestCase):

    def test_blessed_block_hash(self):
        content = load_fixture('sample_upstream_config.txt')
        hash = extract_blessed_block_hash(content)
        self.assertIsInstance(hash, str)
        expected = (
            '<<95,253,152,33,253,132,175,201,16,213,118,213,1,87,113,203,209'
            ',242,143,230,104,213,232,83,61,173,201,176,206,176,178,42>>'
        )
        self.assertEqual(hash, expected)

    def test_blessed_block_hash_invalid_hash(self):
        # Raise an exception if the hash does not satisfy the regular expession
        # summarising the format of a hash.
        content = load_fixture('sample_upstream_config_invalid.txt')

        exception = False
        exception_type = None

        try:
            extract_blessed_block_hash(content)
        except Exception as err:
            exception = True
            exception_type = err

        self.assertTrue(exception)
        self.assertIsInstance(exception_type, Exception)

    def test_missing_keys(self):
        # Expect the blessed_block_hash key not existing within the config to
        # raise a TypeError exception.
        content = load_fixture('sample_upstream_config_missing_keys.txt')
        exception = False
        exception_type = None

        try:
            extract_blessed_block_hash(content)
        except Exception as err:
            exception = True
            exception_type = err

        self.assertIsInstance(exception_type, TypeError)
        self.assertTrue(exception)


class TestCaseGetBlessedBlock(TestCase):

    def test_get_blessed_block(self):
        content = load_fixture('sample_upstream_config.txt')
        result = get_blessed_block(content)
        hash = (
            '<<95,253,152,33,253,132,175,201,16,213,118,213,1,87,113,203,'
            '209,242,143,230,104,213,232,83,61,173,201,176,206,176,178,42>>'
        )
        expected = {
            'blessed_block': 910531,
            'blessed_block_hash': hash}
        self.assertEqual(result, expected)
        self.assertIsInstance(result, dict)
