from mongoengine import *
#connect('')


class Cluster(Document):
    price = IntField(required=True)
    surface = IntField(required=False)
    rooms = IntField(required=False)
    toilets = IntField(required=False)
    feats = IntField(required=False)
    images = IntField(required=False)
