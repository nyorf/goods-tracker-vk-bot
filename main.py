from distutils.command import upload
from tokens import TOKEN
from websites import *
import sys
import requests
import random
import time
import json

API_VERSION = 5.131

messages = {
    "itemAdded": "Товар {} был успешно добавлен в список отслеживаемых.",
    "itemRemoved": "Товар {} был успешно удалён из списка отслеживаемых.",
    "itemList": "Список отслеживаемых товаров: {}",
    "nowAvailable": "Отслеживаемый вами товар появился в наличии.",
    "nowAvailable_alt": "{} теперь в наличии на {}!"
}

sticker_ids = {
    "almond_cool": "53453",
    "almond_ok": "53446",
    "sonechka_you_died": "57164"
}

def sendTextMessage(user_id, message, reply_id=None):
    response = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&message={}&reply_to={}&dont_parse_links={}".format(
            user_id,
            int(time.time()),
            message,
            reply_id,
            1
        ),
        token = TOKEN,
        version = API_VERSION
    ))

    return response


def sendStickerMessage(user_id, sticker_id, reply_id=None):
    response = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&sticker_id={}&reply_to={}".format(
            user_id,
            int(time.time()),
            sticker_id,
            reply_id
        ),
        token = TOKEN,
        version = API_VERSION
    ))

    return response


def sendPhotoMessage(user_id, photo, message=None, reply_id=None):
    uploadLink = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "photos.getMessagesUploadServer",
        parameters = "peer_id={}".format(
            user_id
        ),
        token = TOKEN,
        version = 5.131
    ))

    image = open(f'{photo}', 'rb')
    uploadPhoto = requests.post(uploadLink.json()['response']['upload_url'], files={"photo": image})
    image.close()

    savePhoto = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "photos.saveMessagesPhoto",
        parameters = "photo={}&server={}&hash={}".format(
            uploadPhoto.json()['photo'],
            uploadPhoto.json()['server'],
            uploadPhoto.json()['hash']
        ),
        token = TOKEN,
        version = API_VERSION
    ))

    sendMessage = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&message={}&attachment={}&reply_to={}".format(
            user_id,
            int(time.time()),
            message,
            "photo{}_{}".format(
                savePhoto.json()['response'][0]['owner_id'],
                savePhoto.json()['response'][0]['id']
            ),
            reply_id
        ),
        token = TOKEN,
        version = API_VERSION
    ))

    return [uploadLink, uploadPhoto, savePhoto, sendMessage]

exit(0)
