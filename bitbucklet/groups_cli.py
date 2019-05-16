import click
import os
import logging
import json

import requests
from requests import HTTPError

from bitbucklet.token import get_access_token, BearerAuth
from bitbucklet.urls import groups_url

@click.group(name='groups', help = 'Managing groups')
def groups_cli():
    pass

@click.command(name='add', help = 'Add a new group')
@click.argument('group_name')
def groups_add(group_name: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    # See
    # https://confluence.atlassian.com/bitbucket/groups-endpoint-296093143.html#groupsEndpoint-PUTnewmemberintoagroup
    response = requests.post(
        f"{groups_url()}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
        data = f"name={group_name}"
    )

    print(response.text)

@click.command(name='list', help = 'List all groups')
@click.option('--verbose', is_flag=True, default=False, help="Print JSON output")
def groups_list(verbose: bool):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')

    access_token = get_access_token()
    response = requests.get(
        groups_url().format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
    )
    if verbose:
        print(json.dumps(json.loads(response.text), indent=2))
        return

    groups = response.json()
    [print(group['slug']) for group in groups]

@click.command(name='del', help = 'Delete a group')
@click.argument('group_name')
def groups_del(group_name: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    # See
    # https://confluence.atlassian.com/bitbucket/groups-endpoint-296093143.html#groupsEndpoint-DELETEamember
    response = requests.delete(
        f"{groups_url()}/{group_name}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token)
    )
    if response.status_code == 204:
        print('OK')
        return

    raise HTTPError(response.text)
    

@click.command(name='list-users', help = 'List all the users in a group')
@click.option('--verbose', is_flag=True, default=False, help="Print JSON output")
@click.argument('group_name')
def groups_list_user(verbose: bool, group_name: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')

    access_token = get_access_token()
    response = requests.get(
        f"{groups_url()}/{group_name}/members".format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
    )

    if response.status_code != 200:
        raise HTTPError(response.text)

    if verbose:
        print(json.dumps(json.loads(response.text), indent=2))
        return

    members = response.json()
    [print(member['username']) for member in members]

@click.command(name='add-user', help = 'Add a user into a group')
@click.argument('group_name')
@click.argument('username')
def groups_add_user(group_name: str, username: str):
    __group_add_user(group_name, username)

# extracted it into a private method for re-use in users.py
def __group_add_user(group_name: str, username: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    # See
    # https://confluence.atlassian.com/bitbucket/groups-endpoint-296093143.html#groupsEndpoint-PUTnewmemberintoagroup
    response = requests.put(
        f"{groups_url()}/{group_name}/members/{username}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
        # Required by the API
        headers = {
            'Content-Type' : 'application/json'
        },
        # Required by the API
        data = '{}'
    )

    print(response)

@click.command(name='del-user', help = 'Delete a user from a group')
@click.argument('group_name')
@click.argument('username')
def groups_del_user(group_name: str, username: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    # See
    # https://confluence.atlassian.com/bitbucket/groups-endpoint-296093143.html#groupsEndpoint-DELETEamember
    response = requests.delete(
        f"{groups_url()}/{group_name}/members/{username}"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token)
    )
    if response.status_code == 204:
        print('OK')
        return

    raise HTTPError(response.text)
    

groups_cli.add_command(groups_add)
groups_cli.add_command(groups_list)
groups_cli.add_command(groups_del)

groups_cli.add_command(groups_add_user)
groups_cli.add_command(groups_list_user)
groups_cli.add_command(groups_del_user)