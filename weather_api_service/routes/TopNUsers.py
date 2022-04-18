from flask import request, make_response
from weather_api_service import app, getResponseHeaders
from weather_api_service.models.HttpResponse import HttpResponse
from weather_api_service.models.User import auth_required
from weather_api_service.services.FindTopNElements import FindTopN
from weather_api_service.models.Analytics import Audit
import json

@app.route('/topnusers', methods=['GET'])
@auth_required
def get_topnusers(current_user):
    try:     
        payload = request.args
        rows = Audit.query.all()
        n: int = int(payload['n'])
        user_list, top_n_users = [], {}
        if rows and n:
            for row in rows:
                user_list.append(row.username)

            top_n = FindTopN(user_list, n)
            for user, freq in top_n:
                top_n_users[user] = freq

            resp = HttpResponse(data=top_n_users, status=200, message='Successfully Listed Top {0} Users'.format(n))
        else:
            resp = HttpResponse(status=500, message='Failed to List Top {0} Users'.format(n))
        
    except Exception as e:
        resp = HttpResponse(message='Exception has occured - '+ str(e), status=500)

    return make_response(json.dumps(resp.__dict__), resp.status, getResponseHeaders())