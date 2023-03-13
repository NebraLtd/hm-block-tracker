import os
import requests
import sentry_sdk
from jinja2 import Template
from urllib.parse import urlparse, parse_qs
from hm_pyhelper.hardware_definitions import get_variant_attribute


def init_sentry():
    sentry_block_tracker = os.environ.get("SENTRY_BLOCK_TRACKER")
    sentry_sdk.init(
        sentry_block_tracker,
        traces_sample_rate=1.0,
    )


def get_latest_snapshot_block(base_url):
    # Fetches latest snapshoted block from Helium API.
    # resp = requests.get('https://helium-snapshots.nebracdn.com/latest.json')
    cache = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    resp = requests.get(
        'https://storage.googleapis.com/{}/latest.json'.format(
            base_url.replace('https://', '')
        ),
        headers=cache, timeout=30
    )
    if resp.status_code == 200:
        return resp.json()
    else:
        raise FileNotFoundError("Error fetching latest.json from Nebra Google Cloud")


def populate_template(
        blessed_block,
        base_url,
        i2c_bus,
        key_slot,
        i2c_address,
        onboarding_key_slot,
        template_file='config.template'
):
    template = Template(open(template_file).read())
    block_id = blessed_block['height']
    block_hash = blessed_block['hash']

    output = template.render(
        i2c_bus=i2c_bus,
        base_url=base_url,
        key_slot=key_slot,
        blessed_block=block_id,
        i2c_address=i2c_address,
        blessed_block_hash=block_hash,
        onboarding_key_slot=onboarding_key_slot
    )
    return output


def output_config_file(config, path):
    with open(path, "w") as file:
        file.write(config)


def is_production_fleet() -> bool:
    return bool(int(os.getenv('PRODUCTION', '0')))


def is_device_type(board_name: str) -> bool:
    return bool(int(os.getenv(board_name, '0')))


def parse_i2c_address(port):
    """
    Takes i2c address in decimal as input parameter, extracts the hex version and returns it.
    """
    return f'{port:x}'


def main():
    init_sentry()
    if is_production_fleet():
        base_url = 'https://helium-snapshots.nebracdn.com'
        template_path = 'config.template'
    else:
        base_url = 'https://helium-snapshots-stage.nebracdn.com'
        template_path = 'config-stage.template'

    onboarding_key_slot = 0

    if is_device_type('ROCKPI'):
        swarm_key_uri = get_variant_attribute('nebra-indoor2', 'SWARM_KEY_URI')
        path = 'docker.config.rockpi'
    elif is_device_type('PISCES'):
        swarm_key_uri = get_variant_attribute('pisces-fl1', 'SWARM_KEY_URI')
        path = 'docker.config.pisces'
    elif is_device_type('PYCOM'):
        swarm_key_uri = get_variant_attribute('pycom-fl1', 'SWARM_KEY_URI')
        path = 'docker.config.pycom'
    elif is_device_type('HELIUMOG'):
        swarm_key_uri = get_variant_attribute('helium-fl1', 'SWARM_KEY_URI')
        onboarding_key_uri = get_variant_attribute('helium-fl1', 'ONBOARDING_KEY_URI')
        path = 'docker.config.og'
    else:
        swarm_key_uri = get_variant_attribute('nebra-indoor1', 'SWARM_KEY_URI')
        path = 'docker.config'

    if onboarding_key_uri:
        parse_onboarding_key = urlparse(onboarding_key_uri)
        query_string = parse_qs(parse_onboarding_key.query)
        onboarding_key_slot = query_string["slot"][0]
    else:
        onboarding_key_slot = 0

    parse_result = urlparse(swarm_key_uri)
    i2c_bus = parse_result.hostname
    i2c_address = parse_i2c_address(parse_result.port)
    query_string = parse_qs(parse_result.query)
    key_slot = query_string["slot"]

    latest_snapshot = get_latest_snapshot_block(base_url)
    config = populate_template(latest_snapshot, base_url, i2c_bus, key_slot,
                               i2c_address, onboarding_key_slot, template_path)
    output_config_file(config, path)


if __name__ == '__main__':
    main()
