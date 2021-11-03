import json
import os
from jinja2 import Template


def get_latest_snapshot_block():
    """
    We are already building this file as part of the workflow
    """
    with open('/var/miner_data/saved-snaps/latest.json') as f:
        return json.loads(f.read())


def populate_template(blessed_block, base_url, template_file='config.template'):
    template = Template(open(template_file).read())
    block_id = blessed_block['height']
    block_hash = blessed_block['hash']

    output = template.render(
        base_url=base_url,
        blessed_block=block_id,
        blessed_block_hash=block_hash
    )
    return output


def output_config_file(config, path='docker.config'):
    open(path, "w").write(config)


def main():
    latest_snapshot = get_latest_snapshot_block()

    if bool(int(os.getenv('PRODUCTION', '0'))):
        base_url = 'https://helium-snapshots.nebra.com'
    else:
        base_url = 'https://helium-snapshots-stage.nebra.com'

    config = populate_template(latest_snapshot, base_url)
    output_config_file(config)


if __name__ == '__main__':
    main()
