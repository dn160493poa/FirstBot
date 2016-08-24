from flask import Flask, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://dp160493poa:366619oleg@ds029675.mlab.com:29675/heroku_2hz4q0l0")
db = client.heroku_2hz4q0l0


@app.route("/")
def test():
    return "It work"


def send(chat_id, text):
    requests.post("https://api.telegram.org/bot257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I/sendMessage",
                  {
                      "chat_id": chat_id,
                      "text": text
                  })


@app.route("/hook", methods=["POST"])
def hook():
    chat_id = request.get_json()["message"]["chat"]["id"]
    text = request.get_json()["message"]["text"]

    command, *args = text.split()

    send(chat_id, "Я могу помочь найти ячейку!")
    send(chat_id, "Введи /город  с большой буквы, вот так: /Киев")

    if command == "/add":
        db.products.insert({"products": args})
        send(chat_id, "Products add")
    if command == "/get":
        answer = "\n".join(map(str, db.products.find()))

        send(chat_id, answer)
    if command == "/Киев":
        send(chat_id, "https://www.google.ru/maps/place/бульвар+Дружби+Народів,+4,+%D0%9A%D0%B8%D1%97%D0%B2,+%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0/@50.4116455,30.5284588,17z/data=!4m13!1m7!3m6!1s0x40d4cf3f53763da9:0xf6eca58db9696a8a!2z0LHRg9C70YzQstCw0YAg0JTRgNGD0LbQsdC4INCd0LDRgNC-0LTRltCyLCA0LCDQmtC40ZfQsiwg0KPQutGA0LDQuNC90LA!3b1!8m2!3d50.4116455!4d30.5306475!3m4!1s0x40d4cf3f53763da9:0xf6eca58db9696a8a!8m2!3d50.4116455!4d30.5306475")
        for dep in db.safes.find():
            send(chat_id, dep)

    return "OK"




