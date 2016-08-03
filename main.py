from flask import Flask, request
import requests
from pymongo import MongoClient

app = Flask(__name__)


@app.route("/")
def test():
    return "It work"


@app.route("/hook", methods=["POST"])
def hook():
    chat_id = request.get_json()["message"]["chat"]["id"]
    requests.post("https://api.telegram.org/bot257528811:AAE1olpVb7hpblrHVr_fgRhAaloOtJ8oT4I/sendMassage",
                {
                    "chat_id": chat_id,
                    "text": "hi!"
                })
    return "OK"
