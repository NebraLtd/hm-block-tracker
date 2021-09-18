import base64
import requests
from jinja2 import Template


def get_latest_snapshot_block():
    # Fetches latest snapshoted block from Helium API.
    resp = requests.get('https://api.helium.io/v1/snapshots')
    if resp.status_code == 200:
        return resp.json()['data'][0]
    else:
        raise Exception("Error fetching snapshot block from Helium API")


def convert_snapshot_to_blessed_block(snapshot):
    snapshot_hash = snapshot['snapshot_hash']
    snapshot_hash += "=" * ((3 - len(snapshot_hash) % 3) % 3)
    decoded_hash = base64.urlsafe_b64decode(snapshot_hash)
    erlang_array = '<<'
    integer_array = list(decoded_hash)
    for i in range(0, len(integer_array)):
        if i == len(integer_array) - 1:
            erlang_array += '%s' % str(integer_array[i])
        else:
            erlang_array += '%s,' % str(integer_array[i])
    erlang_array += '>>'
    return {
        'blessed_block': snapshot['block'],
        'blessed_block_hash': erlang_array
    }


def populate_template(blessed_block, template_file='config.template'):
    template = Template(open(template_file).read())
    block_id = blessed_block['blessed_block']
    block_hash = blessed_block['blessed_block_hash']
    output = template.render(
        blessed_block=block_id,
        blessed_block_hash=block_hash
    )
    return output


def output_config_file(config, path='docker.config'):
    open(path, "w").write(config)


def main():
    latest_snapshot = get_latest_snapshot_block()
    blessed_block = convert_snapshot_to_blessed_block(latest_snapshot)
    config = populate_template(blessed_block)
    output_config_file(config)


if __name__ == '__main__':
    main()
