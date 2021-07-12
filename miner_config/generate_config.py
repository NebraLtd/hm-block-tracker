from jinja2 import Template

from miner_config.parse_config import read_sys_config_file
from miner_config.parse_config import get_blessed_block


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
    config_lines = read_sys_config_file()
    blessed_block = get_blessed_block(config_lines)
    config = populate_template(blessed_block)
    output_config_file(config)


if __name__ == '__main__':
    main()
