from flask import Flask, request
import requests
from pymongo import MongoClient
import telegram

app = Flask(__name__)
KEY = "257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I"


client = MongoClient("mongodb://dp160493poa:366619oleg@ds029675.mlab.com:29675/heroku_2hz4q0l0")
db = client.heroku_2hz4q0l0

bot = telegram.Bot(KEY)


@app.route("/")
def test():
    return "It work"


def send(chat_id, text):
    requests.post("https://api.telegram.org/bot{key}/sendMessage".format(key=KEY),
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


def map(lat=0.0, lng=0.0, zoom=13, size=100, markers=[]):
    url = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size={size}x{size}&key=AIzaSyBEbX-HI26eD3euneOEXXphg4xT950UjC0".format(lat=lat, lng=lng, size=size, zoom=zoom)

    for marker in markers:
        url += marker

    return url


def send_photo(chat_id, url):
    r = requests.post("https://api.telegram.org/bot{key}/sendPhoto".format(key=KEY), json={
        "chat_id": chat_id,
        "photo": url
    })
    print(r)


@app.route("/hook", methods=["POST"])
def hook():
    chat_id = request.get_json()["message"]["chat"]["id"]
    text = request.get_json()["message"].get("text")
    location = request.get_json()["message"].get("location")


    command, *args = text.split()

    send(chat_id, "Напишите команду")
    send(chat_id, "Командой пока что может быть название населенного пункта")

    if text:
        command, *args = text.split()

        if command == "/add":
            db.products.insert({"products": args})
            send(chat_id, "Products added.")

        if command == "/get":
            answer = "\n".join(
                map(str, db.products.find())
            )
            send(chat_id, answer)

        if command == "map":
            url = map(50.4116, 30.5284588, 14, 300, markers=[
                Marker("C", 50.4116, 30.5284588),
                Marker("A", 50.4117, 30.5284688, "green"),
            ])
            bot.sendPhoto(chat_id, url)

    if location:
        send(chat_id, "{}, {}".format(location["longitude"], location["latitude"]))
    return "OK"



