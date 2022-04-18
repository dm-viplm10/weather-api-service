from flask import request, make_response
from weather_api_service import app, getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.models.User import auth_required
from weather_api_service.services import ReadCountryData as read_service
import json

@app.route('/getcountry', methods=['GET'])
@auth_required
def get_country(current_user):
    try:        
        data = read_service.ReadCountryFile()
        if data:
            country = {'countries':list(data.keys())}
            resp = HttpResponse(data=country, status=200, message='Successfully Listed countries')
        else:
            resp = HttpResponse(status=500, message='Failed to List Countries')
        
    except Exception as e:
        resp = HttpResponse(message='Exception has occured - '+ str(e), status=500)

    return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())