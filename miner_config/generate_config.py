import requests
from jinja2 import Template


def get_latest_snapshot_block():
    # Fetches latest snapshoted block from Helium API.
    # resp = requests.get('https://helium-snapshots.nebra.com/latest.json')
    cache = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
    }
    resp = requests.get(
      'https://storage.googleapis.com/helium-snapshots.nebra.com/latest.json',
      headers=cache
    )
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception("Error fetching snapshot block from Helium API")


def populate_template(blessed_block, template_file='config.template'):
    template = Template(open(template_file).read())
    block_id = blessed_block['height']
    block_hash = blessed_block['hash']
    output = template.render(
        blessed_block=block_id,
        blessed_block_hash=block_hash
    )
    return output


def output_config_file(config, path='docker.config'):
    open(path, "w").write(config)


def main():
    latest_snapshot = get_latest_snapshot_block()
    config = populate_template(latest_snapshot)
    output_config_file(config)


if __name__ == '__main__':
    main()
