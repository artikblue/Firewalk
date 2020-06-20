from mongoengine import *
#connect('')


class Cluster(Document):
    tags = ListField(required=True)
    clusters = ListField(required=False)
    numpca = IntField(required=False)
    algorithm = StringField(required=False)