from urllib import response
from weather_api_service import db, secret_key, getResponseHeaders
import jwt, json
from flask import request, make_response
from functools import wraps
from weather_api_service.models.Analytics import Audit as AuditActivity
from weather_api_service.models.HttpResponse import HttpResponse
from datetime import datetime 

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
        if not token:
            resp = HttpResponse(message='Valid token is missing', status=500)
            return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            cur_user = User.query.filter_by(username=data['user_name']).first()
            audit = AuditActivity(datetime.now(), '', '', cur_user, 'User authentication successful')  
            db.session.add(audit)
            db.session.commit()
            print(f'{cur_user.username} authenticated')
        except:
            resp = HttpResponse(message='Invalid Token', status=500)
            return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())
 
        return func(cur_user)
    return authenticator