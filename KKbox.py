import sys
import requests as requests

from linebot import LineBotApi
import random
from linebot.models import TextSendMessage

import os

LINE_UUID = os.environ['LINE_UUID']
TOKEN = os.environ['TOKEN']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


# 取得憑證Token
def get_token():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",  #內容類型
        "Host": "account.kkbox.com"
    }
    # 參數
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    r = requests.post('https://account.kkbox.com/oauth2/token', data=data, headers=headers)  # API網址取得憑證

    response = r.json()  # 轉換成dictionary

    if 'error' in response:
        print(response['error'])
        sys.exit()
    return response['access_token']  # 取得憑證(Access Token)欄位資料


def show_type(access_token):
    # 取得音樂排行榜列表API網址
    url = "https://api.kkbox.com/v1.1/charts"
    # 標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  # 帶著存取憑證
    }
    # 參數
    params = {
        "territory": "TW"  # 台灣領域
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()["data"]
    for item in result:
        print(item["id"], item["title"])


def get_raking(chart, access_token, num: int = 5) -> list:
    url = "https://api.kkbox.com/v1.1/charts/"+chart+"/tracks"
    # 標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token  # 帶著存取憑證
    }
    # 參數
    params = {
        "territory": "TW"  # 台灣領域
    }
    response = requests.get(url, headers=headers, params=params)

    result = []

    raking = response.json()["data"]
    for item in raking[:num]:
        # print([item["name"], item["url"]])
        result.append((item["name"], item["url"]))

    return result

result = []
if __name__ == '__main__':
    # doc
    # https://www.learncodewithmike.com/2020/02/python-kkbox-open-api.html

    access_token = get_token()

    # show_type(access_token)
    raking = get_raking('LZPhK2EyYzN15dU-PT', access_token)


    for song_name, _ in raking:
        result.append(song_name)
        print(song_name)

line_uuid = LINE_UUID
line_bot_api = LineBotApi(TOKEN)
line_bot_api.push_message(
    line_uuid,
    TextSendMessage(text = "流行音樂榜:"+"\n"+"1."+result[0]+"\n"+"2."+result[1]+"\n"+"3."+result[2]+"\n"+"4."+result[3]+"\n"+"5."+result[4]))

