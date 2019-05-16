import click
import os
import logging
import json

import requests
from requests import HTTPError

from bitbucklet.token import get_access_token, BearerAuth
from bitbucklet.urls import teams_url
from bitbucklet.groups_cli import __group_add_user

@click.group(name='users', help = 'Managing users')
def users_cli():
    pass

@click.command(name = 'list', help = 'List all the users (sort of)')
@click.option('--verbose', is_flag=True, default=False)
def list_users(verbose: bool):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')

    access_token = get_access_token()
    response = requests.get(
        f"{teams_url()}/members"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
    )

    if verbose:
        print(json.dumps(json.loads(response.text), indent=2))
        return

    members = response.json()
    [print(member['username']) for member in members['values']]

@click.command(name = 'add', help = 'Add an user')
@click.argument('username')
def add_user(username: str):
    # Normally, adding a user into any group making it a member of the Team.
    # By default, BitBucket creates two groups `administrators` and `developers`.
    # So obviously, adding a new user into `developers` makes sense here.
    __group_add_user('developers', username)

@click.command(name = 'del', help = 'Delete an user')
@click.argument('username')
def del_user(username: str):
    # Removing a User out of a team is actually more complicated.
    # We need to look for all groups and the user's granted priviledges to repositories.
    raise NotImplementedError("This command is not inmplemented")

users_cli.add_command(list_users)
users_cli.add_command(add_user)
users_cli.add_command(del_user)
