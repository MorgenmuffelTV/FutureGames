import requests
import json
import datetime as dt
import configparser

def get_token():
    config = configparser.ConfigParser()
    config.read_file(open('games.config'))
    client_id = config.get('authorisation', 'client_id')
    client_secret = config.get('authorisation', 'client_secret')

    response = requests.post("https://id.twitch.tv/oauth2/token?client_id="+client_id+"&client_secret="+client_secret+"&grant_type=client_credentials")
    print(response)
    # Writing to response to json
    token = response.json()

    expire_date = dt.datetime.now() + dt.timedelta(seconds=token["expires_in"])

    token["expire_date"] = expire_date.isoformat()
    print(token)

    with open("token.json", "w") as f:
        f.write(json.dumps(token))

if __name__ == '__main__':
    get_token()