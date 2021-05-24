import requests
import os
from dotenv import load_dotenv
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
# To set your BEARER_TOKEN, create a file .env and SET:
# 'Bearer_Token'='<your_bearer_token>'

Last_Id = None
def auth():
    load_dotenv()
    return os.getenv('Bearer_Token')


def create_url():
    # Replace with user ID below
    user_id = 738811218769633281
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id) if Last_Id == None else "https://api.twitter.com/2/users/{}/tweets?since_id={}".format(user_id,Last_Id)


def get_params():
    return {"tweet.fields": "created_at"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
    except:
        return 0


def Filter_Content(json_response):
    global Last_Id
    #Read New Content if available
    try:
        for key in json_response["data"]:
            SendWebhook(key["text"])
            time.sleep(2)
        #Set Last Id
        Last_Id = json_response["data"][0]["id"]
    except:
        pass

def SendWebhook(text):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/846475247133261917/9TOD50nCnCOWBMHsUQY7BOX_CpmKZ7mbTnvexS-fn1NDKoW9kenPMKxV-vhOtZip9LyN')
    embed = DiscordEmbed(description=text, color='03b2f8')
    embed.set_author(name='Fogos.pt (@FogosPt', url='https://twitter.com/FogosPt', icon_url='https://pbs.twimg.com/profile_images/740254226060840964/WDmRwu4v_200x200.jpg')
    embed.set_footer(text="Twitter", icon_url='https://pbs.twimg.com/profile_images/740254226060840964/WDmRwu4v_200x200.jpg')
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()


def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()
    json_response = connect_to_endpoint(url, headers, params)
    Filter_Content(json_response)


if __name__ == "__main__":
    while(1):
        main()
        #Read twitter every 10 seconds
        time.sleep(10)
