from flask import Blueprint, jsonify, current_app, request
from flask_login import login_manager, login_user, current_user, logout_user
from bson import json_util, ObjectId
from .models import User
import json  # Import the json module

users = Blueprint('users', __name__)

@users.route('/user/get/<user_id>/', methods=['GET'])
def get_user(user_id):
    try:
        user_doc = current_app.db.users.find_one({'_id': ObjectId(user_id)})
        if user_doc:
            # Parse the JSON string to a dictionary
            user_data = json.loads(json_util.dumps(user_doc))
            return jsonify(user_data), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@users.route('/login/', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already logged in'}), 200

    data = request.get_json()
    username = data.get('username')

    user_doc = current_app.db.users.find_one({'username': username})
    if user_doc:
        user = User(user_id=user_doc['_id'], username=user_doc['username'], roles=user_doc['roles'])
        login_user(user, remember=True)
        return jsonify({'message': 'Logged in successfully'}), 200

    return jsonify({'error': 'Invalid login credentials'}), 401

@users.route('/logout/', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

