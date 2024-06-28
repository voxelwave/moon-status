import requests
import json
import pytz

from datetime import datetime

# Constants related to Visual Crossing API access 
POSTAL = '12345' # Random postal code in New York. The API requires a location
                 # for the query, but it's unnecessary here since I'm just
                 # using it to retrieve the moon phase. Put whatever here.
VC_ENDPOINT = ('https://weather.visualcrossing.com/'
               + f'VisualCrossingWebServices/rest/services/timeline/{POSTAL}')
AUTH_HEADER = 'key'

### VISUAL CROSSING API FUNCTIONS ###

def retrieve_key(path: str) -> str:
    '''
    Retrieves the API key from the specified filepath.
    Raises an exception if the filepath is invalid.
    Doesn't test API access due to limitations on number of allowed queries.
    '''
    key = None
    try:
        file = open(path)
        key = file.readline()
    except OSError as e:
        print(f'Something went wrong while retrieving the token: {e}')
    if not key is None:
        return key

def get_moon_phase(key: str, date_str: str) -> float:
    '''
    Retrieves the moon phase for the date (as a float, 0.0~1.0) 
    from Visual Crossing using the given API key.
    Date must be formatted as "YYYY-MM-DD".
    Raises an exception if this fails.
    '''
    try:
        auth_param = {AUTH_HEADER: key}
        response_dict = json.loads(
            requests.get(f'{VC_ENDPOINT}/{date_str}', params=auth_param).content)
        if ('days' in response_dict) and ('moonphase' in response_dict['days'][0]):
            # see sample API response for this... too much nested data to bother here.
            return response_dict['days'][0]['moonphase']
    except Exception as e:
        print(f'Something went wrong retrieving the current moon phase: {e}')

def moon_phase_to_emoji(phase: float) -> str:
    '''
    Helper function to take the current moon phase as a double (percentage),
    and return the emoji that corresponds to the moon phase.
    Moon phase percentage should be retrieved from get_moon_phase().
    See: 
    https://www.visualcrossing.com/resources/documentation/weather-api/
    '''
    phase_int = int(phase * 100)
    if phase_int in range(6, 20):
        return '🌒'
    if phase_int in range(20, 31): # 25
        return '🌓'
    if phase_int in range(31, 45):
        return '🌔'
    if phase_int in range(45, 56): # 50
        return '🌕'
    if phase_int in range(56, 70):
        return '🌖'
    if phase_int in range(70, 81): # 75
        return '🌗'
    if phase_int in range(81, 95):
        return '🌘'
    else:
        return '🌑' # 0
    
def format_current_date() -> str:
    '''
    Helper function to get today's date (CDT) in YYYY-MM-DD format.
    '''
    return datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d')