from distutils.command import upload
from tokens import TOKEN
from websites import *
import sys
import requests
import random
import time

messages = {
    "itemAdded": "Товар был успешно добавлен в список отслеживаемых.",
    "itemRemoved": "Товар был успешно удалён из списка отслеживаемых.",
    "itemList": "Список отслеживаемых товаров:",
    "nowAvailable": "Отслеживаемый вами товар появился в наличии."
}

sticker_ids = {
    "almond_cool": "53453",
    "almond_ok": "53446",
    "sonechka_you_died": "57164"
}

def sendTextMessage(user_id, message):
    response = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&message={}&dont_parse_links={}".format(
            user_id,
            int(time.time()),
            message,
            1
        ),
        token = TOKEN,
        version = 5.131
    ))

    return response

def sendStickerMessage(user_id, sticker_id):
    response = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&sticker_id={}".format(
            user_id,
            int(time.time()),
            sticker_id
        ),
        token = TOKEN,
        version = 5.131
    ))

    return response

def sendPhotoMessage(user_id, photo, message=""):
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
        version = 5.131
    ))

    sendMessage = requests.get("https://api.vk.com/method/{method}?{parameters}&access_token={token}&v={version}".format(
        method = "messages.send",
        parameters = "user_id={}&random_id={}&message={}&attachment={}".format(
            user_id,
            int(time.time()),
            message,
            "photo{}_{}".format(
                savePhoto.json()['response'][0]['owner_id'],
                savePhoto.json()['response'][0]['id']
            )
        ),
        token = TOKEN,
        version = 5.131
    ))

    return [uploadLink, uploadPhoto, savePhoto, sendMessage]
