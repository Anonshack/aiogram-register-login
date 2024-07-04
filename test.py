import requests
import json

BOT_TOKEN = '7324009171:AAGUKEErtX8ABM2lnDpksNs1qfBV49Ylr4A'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'


def get_updates():
    url = BASE_URL + 'getUpdates'
    response = requests.get(url)
    return response.json()


if __name__ == '__main__':
    updates = get_updates()
    print(json.dumps(updates, indent=2))
