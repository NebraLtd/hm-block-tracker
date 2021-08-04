import subprocess
import sys
from miner_config.parse_config import read_sys_config_file
from miner_config.parse_config import extract_blessed_block


def main():
    result = subprocess.run(
        ['docker', 'exec', 'miner', '/opt/miner/bin/miner', 'info', 'height'],
        capture_output=True,
        text=True
    ).stdout

    miner_block_height = int(result.split('\t')[2].strip())
    config_file = read_sys_config_file(path='config/sys.config')
    config_block_height = extract_blessed_block(config_file)

    print(
        "%s (blessed block) ->->-> %s (miner block)"
        % (config_block_height, miner_block_height)
    )

    if config_block_height < miner_block_height:
        print("Miner has continued syncing after blessed block. Success!")
        sys.exit(0)
    else:
        print("Miner has stalled at blessed block. Failure!")


if __name__ == '__main__':
    main()
