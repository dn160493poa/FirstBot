from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/")
def test():
    return "It work"


@app.route("/hook", methods=["POST"])
def hook():
    chat_id = request.get_json()["message"]["chat"]["id"]
    requests.post("https://api.telegram.org/bot257528811:AAHbKoS1oPEcq_IQkbQ8YB-VQyoRkYTX9rQ/sendMessage", {
            "chat_id": chat_id,
            "text": "Привет, Вам нужны ячейки?"
        })
    return "OK"
