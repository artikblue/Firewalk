from mongoengine import *
#connect('')


class Regression(Document):
    coefs = FloatField(required=True)
    rank = FloatField(required=True)
    singular = FloatField(required=False)
    intercept = FloatField(required=False)
    scores = FloatField(required=False)


