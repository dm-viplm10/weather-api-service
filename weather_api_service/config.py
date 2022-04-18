import os


app_config_dict = {
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///weather_api_service.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}

secret_key = os.environ.get('secret_key', '9cecb32b381c4678b1b102419221304s')
api_key = "9cecb32b381c4678b1b102419221304"

