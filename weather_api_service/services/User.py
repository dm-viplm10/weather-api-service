from weather_api_service import db, secret_key, encrypt
from weather_api_service.models.User import User
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.services.Utilities import Utilities
from datetime import datetime
import jwt

def login_user(payload) -> HttpResponse:
    try:
        user_name: str = payload.get('user_name', None)
        password: str = payload.get('password', None)
        if user_name and password:
            status, message, data = validate_user_credentials(user_name=user_name, password=password)
            if status == 200:
                access_token = jwt.encode(payload=data, key=secret_key)
                data['access_token'] = access_token
        else:
            status, message, data = (400, 'Bad request', None)

        response = HttpResponse(message=message, status=status, data=data)
    except Exception as e:
        response = HttpResponse(message=f'Exception Occured - {str(e)}', status=500)
    
    return response

def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    status, message, user = 401, 'Incorrect username or password', None
    try:
        user_obj = (
            db.session.query(User)
            .filter(User.username == user_name)
            .first()
        )
        if user_obj:           
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            if entered_password_enc == user_obj.password:
                status, message = 200, 'User successfully authenticated'                      
                user = {
                    'user_name': user_obj.username, 'first_name': user_obj.full_name
                }
            else:
                message =  'Invalid Credentials'                
        else:   
            message = 'Invalid username or password'
            status = 500
                    
    except Exception as e:
        message = str(e)
        status = 500        

    Utilities.CommitAnalyticsDB(datetime.now(), '', '', user_obj, message)

    return status, message, user
        