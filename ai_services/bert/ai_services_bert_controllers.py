import time
import requests
from requests.exceptions import RequestException
from flask import request, render_template


def bert_controller():
    return render_template('bert_index.html')