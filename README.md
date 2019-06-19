# bitbucklet - BitBucket CLI

This is a small CLI developed to interact with BitBucket Cloud API for easily manipulate the BitBucket Team.

[TOC]

## Prerequisites

### OAuth Consumer

If you don't have a dedicated BitBucket App, you can create an OAuth Consumer 

The Scopes of the OAuth token needs to have:

```text
repository:write
repository:admin
account:write
team:write
project:write"
```

#### The `.env` File

In order to use this CLI, the following environment variables are required:

| Variable                | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| BITBUCKET_TEAM          | Your BitBucket team ID                                  |
| BITBUCKET_CLIENT_ID     | Your OAuth consumer ID                                  |
| BITBUCKET_CLIENT_SECRET | Your OAuth consumer Secret                              |
| BITBUCKET_USERNAME      | The username to authorize access to BitBucket resources |
| BITBUCKET_PASSWORD      | The password of the username                            |

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
    groups  Managing groups
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

## Release

```shell
$ pip setup.py sdist
```