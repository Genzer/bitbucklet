import click
import os
import logging
import json
import time
from tabulate import tabulate
from typing import Tuple, List

import requests
from requests import HTTPError

from bitbucklet.token import get_access_token, BearerAuth
from bitbucklet.urls import teams_url, user_accesses_url

@click.group(name='accesses', help = 'Managing accesses')
def accesses_cli():
    pass

@click.command(name='list-all', help='List all accesses of all users')
@click.option("-f", "--format", "format", type=click.Choice(['table', 'json', 'pipe'], case_sensitive=False), help="Format the output")
def get_all_user_accesses(format: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    bitbucket_cloud_session = os.getenv('BITBUCKET_CLOUD_SESSION')

    access_token = get_access_token()

    # TODO: Handle pagination
    get_all_users_response = requests.get(
        f"{teams_url()}/members"
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
    )
    
    if get_all_users_response.status_code != 200:
        raise RuntimeError(get_all_users_response.status_code)

    members = [(member['display_name'], member['account_id'])
        for member in get_all_users_response.json()['values']]
    
    get_team_response = requests.get(
        teams_url()
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token)
    )
    
    if get_team_response.status_code != 200:
        logging.error(get_team_response)
        raise RuntimeError(f"Fail to obtain team {bitbucket_team_name}")

    bitbucket_team_uuid = get_team_response.json()['uuid']
    cookies = {
        'optintowebauth' : '1',
        'cloud.session.token': bitbucket_cloud_session
    }

    all_members_accesses = []

    for display_name, user_uuid in members:
        logging.debug(f"Fetching {display_name}")
        users_accesses = __get_user_accesses(
            user_accesses_url()
            .format(
                team_id=bitbucket_team_uuid,
                user_id=user_uuid
                ),
            cookies=cookies
        )

        all_members_accesses.append(users_accesses)
        # IMPORTANT
        # ----
        # Workaround for Rate Limiting.
        # Too many requests sent in a short period of time will trigger BitBucket
        # to block the subsequent requests.
        time.sleep(2)

    FORMATTERS = {
        'default': __tabulate_format,
        'table': __tabulate_format,
        'json': __json_format,
        'pipe': __pipe_format
    }

    formatter = FORMATTERS.get(format, FORMATTERS.get('default'))
    formatter(all_members_accesses)

def __tabulate_format(all_member_accesses: List[Tuple]):
    headers = ['user', 'user_id', 'repos', 'groups']
    table = []
    for display_name, account_id, repos, groups in all_member_accesses:
        table.append( [
                display_name,
                account_id,
                '\n'.join(repos),
                '\n'.join(groups)
            ])
    print(tabulate(table, headers=headers, showindex=range(1, len(table) + 1), tablefmt='pipe'))
    return None

def __json_format(all_member_accesses: List[Tuple]):
    result = []
    for display_name, account_id, repos, groups in all_member_accesses:
        result.append({
            'display_name': display_name,
            'account_id': account_id,
            'repos': repos,
            'groups': groups
        })
    print(json.dumps(result,indent=2))

def __pipe_format(all_member_accesses: List[Tuple]):
    """Prints out in stdin using a format that it is possible to pipe
    into another command like `awk`.
    """
    for display_name, account_id, repos, groups in all_member_accesses:
        for repo in repos:
            print(f"{display_name}\t{account_id}\t{repo}")

def __get_user_accesses(url, **options) -> Tuple[str, str, List[str], List[str]]:
    response = requests.get(
        url,
        **options
    )

    logging.debug(response.json())

    access_summary = response.json()

    repos = [ repo['name'] for repo in access_summary['repos'] ]
    groups = [ group['slug'] for group in access_summary['groups']]
    return (access_summary['user']['display_name'], access_summary['user']['account_id'], repos, groups)


@click.command(name='list', help='List all accesses of a user')
@click.argument('user', required=True)
def get_user_accesses(user: str):
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    bitbucket_cloud_session = os.getenv('BITBUCKET_CLOUD_SESSION')

    access_token = get_access_token()

    get_team_response = requests.get(
        teams_url()
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token)
    )
    
    if get_team_response.status_code != 200:
        logging.error(get_team_response)
        raise RuntimeError(f"Fail to obtain team {bitbucket_team_name}")

    bitbucket_team_uuid = get_team_response.json()['uuid']

    cookies = {
        'optintowebauth' : '1',
        'cloud.session.token': bitbucket_cloud_session
    }

    logging.debug(f"cookies: {cookies}")

    response = requests.get(
        user_accesses_url()
            .format(
                team_id=bitbucket_team_uuid,
                user_id=user
                ),
        cookies=cookies
    )

    logging.debug(response.json())

    access_summary = response.json()

    repos = [ repo['name'] for repo in access_summary['repos'] ]
    groups = [ group['slug'] for group in access_summary['groups']]

    headers = ['user', 'user_id', 'repos', 'groups']
    table = [[access_summary['user']['display_name'],
        access_summary['user']['uuid'],
        '\n'.join(repos),
        '\n'.join(groups)
    ]]
    print(tabulate(table, headers=headers, showindex=range(1, len(table) + 1), tablefmt='pipe'))


accesses_cli.add_command(get_user_accesses)
accesses_cli.add_command(get_all_user_accesses)