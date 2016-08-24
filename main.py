from flask import Flask, request
import requests
from pymongo import MongoClient
import telegram

app = Flask(__name__)

client = MongoClient("mongodb://dp160493poa:366619oleg@ds029675.mlab.com:29675/heroku_2hz4q0l0")
db = client.heroku_2hz4q0l0

bot = telegram.Bot("257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I")

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
        answer = ""
        for doc in db.products.find():
            answer += str(doc["products"]) + "\n"

        send(chat_id, answer)
    if command == "/Киев":
        for dep in db.safes.find():
            send(chat_id, dep)
    if command == "/go":
        bot.sendPhoto(chat_id, "url")

    return "OK"


