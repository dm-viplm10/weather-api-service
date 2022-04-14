from flask import request, make_response
from weather_api_service import app, getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
import json
from weather_api_service.services import ReadCountryData as read_service

@app.route('/getcity', methods=['GET'])
def get_city():
    try:
        payload = request.args
        country = payload['country']
        data = read_service.ReadCountryFile()
        city_list = []
        if data and country:  
            city = {'country': country, 'cities': data[country]}
            resp = HttpResponse(data=city, status=200, message='Successfully Listed cities for {0}'.format(country))
        else:
            resp = HttpResponse(status=500, message='Failed to List Cities: No country selected or data not available')

    except Exception as e:
        resp = HttpResponse(message='Exception has occured - '+ str(e), status=500)

    return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())