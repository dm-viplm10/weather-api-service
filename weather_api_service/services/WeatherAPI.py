import requests, json
from weather_api_service import api_key
from weather_api_service.services.Utilities import Utilities
from datetime import datetime

class WeatherApiService:
    def __init__(self, current_user) -> None:
        self.data = None
        self.status = None
        self.message =None
        self.current_user = current_user

    def Forecast(self, payload):        
        try:
            city : str = payload.get('city', None)
            days : int = payload.get('days', None)
            if self.current_user and city and isinstance(days, int):
                url = "http://api.weatherapi.com/v1/forecast.json?key={0}&q={1}&days={2}&aqi=no&alerts=no"
                response = requests.post(url=url.format(api_key, city, days))
                data=json.loads(response.text)
                if response.status_code == 200:
                    country, city_db = data['location']['country'], data['location']['name']                   
                    self.data, self.status, self.message = data, response.status_code, 'Successfully Fetched Forecast'         
                else:   
                    country, city_db = '', ''             
                    try:
                        self.data, self.status, self.message = data, response.status_code, data['error']['message']                     
                    except:
                        self.message, self.status = 'Exception Occured - Invalid API request', response.status_code   

                Utilities.CommitAnalyticsDB(datetime.now(), country, city_db, self.current_user, self.message)                
            else:
                self.status=500
                self.message='Exception Occured - Invalid Login or input parameters'
        
        except Exception as e:
            self.message=f'Exception Occured - {str(e)}'
            self.status=500

        return self.data, self.status, self.message