from weather_api_service import db, secret_key, getResponseHeaders
import jwt, json
from flask import request, make_response
from functools import wraps
from weather_api_service.models.HttpResponse import HttpResponse

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def to_json(self):
        return dict(
            username=self.username,
            full_name=self.full_name
        )


def auth_required(func):
    @wraps(func)
    def authenticator():
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'] 
        else:
            resp = HttpResponse(message='Valid token is missing', status=500)
            return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            cur_user = User.query.filter_by(username=data['user_name']).first()      
        except:
            resp = HttpResponse(message='Invalid Token', status=500)
            return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())
        
        data, status, message = func(cur_user)
        resp = HttpResponse(data=data, status=status, message=message)
        return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())

    return authenticator