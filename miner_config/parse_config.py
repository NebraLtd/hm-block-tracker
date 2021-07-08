import re


def read_sys_config_file(path='miner/config/sys.config'):
    with open(path) as f:
        content = f.readlines()
    content = list(map(lambda x: x.strip(), content))
    return content


def extract_blessed_block(config_lines):
    blessed_block = None

    for line in config_lines:
        if 'blessed_snapshot_block_height' in line:
            blessed_block = int(line.split(',')[1].replace('}', '').strip())

    if not blessed_block:
        raise KeyError()

    return blessed_block


def extract_blessed_block_hash(config_lines):
    # Extract the blessed block hash from the config file.
    blessed_block_hash = None

    for x in range(len(config_lines)):
        if 'blessed_snapshot_block_hash' in config_lines[x]:
            blessed_block_hash = config_lines[x+1]
            blessed_block_hash = blessed_block_hash.replace('},', '').strip()

    # Verify the hash satisfies the expected format of a hash...
    expression = '^<<([0-9]+(,[0-9]+)+)>>$'
    if not re.match(expression, blessed_block_hash):
        raise Exception('Extracted block hash does not match the expected '
                        'format of a block hash.')

    return blessed_block_hash


def get_blessed_block(config_lines):
    return {
        'blessed_block': extract_blessed_block(config_lines),
        'blessed_block_hash': extract_blessed_block_hash(config_lines)
    }
