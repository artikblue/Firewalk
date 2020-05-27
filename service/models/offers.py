from mongoengine import *
#connect('')


class Offer(Document):
    site = StringField(required=True)
    city = StringField(required=True)
    zone = StringField(required=True)
    url = StringField(required=True) 
    name = StringField(required=True)
    address = StringField(required=True)
    toilets = IntField(required=True)
    rooms = IntField(required=True)
    surface = FloatField(required=True)
    images = ListField(required=True)
    price = FloatField(required=True)
    company = StringField(required=True)
    feats = ListField(required=True)
    parse_date = StringField(required=True)
    geo_coords = StringField(required=False)