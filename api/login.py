from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from model.gamers import getUser

# Blueprints allow this code to be procedurally abstracted from main.py, meaning code is not all in one place
login_api = Blueprint('login_api', __name__, url_prefix='/api/login')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(login_api)

# Add CORS support to the NameAPI blueprint
def after_request(response):
    # Add the 'Access-Control-Allow-Origin' and 'Access-Control-Allow-Headers' headers to the response
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

class Login(Resource):
    def post(self):
        body = request.get_json(force=True)
        name = body.get('name')
        if name is None or len(name) < 2:
            return {'message': f'name is missing'}
        password = body.get('password')
        user = getUser(name)

        if user is None:
            return {'message': f"invalid username"}

        isPass = user.is_password(password)

        if not isPass:
            return {'message': f"wrong password"}
        
        response = jsonify(user.read())
        return response

api.add_resource(Login, '/')