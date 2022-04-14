from weather_api_service import db
from datetime import datetime


class Audit(db.Model):
    __tablename__ = 'analytics'
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    username = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)

    def __init__(self, timestamp, country, city, user, message):
        self.timestamp = timestamp
        self.country = country
        self.city = city
        self.message=message
        self.full_name = user.full_name
        self.username = user.username

    
