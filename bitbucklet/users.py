import click
import os
import logging
import json

import requests
from requests import HTTPError

from bitbucklet.token import get_access_token, BearerAuth
from bitbucklet.urls import teams_url, team_invitations_url
from bitbucklet.groups_cli import __group_add_user

@click.group(name='users', help = 'Managing users')
def users_cli():
    pass

@click.command(name = 'list', help = 'List all the users (sort of)')
@click.option('--verbose', is_flag=True, default=False)
def list_users(verbose: bool):
    from tabulate import tabulate

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

    members = response.json()['values']
    
    table = [[member['user']['display_name'], member['user']['account_id'], member['user']['uuid']] for member in members ]
    headers = ['display_name', 'account_id', 'uuid']
    print(tabulate(table, headers=headers, showindex=range(1, len(table) + 1), tablefmt='github'))

@click.command(name = 'invite', help = 'Invite an user by their primary email')
@click.argument('email')
@click.argument('group', default='developers')
def add_user(email: str, group: str):
    import json
    # Since June 2019, BitBucket changed their policy which a new user
    # can only be invited via their email address. Once they accept the
    # invitation email address, their username will be added into the team
    # `developers`.
    
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    response = requests.put(
        f"{team_invitations_url()}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
        headers = {
            'Content-Type': 'application/json'
        },
        data = json.dumps({
            'email': email,
            'group_slug': group
        })
    )

    print(response.text)

@click.command(name = 'list-pending', help = 'List unaccepted invitations')
def list_pending_users():
    from tabulate import tabulate

    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    response = requests.get(
        f"{team_invitations_url()}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token)
    )

    invitations = response.json()
    headers = ['email', 'invited_by', 'utc_sent_on']
    table = [[i['email'], i['invited_by']['display_name'], i['utc_sent_on']] for i in invitations]
    print(tabulate(table, headers=headers, showindex=range(1, len(table) + 1), tablefmt='github'))

@click.command(name = 'del-invitation', help = 'Delete an unaccepted invitation')
@click.argument('email')
def delete_invitation(email: str):
    import json
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    response = requests.delete(
        f"{team_invitations_url()}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
        headers = {
            'Content-Type' : 'application/json'
        },
        data = json.dumps({
            'email' : email
        })
    )

    print(response)

@click.command(name = 'del', help = 'Delete an user')
@click.argument('username')
def del_user(username: str):
    # Removing a User out of a team is actually more complicated.
    # We need to look for all groups and the user's granted priviledges to repositories.
    raise NotImplementedError("This command is not inmplemented")

users_cli.add_command(list_users)
users_cli.add_command(add_user)
users_cli.add_command(list_pending_users)
users_cli.add_command(delete_invitation)
users_cli.add_command(del_user)
