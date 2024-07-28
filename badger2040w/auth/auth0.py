AUTH0_CONFIG_PATH = "/auth/config.txt"

DEFAULT_TEXT = """your-domain.auth0.com
your-client-id
algorithms
"""


def config_auth0():
    # global auth0_request_data
    # Open the auth0 config file
    try:
        auth0_config = open(AUTH0_CONFIG_PATH, "r")
    except OSError:
        with open(AUTH0_CONFIG_PATH, "w") as f:
            f.write(DEFAULT_TEXT)
            f.flush()
        auth0_config = open(AUTH0_CONFIG_PATH, "r")

    # Read in the next lines
    AUTH0_DOMAIN = auth0_config.readline()
    AUTH0_CLIENT_ID = auth0_config.readline()
    ALGORITHMS = auth0_config.readline()
    AUDIENCE = auth0_config.readline()
    

    auth0_request_data = {
        "domain": AUTH0_DOMAIN.strip('\n'),
        "client_id": AUTH0_CLIENT_ID.strip('\n'),
        "algorithms": [ALGORITHMS.strip('\n')],
        "audience": AUDIENCE.strip('\n')
    }
    
    auth0_config.close()
    return auth0_request_data