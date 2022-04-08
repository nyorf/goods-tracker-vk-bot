from tokens import TOKEN
import requests
import random
import time


def sendMessage(user_id, message):
    response = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = f"user_id={user_id}&random_id={int(time.time())}&message={message}",
        token = TOKEN,
        version = 5.131
    ))

    return response



test = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
    method = "users.get",
    parameters = "user_ids=210700286&fields=bdate",
    token = TOKEN,
    version = 5.131
))

sendMessage(201215884, int(time.time()))
