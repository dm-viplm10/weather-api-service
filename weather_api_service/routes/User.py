from flask import request, make_response
from weather_api_service import app, db, secret_key, getResponseHeaders
import json
from weather_api_service.services import User as user_service


@app.route('/login', methods=['POST'])
def login():
    response = user_service.login_user(request.json)
    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())


