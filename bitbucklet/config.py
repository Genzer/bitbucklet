import click
from typing import Type
from pathlib import Path

BITBUCKLET_DOTENV_TEMPLATE = Path(__file__).parent / '__bitbucklet_config_template.env'

@click.group(name = 'cfg')
def cfg_cli():
    pass

@click.command(name = 'make-blank')
@click.argument('path', required=False, type=click.Path(exists=False, writable=True))
@click.option('-o', '--overwrite', is_flag=True, default=False, help="Overwrite existing file")
def generate_empty_bitbucklet_dotenv(overwrite: bool, path: click.Path):

    bitbucklet_dotenv_at_home = Path.home() / '.bitbucklet' if path is None else Path(path)

    if bitbucklet_dotenv_at_home.exists() and not overwrite:
        from click import BadParameter
        raise BadParameter(f"Path {bitbucklet_dotenv_at_home} is existing. Use --overwrite to overwirte its content.")

    with open(bitbucklet_dotenv_at_home, 'w') as dotenv:
        with open(BITBUCKLET_DOTENV_TEMPLATE, 'r') as template:
            dotenv.write(template.readlines)

cfg_cli.add_command(generate_empty_bitbucklet_dotenv)