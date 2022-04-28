from flask import request
from weather_api_service import app
from weather_api_service.models.User import auth_required
from weather_api_service.services.Utilities import Utilities

@app.route('/topncity', methods=['GET'])
@auth_required

def get_topncity(current_user):
    return  Utilities.FindTopN('Cities', request.args)


@app.route('/topncountry', methods=['GET'])
@auth_required

def get_topncountry(current_user):
    return  Utilities.FindTopN('Countries', request.args)


@app.route('/topnuser', methods=['GET'])
@auth_required

def get_topnusers(current_user):
    return  Utilities.FindTopN('Users', request.args)