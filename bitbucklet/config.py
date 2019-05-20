import click
from typing import Type
from pathlib import Path

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
        from inspect import cleandoc
        dotenv.write(cleandoc("""
        # Here are very important environment variables
        # required by bitbucket_cli.

        # The user used here should be granted with
        # enough permissions. See README.md OAuth
        BITBUCKET_USERNAME=
        BITBUCKET_PASSWORD=

        # If you don't have a dedicated BitBucket App, simply
        # create an OAuth2 Consumer in your BitBucket Settings.
        BITBUCKET_CLIENT_ID=
        BITBUCKET_CLIENT_SECRET=

        BITBUCKET_TEAM=
        """))

cfg_cli.add_command(generate_empty_bitbucklet_dotenv)