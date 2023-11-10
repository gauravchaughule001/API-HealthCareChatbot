# run.py
from flask import Flask, request, jsonify
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController
from app.controllers.chat_controller import ChatController
from app.views.user_view import UserView
from app.views.auth_view import AuthView
from app.views.chat_view import ChatView
from flask_cors import CORS, cross_origin
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)

# Initialize controller and view
user_controller = UserController()
auth_controller = AuthController()
chat_controller = ChatController()
user_view = UserView(user_controller)
auth_view = AuthView(auth_controller)
chat_view = ChatView(chat_controller)


# Routes

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return auth_view.login(username, password)

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({'message':'Hello World Using Python Rest API !'}), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    return user_view.create_user(username, email, password)

def isTokenValid(request):
    return auth_view.verify_token(request.headers.get('Authorization'))

@app.route('/users', methods=['GET'])
def get_users():
    response = {}
    token_res = isTokenValid(request)
    if token_res['isTokenExpired'] == True:
        return {'message':'Unauthorized','data':'Access token expired'}, 401
    elif token_res['isTokenInvalid'] == True:
        return {'message':'Unauthorized','data':'Invalid access token'}, 401
    elif len(token_res['token'])>0:
        return user_view.get_users()
    else:
        return {'message':'Unable to process the request'}, 501

@app.route('/users', methods=['PUT'])
def update_user():
    user_id = request.args.get('user_id')
    data = request.get_json()
    return user_view.update_user(user_id, data.get('username'), data.get('email'))

@app.route('/users', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('user_id')
    user_deleted = user_view.delete_user(user_id)
    return user_deleted

@app.route('/chat', methods=['POST'])
def chat():
    return chat_view.chat(request)

@app.route('/chat', methods=['GET'])
def get_chats():
    number = request.args.get('number')
    return chat_view.get_chats(number)

if __name__ == '__main__':
    app.run(debug=True)
