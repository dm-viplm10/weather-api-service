from flask import request
from weather_api_service import app
from weather_api_service.models.User import auth_required
from weather_api_service.services.Utilities import Utilities

@app.route('/getcity', methods=['GET'])
@auth_required
def get_city(current_user):
    data, status, message = None, None, None
    try:
        payload = request.args
        country = payload['country']
        country_data = Utilities.ReadCountryFile()
        if country_data and country:  
            data, status, message = {'country': country, 'cities': country_data[country]}, 200, f'Successfully Listed cities for {country}'
        else:
            status, message = 500, 'Failed to List Cities: No country selected or data not available'

    except Exception as e:
        message, status = f'Exception has occured - {str(e)}', 500

    return  data, status, message


@app.route('/getcountry', methods=['GET'])
@auth_required
def get_country(current_user):
    data, status, message = None, None, None 
    try:             
        country_data = Utilities.ReadCountryFile()
        if country_data:
            data, status, message = {'countries':list(country_data.keys())}, 200, 'Successfully Listed countries'
        else:
            status, message =500, 'Failed to List Countries'
        
    except Exception as e:
        message, status = f'Exception has occured - {str(e)}', 500

    return  data, status, message