from mongoengine import *
#connect('')


class Classifier(Document):
    classifier_type = StringField(required=True)
    object_data = BinaryField(required=True)
    accuracy = FloatField(required=False)
    scores = ListField(required=False)
    