import click
import os
import logging
import json
from typing import Tuple

import requests
from requests import HTTPError

from bitbucklet.token import get_access_token, BearerAuth
from bitbucklet.urls import teams_url, users_privileges_url, groups_privileges_url, repos_url

@click.group(name='repos', help = 'Managing repositories and their permissions')
def repos_cli():
    pass

@click.command(name = 'list-in-project', help = 'List repositories in a project')
@click.argument("project")
def list_in_project(project: str) -> None:
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    get_repos_in_project_response = requests.get(
        repos_url()
            .format(team=bitbucket_team_name),
        auth = BearerAuth(access_token),
        params = {
            'q': f"project.key=\"{project}\"",
            'pagelen': 100
        }
    )
    
    if get_repos_in_project_response.status_code != 200:
        logging.error(get_repos_in_project_response.text)
        raise RuntimeError(f"Fail to obtain repositories in project {project} in team {bitbucket_team_name}")

    repositories = get_repos_in_project_response.json()['values']
    names = [repo['name'] for repo in repositories]
    for name in names:
        print(name)

@click.command(name = 'grant', help = 'Grant access to user or group')
@click.option("-u", "--user", "user", help="Id (bitbucket) of the user. Mutual exists with --group")
@click.option("-g", "--group", "group", help="Group slug. Mutual exists with --user")
@click.option("-a", "--access", type=click.Choice(["read", "write", "admin"], case_sensitive=False), required=True)
@click.argument("repo")
def grant_access(access: str, repo: str, user: str, group: str):

    if group:
        return __grant_group_access(group, access, repo)

    if user:
        return __grant_user_access(user, access, repo)
    
    raise NotImplementedError("You should not be here")

def __grant_group_access(group_slug: str, access: str, repo: str):
    logging.info(f"Grant group {group_slug} to {access} on {repo}")
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
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

    response = requests.put(
        groups_privileges_url()
            .format(
                team=bitbucket_team_name,
                team_id=bitbucket_team_uuid,
                repo=repo,
                group=group_slug),
        auth = BearerAuth(access_token),
        headers = {
            'Content-Type': 'text/plain'
        },
        data = access,
    )

    print(response)

def __grant_user_access(user_id: str, access: str, repo: str):
    logging.info(f"Grant user {user_id} to {access} on {repo}")
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    response = requests.put(
        users_privileges_url()
            .format(
                team=bitbucket_team_name,
                repo=repo,
                user_id=user_id),
        auth = BearerAuth(access_token),
        headers = {
            'Content-Type': 'text/plain'
        },
        data = access,
    )

    print(response)

@click.command(name = 'revoke', help = 'Revoke access to user or group')
@click.option("-u", "--user", "user", help="Id (bitbucket) of the user. Mutual exists with --group")
@click.option("-g", "--group", "group", help="Group slug. Mutual exists with --user")
# @click.option("-a", "--access", type=click.Choice(["read", "write", "admin"], case_sensitive=False), required=True)
@click.argument("repo")
def revoke_access(repo: str, user: str, group: str):
    if group:
        return __revoke_group_access(group, repo)

    if user:
        return __revoke_user_access(user, repo)
    
    raise NotImplementedError("You should not be here")


def __revoke_group_access(group_slug: str, repo: str):
    logging.info(f"Revoke group {group_slug} to access on {repo}")
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
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

    response = requests.delete(
        groups_privileges_url()
            .format(
                team=bitbucket_team_name,
                team_id=bitbucket_team_uuid,
                repo=repo,
                group=group_slug),
        auth = BearerAuth(access_token),
    )

    print(response)

def __revoke_user_access(user_id: str, repo: str):
    logging.info(f"Revoke user {user_id} to access on {repo}")
    bitbucket_team_name = os.getenv('BITBUCKET_TEAM')
    access_token = get_access_token()

    response = requests.delete(
        users_privileges_url()
            .format(
                team=bitbucket_team_name,
                repo=repo,
                user_id=user_id),
        auth = BearerAuth(access_token),
    )

    print(response)

repos_cli.add_command(grant_access)
repos_cli.add_command(revoke_access)
repos_cli.add_command(list_in_project)
