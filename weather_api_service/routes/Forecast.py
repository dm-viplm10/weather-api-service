import traceback
from flask import request, make_response
from weather_api_service import app, db, api_key, getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.models.Analytics import Audit as AuditActivity
from weather_api_service.models.User import User, auth_required 
import json, requests
from datetime import datetime


@app.route('/forecast', methods=['GET', 'POST'])
@auth_required
def Forecast(current_user):
    try:
        payload = request.json
        city: str = payload.get('city', None)
        days: int = payload.get('days', None)
        if current_user and city and isinstance(days, int):
            url = "http://api.weatherapi.com/v1/forecast.json?key={0}&q={1}&days={2}&aqi=no&alerts=no"
            response = requests.post(url=url.format(api_key, city, days))
            data=json.loads(response.text)
            if response.status_code == 200:
                audit = AuditActivity(datetime.now(), data['location']['country'], data['location']['name'], current_user, 'Successfully Fetched Forecast')
                db.session.add(audit)
                db.session.commit()
                resp = HttpResponse(data=data, status=response.status_code, message='Successfully Fetched Forecast')              
            else:                
                try:
                    resp = HttpResponse(data=data, status=response.status_code, message=data['error']['message'])
                    audit = AuditActivity(datetime.now(), '', '', current_user, data['error']['message'])
                    db.session.add(audit)
                    db.session.commit()
                except Exception as exc:
                    traceback.print_exc()
                    resp = HttpResponse(message='Exception Occured - Invalid API request', status=response.status_code)
                    audit = AuditActivity(datetime.now(), '', '', current_user, 'Exception Occured - '+str(e))
                    db.session.add(audit)
                    db.session.commit()
            
        else:
            resp = HttpResponse(message='Exception Occured - Invalid Login or input parameters', status=500)            

    except Exception as e:
        traceback.print_exc()
        exception_str = str(e)
        resp = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())
