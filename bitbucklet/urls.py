def token_url():
    return 'https://bitbucket.org/site/oauth2/access_token'

# BitBucket Cloud API v2 does **NOT** have any endpoint for
# working with Groups. So here we HAD to use the v1.0 which
# was said to be deprecated and no longer functions.
# But apparently, it is still working.
def groups_url():
    return 'https://api.bitbucket.org/1.0/groups/{team}'

def teams_url():
    return 'https://api.bitbucket.org/2.0/teams/{team}'

def repos_url():
    return 'https://api.bitbucket.org/2.0/repositories/{team}'

def team_invitations_url():
    return "https://api.bitbucket.org/1.0/users/{team}/invitations"

def users_privileges_url():
    return 'https://bitbucket.org/!api/internal/privileges/{team}/{repo}/{user_id}/'

def groups_privileges_url():
    return 'https://bitbucket.org/!api/1.0/group-privileges/{team}/{repo}/{team_id}/{group}/?exclude-members=1'

def user_accesses_url():
    return "https://bitbucket.org/!api/internal/user/{team_id}/access/{user_id}"
