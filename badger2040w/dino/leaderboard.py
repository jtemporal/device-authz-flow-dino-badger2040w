import urequests


API_CONFIG_PATH = "/dino/api-config.txt"

DEFAULT_TEXT = "http://localhost:4040"


def config_api():
    # global auth0_request_data
    # Open the auth0 config file
    try:
        api_config = open(API_CONFIG_PATH, "r")
    except OSError:
        with open(API_CONFIG_PATH, "w") as f:
            f.write(DEFAULT_TEXT)
            f.flush()
        api_config = open(API_CONFIG_PATH, "r")
    
    API_DOMAIN = api_config.readline()
    return API_DOMAIN.strip('\n')



def set_user_score(access_token, score):
    if access_token == 'error':
        print("something went wrong")
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://{config_api()}/scores?score={str(score)}"
    print(url)
    response = urequests.post(
        url,
        headers=headers
    )
    
    print("Score set with API")

    
# This is where you implement other API calls
