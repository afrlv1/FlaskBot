from flask import Flask, request
import requests
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')
access_key = os.getenv('access_key')

app = Flask(__name__)

def get_weather():
    params = {"access_key": access_key, "query": "Moscow"}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    return f"Сейчас в Москве {api_response['current']['temperature']}

def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]
        weather = get_weather()
        send_message(chat_id, weather)
    return {"ok": True}
