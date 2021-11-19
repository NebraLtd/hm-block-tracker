import os
import requests
from jinja2 import Template


def get_latest_snapshot_block(base_url):
    # Fetches latest snapshoted block from Helium API.
    # resp = requests.get('https://helium-snapshots.nebra.com/latest.json')
    cache = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    resp = requests.get(
        'https://storage.googleapis.com/{}/latest.json'.format(
            base_url.replace('https://', '')
        ),
        headers=cache
    )
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception("Error fetching snapshot block from Helium API")


def populate_template(
        blessed_block,
        base_url,
        i2c_bus,
        template_file='config.template'
):
    template = Template(open(template_file).read())
    block_id = blessed_block['height']
    block_hash = blessed_block['hash']

    output = template.render(
        i2c_bus=i2c_bus,
        base_url=base_url,
        blessed_block=block_id,
        blessed_block_hash=block_hash
    )
    return output


def output_config_file(config, path):
    open(path, "w").write(config)


def main():
    if bool(int(os.getenv('PRODUCTION', '0'))):
        base_url = 'https://helium-snapshots.nebra.com'
    else:
        base_url = 'https://helium-snapshots-stage.nebra.com'

    if bool(int(os.getenv('ROCKPI', '1'))):
        i2c_bus = 'i2c-7'
        path = 'docker.config.rockpi'
    else:
        i2c_bus = 'i2c-1'
        path = 'docker.config'

    latest_snapshot = get_latest_snapshot_block(base_url)
    config = populate_template(latest_snapshot, base_url, i2c_bus)
    output_config_file(config, path)


if __name__ == '__main__':
    main()
