from flask import Flask, request, jsonify, send_from_directory
# from flask_sslify import SSLify
import requests
# from apiai import ApiAI
import json
# import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# import vk
import random
from config import *



from game import root, session, tele_send_message, tele_send_photo
# import logging

app = Flask(__name__,  static_url_path='')





@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)

@app.route('/set_wh', methods=['POST', 'GET'])
def tele_set_wh():
    print("Setting: wh")
    url = URL + "setWebhook?url=" + WH_URL
    print(url)
    r = requests.get(url)
    return str(r.json())

@app.route('/get_wh', methods=['POST', 'GET'])
def tele_get_wh_info():
    print("Getting: wh")
    url = URL + "getWebhookInfo"
    print(url)
    r = requests.get(url)
    return str(r.json())





@app.route('/del_wh', methods=['POST', 'GET'])
def tele_del_wh():
    r = requests.get(URL + "deleteWebhook")
    return str(r.json())


@app.route('/url', methods=['POST', 'GET'])
def url_():
    print("URL pressed")
    return "!", 200

@app.route('/callback', methods=['POST', 'GET'])
def callback_():
    print("callback pressed")
    return "!", 200


# --------------------------------------------------------- ADMIN ---------------------------------------------
@app.route('/', methods=['POST', 'GET'])
def index():
    print("ok_here")
    if request.method=='POST':
        r = request.get_json()

        chat_id = None
        message = None
        callback_data = {}

        if "callback_query" in r:
            chat_id = r["callback_query"]["message"]["chat"]["id"]
            callback_data = json.loads(r["callback_query"]["data"])
            message = "/callback"

        if "message" in r:
            chat_id = r["message"]["chat"]["id"] # в какой чат
            message = r["message"]["text"]       # сообщение пользователя

        if chat_id not in session or message=="/restart":
            session[chat_id] = {"loc": "start", "inv": {}, "room_seen": ""}
        
        if not session[chat_id]["loc"]:
            session[chat_id]["loc"] = "start"

        if message:
            if message == "/callback":
                session[chat_id]["loc"] = callback_data["loc"]
            
            root(session[chat_id]["loc"], chat_id, message)
    
    return '!',200

@app.route('/off', methods=['POST', 'GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if CFG_LOCAL:
        app.run(host="0.0.0.0", port="5000", debug=True)
    else:        
        app.run(host="0.0.0.0", port=PORT, debug=True, ssl_context=CONTEXT)