import util.status_util as status
import util.luna_util as luna
import pytz
import time

from datetime import datetime

DISCORD_TOKEN_PATH = 'token.env'
WEATHER_KEY_PATH = 'weather_key.env'

def run_updates(token, key):
    # Gets the current Discord status, preserves text if any.
    current_status = status.retrieve_status(token)
    if(current_status[status.STATUS]):
        current_text = current_status[status.STATUS]['text']
    else:
        current_text = None
    # Retrieves the moon phase for the current date, gets the moon phase emoji.
    emoji = luna.moon_phase_to_emoji(
        luna.get_moon_phase(key, luna.format_current_date())
    )
    # Build new status.
    if current_text is None:
        new_status = status.build_status(emoji_name=emoji)
    else:
        new_status = status.build_status(text=current_text, emoji_name=emoji)
    # Debug
    now = datetime.now(pytz.timezone('America/Chicago'))
    print(
        f'{now}: Status is being updated.\n'
        + f'For user: {token}\n'
        + f'New status contents: {new_status}\n'
    )
    status.publish_status(token, new_status)

def main():
    '''
    Main loop to continuously monitor and update status information.
    This is scheduled to retrieve lunar data and post an updated status twice per day,
    at 0:00 and 12:00 UTC-5.
    Calls to publish_status will preserve previously-existing status text, if any.
    '''
    # Retrieve Discord token and Visual Crossing key from file paths.
    # Make sure these exist...
    token = status.retrieve_token(DISCORD_TOKEN_PATH)
    key = luna.retrieve_key(WEATHER_KEY_PATH)

    run_updates(token, key)
    while True:
        now = datetime.now(pytz.timezone('America/Chicago'))
        hour = now.hour
        print(f'TIME LOG: {now}')
        if hour == 12 or hour == 0:
            run_updates(token, key)
            print(f'Status changed successfully! Sleeping for 1 hour...')
            time.sleep(3600)
        else:
            print(f'No status change. Sleeping for 30 minutes...')
            time.sleep(1800)

if __name__ == '__main__':
    main()