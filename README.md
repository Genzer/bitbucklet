# bitbucklet - BitBucket CLI

This is a small CLI developed to interact with BitBucket Cloud API for easily manipulate the BitBucket Team.

[TOC]

## Prerequisites

### Installation

You can install `bitbucklet` through the Releases on GitHub page.

```bash
pip install https://github.com/Genzer/bitbucklet/archive/${version}.tar.gz
```

### OAuth Consumer

If you don't have a dedicated BitBucket App, you can create an OAuth Consumer.

The Scopes of the OAuth token needs to have:

```text
repository:write
repository:admin
account:write
team:write
project:write"
```

#### bitbucklet Configuration File

In order to use this CLI, the following environment variables are required:

| Variable                | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| BITBUCKET_TEAM          | Your BitBucket team ID                                  |
|                         | This could be either your Team's username or UUID.      |
| BITBUCKET_CLIENT_ID     | Your OAuth consumer ID                                  |
| BITBUCKET_CLIENT_SECRET | Your OAuth consumer Secret                              |
| BITBUCKET_CLOUD_SESSION | The token issued for accessing BitBucket Cloud from     |
|                         | brower. See the section "# BitBucket Cloud Session".    |

The configuration is loaded in order (the latter overrides the former):

- The `$HOME/.bitbucklet` file.
- The file defined using environment variable `BITBUCKLET_CONFIG_FILE`.
- The `.env` at the current `PYTHON_PATH`.

Tips: You can generate an empty configuration file using the command:

```bash
bitbucklet cfg make-blank
```

## Usage

The help of the CLI should be helpful enough.

```shell
$ bitbucklet --help

Usage: bitbucklet [OPTIONS] COMMAND [ARGS]...

Options:
    --debug  Print log in DEBUG level
    --help   Show this message and exit.

Commands:
    accesses  Managing accesses
    cfg
    groups  Managing groups
    repos   Managing repositories
    tokens  Tokens
    users   Managing users
```

Some common use case:

```bash
# List all users
bitbucklet users list

# List all groups
bitbucklet groups list

# List users of group `developers`.
# Please note, `developers` is a slug of the group.
bitbucklet groups list-user developers

# Add a user into the team
# Here you can use both username or primary email address.
bitbucklet users invite new_user@myorg.com


# Grant 'write' permission for a User to a Repository
bitbucklet repos grant -u $USER_UIID --access read awesome-repository

# Revoke access of a User
bitbucklet repos revoke -u $USER_UUID awesome-repository

# Check accesses granted for a specific user whose id is abcdefghijklmn0123.
bitbucklet accesses list abcdefghijklmn0123

# List all accesses of all users in the workspace.
# KNOWN LIMITATIONS: This command does not handle pagination.
bitbucklet accesses list-all
```

## Development

The CLI mainly uses [`Click`](https://click.palletsprojects.com/en/7.x/).

To start develop:

```shell
$ cd bitbucklet
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python -m pip install -r requirement.txt
```

To install as a CLI:

```shell
$ pip install --editable .
$ bitbucklet --help
```

### Release

```shell
$ pip setup.py sdist
```

## BitBucket Cloud Session

Some command in `bitbucklet` (i.e `accesses`) makes use some **internal** APIs being used by BitBucket Cloud Web.

In order to authenticate with these APIs, we have to obtain a cookie named `cloud.session.token` from the browser.

The following steps guide you how to get it:

1 - Open browser (i.e Chrome) and go to https://bitbucket.org/yourorganization.

2 - Log in. Make sure your account is in "Administrator" group.

3 - Open Developer Tools or Inspect and obtain he cookie `cloud.session.token`.

4 - Save it into the `bitbucklet` configuration file (ie `~/.bitbucklet`).

