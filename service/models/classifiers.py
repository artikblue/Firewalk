from mongoengine import *
#connect('')


class Classifier(Document):
    classifier_type = StringField(required=True)
    object_data = BinaryField(required=True)
    accuracy = FloatField(required=False)
    scores = ListField(required=False)
    feats = ListField(required=False)
    criterion = StringField(required=False)
    random_state = IntField(required=False)
    min_samples_split = IntField(required=False)
    max_depth=IntField(required=False)
    test_size = FloatField(required=False)
    categories = StringField(required=False)
