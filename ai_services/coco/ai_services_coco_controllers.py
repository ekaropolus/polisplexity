from flask import render_template, jsonify, request
import requests

def coco_ctr():
    return render_template('coco_index.html')