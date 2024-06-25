import requests
import json

# Constants related to Discord API access
DISCORD_ENDPOINT = 'https://discord.com/api/v10/users/@me/settings'
AUTH_HEADER = 'authorization'
STATUS = 'custom_status' # Identifier for custom statuses in JSON response

### DISCORD API FUNCTIONS ###

def retrieve_token(path: str) -> str:
    '''
    Retrieves the Discord auth token from the specified filepath and 
    tests its validity.
    Raises an exception if the filepath or the token is invalid.
    '''
    token = None
    try:
        file = open(path)
        token = file.readline()
        header = {AUTH_HEADER: token}
        response = requests.get(DISCORD_ENDPOINT, headers=header)
        if not response.ok:
            raise requests.HTTPError
    except (OSError, requests.HTTPError) as e:
        print(f'Something went wrong while retrieving the token: {e}')
    if not token is None:
        return token

def retrieve_status(token: str) -> dict:
    '''
    Retrieves the current Discord status of the user with the given token 
    as a Python dictionary (parsing JSON automatically).
    Raises an exception if this fails.
    '''
    try:
        response_dict = json.loads(
            requests.get(DISCORD_ENDPOINT, headers={AUTH_HEADER: token}).content)
        if STATUS in response_dict:
            # the custom_status key is required as well. response is a nested dict
            return {STATUS: response_dict[STATUS]}
    except Exception as e:
        print(f'Something went wrong retrieving user status: {e}')

def build_status(text: str = None, 
                 expires_at: str = None, 
                 emoji_id: str = None, 
                 emoji_name: str = None
                ) -> str:
    '''
    Dumps a JSON string for a custom Discord status given optional arguments.
    '''
    status_dict = {STATUS: {}}
    if text:
        status_dict[STATUS]["text"] = text
    if expires_at:
        status_dict[STATUS]["expires_at"] = expires_at
    if emoji_id:
        status_dict[STATUS]["emoji_id"] = emoji_id
    if emoji_name:
        status_dict[STATUS]["emoji_name"] = emoji_name
    return status_dict

def publish_status(token: str, custom_status: dict) -> None:
    '''
    Publishes the given custom status to the user's account whose token matches.
    Throws an exception if Discord returns a bad response and prints the response.
    '''
    header = {AUTH_HEADER: token}
    r = requests.patch(DISCORD_ENDPOINT, json=custom_status, headers=header)
    try:
        if not r.ok:
            raise requests.HTTPError
    except requests.HTTPError as e:
        print(f'Something went wrong publishing the status: {e}')
