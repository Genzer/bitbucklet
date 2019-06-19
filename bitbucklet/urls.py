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

def team_invitations_url():
    return "https://api.bitbucket.org/1.0/users/{team}/invitations"