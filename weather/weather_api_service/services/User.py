from weather_api_service import db, secret_key, encrypt
from weather_api_service.models.User import User
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.models.Analytics import Audit as AuditActivity
from datetime import datetime
import jwt

def login_user(payload) -> HttpResponse:
    try:
        #print(payload)
        user_name: str = payload.get('user_name', None)
        password: str = payload.get('password', None)
        print(user_name, password)    
        if user_name and password:
            status, message, data = validate_user_credentials(user_name=user_name, password=password)
            if status == 200:
                access_token = jwt.encode(payload=data, key=secret_key)
                data['access_token'] = access_token
        else:
            status, message, data = (400, 'Bad request', None)

        response = HttpResponse(message=message, status=status, data=data)
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return response

def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    status = 401
    print(secret_key)
    message = 'Incorrect username or password'
    user = None
    try:
        user_obj = (
            db.session.query(User)
            .filter(User.username == user_name)
            .first()
        )
        if user_obj:
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            print(entered_password_enc, user_obj.password)
            if entered_password_enc == user_obj.password:
                status = 200
                audit = AuditActivity(datetime.now(), '', '', user_obj, 'User login successful')  
                db.session.add(audit)
                db.session.commit()              
                message = 'User successfully authenticated'
                user = {
                    'user_name': user_obj.username, 'first_name': user_obj.full_name
                }
            else:
                audit = AuditActivity(datetime.now(), '', '', user_obj, 'Invalid Credentials')
                db.session.add(audit)
                db.session.commit()
        else:   
            message = 'Invalid username or password'
            audit = AuditActivity(datetime.now(), '', '', user_obj, message)    
            status = 500
            db.session.add(audit)
            db.session.commit()
        
    except Exception as e:
        message = str(e)
        status = 500
        audit = AuditActivity(datetime.now(), '', '', user_obj, message)
        db.session.add(audit)
        db.session.commit()

    return status, message, user
