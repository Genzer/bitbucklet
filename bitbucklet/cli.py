import click
import os
import logging

from bitbucklet.token import token_cli
from bitbucklet.groups_cli import groups_cli
from bitbucklet.users import users_cli

@click.group()
@click.option('--debug', is_flag=True, default=False, help='Print log in DEBUG level')
def main(debug):
    from dotenv import load_dotenv
    from pathlib import Path

    load_dotenv(dotenv_path=Path('.') / '.env')
    
    if debug:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

main.add_command(token_cli)
main.add_command(groups_cli)
main.add_command(users_cli)

if __name__ == "__main__":
    main()