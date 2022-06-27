def token_url():
    return 'https://bitbucket.org/site/oauth2/access_token'

# BitBucket Cloud API v2 does **NOT** have any endpoint for
# working with Groups. So here we HAD to use the v1.0 which
# was said to be deprecated and no longer functions.
# But apparently, it is still working.
def groups_url():
    return 'https://api.bitbucket.org/1.0/groups/{team}'

def teams_url():
    return 'https://api.bitbucket.org/2.0/workspaces/{team}'

def repos_url():
    return 'https://api.bitbucket.org/2.0/repositories/{team}'

def team_invitations_url():
    return "https://api.bitbucket.org/1.0/users/{team}/invitations"

# @deprecated
# Bitbucket internal API changed its internal behavior since 2022-01.
# It no longer works with "Authorization: Bearer".
# Usage of cloud.session.token requires csrftoken as well as header Referer.
def users_privileges_url():
    return 'https://bitbucket.org/!api/internal/privileges/{team}/{repo}/{user_id}/'

# @deprecated
# Bitbucket internal API changed its internal behavior since 2022-01.
# It no longer works with "Authorization: Bearer".
# Usage of cloud.session.token requires csrftoken as well as header Referer.
def groups_privileges_url():
    return 'https://bitbucket.org/!api/1.0/group-privileges/{team}/{repo}/{team_id}/{group}/?exclude-members=1'

def user_accesses_url():
    return "https://bitbucket.org/!api/internal/user/{team_id}/access/{user_id}"

# NOTE:
# This endpoint is still maintained by Atlassian for backward-compatibility
# because Bitbucket API 2.0 does not provide any similar feature.
def group_privileges_1_0_url():
    return "https://api.bitbucket.org/1.0/group-privileges/{team_id}/{repo}/{team}/{group}"
