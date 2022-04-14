from flask import request, make_response
from weather_api_service import app, getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.services.FindTopNElements import FindTopN
from weather_api_service.models.Analytics import Audit
import json

@app.route('/topncountry', methods=['GET'])
def get_topncountry():
    try:     
        payload = request.args
        rows = Audit.query.all()
        n: int = int(payload['n'])
        user_list, top_n_countries = [], {}
        if rows and n:
            for row in rows:
                if len(row.country) > 0:
                    user_list.append(row.country)

            top_n = FindTopN(user_list, n)
            for user, freq in top_n:
                top_n_countries[user] = freq

            resp = HttpResponse(data=top_n_countries, status=200, message='Successfully Listed Top {0} Countries'.format(n))
        else:
            resp = HttpResponse(status=500, message='Failed to List Top {0} Countries'.format(n))
        
    except Exception as e:
        resp = HttpResponse(message='Exception has occured - '+ str(e), status=500)

    return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())