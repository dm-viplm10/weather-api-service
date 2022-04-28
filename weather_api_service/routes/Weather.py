from flask import request
from weather_api_service import app
from weather_api_service.models.User import auth_required 
from weather_api_service.services.WeatherAPI import WeatherApiService as wapi

@app.route('/forecast', methods=['GET', 'POST'])
@auth_required

def Forecast(current_user):
    return wapi.Forecast(wapi(current_user), request.json)