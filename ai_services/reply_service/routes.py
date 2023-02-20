from flask import Flask
import requests

reply_service = Flask(__name__)

@reply_service.route('/reply_service/', methods=['GET'])
def reply_service_route():
    req = requests.get('https://api.reply.io/v1/people')
    print(req.content)
    return 'hello'