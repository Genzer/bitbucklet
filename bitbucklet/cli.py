import click
import os
import logging

from bitbucklet.token import token_cli
from bitbucklet.groups_cli import groups_cli
from bitbucklet.users import users_cli
from bitbucklet.config import cfg_cli
from bitbucklet.repos import repos_cli

@click.group(no_args_is_help=True)
@click.option('--debug', is_flag=True, default=False, help='Print log in DEBUG level')
@click.version_option()
def main(debug):
    from dotenv import load_dotenv
    from pathlib import Path

    load_dotenv(dotenv_path=Path.home() / '.bitbucklet')
    if os.getenv('BITBUCKLET_CONFIG_FILE') is not None:
        load_dotenv(load_dotenv=os.getenv('BITBUCKLET_CONFIG_FILE'), override=True)
    load_dotenv(dotenv_path=Path('.') / '.env', override=True)

    logging.basicConfig(level=logging.INFO)
    
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

main.add_command(token_cli)
main.add_command(groups_cli)
main.add_command(users_cli)
main.add_command(cfg_cli)
main.add_command(repos_cli)

if __name__ == "__main__":
    main()