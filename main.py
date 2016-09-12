from flask import Flask, request
import requests
from pymongo import MongoClient
import telegram

KEY = "257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I"

app = Flask(__name__)

client = MongoClient("mongodb://dp160493poa:366619oleg@ds029675.mlab.com:29675/heroku_2hz4q0l0")
db = client.heroku_2hz4q0l0

bot = telegram.Bot(KEY)


@app.route("/")
def test():
    return "It work"


def send(chat_id, text):
    requests.post("https://api.telegram.org/bot257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I/sendMessage",
                  {
                      "chat_id": chat_id,
                      "text": text
                  })


def Marker(label, lat, lng, color="red"):
    return "&markers=size:mid|label:{label}|{lat},{lng}|color={color}".format(
        label=label,
        lat=lat,
        lng=lng,
        color=color
    )


def map(lat=0.0, lng=0.0, zoom=13, size=100):
    url = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size={size}x{size}&key=AIzaSyBEbX-HI26eD3euneOEXXphg4xT950UjC0".format(lat=lat, lng=lng, size=size, zoom=zoom)
    return url


def send_photo(chat_id, url):
    requests.post("https://api.telegram.org/bot{key}/sendPhoto".format(key=KEY), json={
                      "chat_id": chat_id,
                      "photo": url
                  })


@app.route("/hook", methods=["POST"])
def hook():
    chat_id = request.get_json()["message"]["chat"]["id"]
    text = request.get_json()["message"]["text"]

    command, *args = text.split()

    send(chat_id, "Напишите команду")
    send(chat_id, "Командой пока что может быть название населенного пункта")

    for safe in db.safes.find(
            {"$or": [
                {"город": command},
                {"страна": command},
                {"область": command},
                {"улица": command},
                {"район": command}
            ]}
    ):
        send(chat_id, "(" + safe["тип"] + " " + "клиентов" + ")" + " " + safe["улица"] + " " + "бранч:" + " " + safe["бранч"])

    if command == "map":
        url = map(50.4116, 30.5284588, 14, 300, markers=[
            Marker("C", 50.4116, 30.5284588),
            Marker("A", 50.4117, 30.5284688, "green"),
        ])
        bot.sendPhoto(chat_id, url)

    if command == "/Киев":
        send(chat_id, "https://www.google.ru/maps/place/бульвар+Дружби+Народів,+4,+%D0%9A%D0%B8%D1%97%D0%B2,+%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0/@50.4116455,30.5284588,17z/data=!4m13!1m7!3m6!1s0x40d4cf3f53763da9:0xf6eca58db9696a8a!2z0LHRg9C70YzQstCw0YAg0JTRgNGD0LbQsdC4INCd0LDRgNC-0LTRltCyLCA0LCDQmtC40ZfQsiwg0KPQutGA0LDQuNC90LA!3b1!8m2!3d50.4116455!4d30.5306475!3m4!1s0x40d4cf3f53763da9:0xf6eca58db9696a8a!8m2!3d50.4116455!4d30.5306475")

    return "OK"




