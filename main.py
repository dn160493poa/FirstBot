from flask import Flask, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://dp160493poa:366619oleg@ds029675.mlab.com:29675/heroku_2hz4q0l0")
db = client.heroku_2hz4q0l0


@app.route("/")
def test():
    return "It work"


Obolon = {"Декабристов 3": "VIP only", "Дружбы народов 11": "Для всех"}
Podol = {}
Svyatoshinskiy = {}
Pecherskiy = {}
Dneprovskiy = {}
Poznyaku = {}
Kiev_info = "Киев: 32 отделения с ячейками"
Kiev_safes = {"Дружбы народов 2": "VIP", "народного ополчения 4":"VIP"}
inAll = (Kiev_safes)

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
        send(chat_id, Kiev_info)
        for dep in Kiev_safes:
            print(dep)

    return "OK"


