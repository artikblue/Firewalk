import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans

class Cluster(Document):

    price_mean = StringField(required=True)
    surface_mean = StringField(required=True)
    rooms_mean = StringField(required=True)
    toilets_mean = StringField(required=True)
    feats_mean = StringField(required=True)
    images_mean = StringField(required=True)

    price_max = StringField(required=True)
    surface_max = StringField(required=True)
    rooms_max = StringField(required=True)
    toilets_max = StringField(required=True)
    feats_max = StringField(required=True)
    images_max = StringField(required=True)

    price_min = StringField(required=True)
    surface_min = StringField(required=True)
    rooms_min = StringField(required=True)
    toilets_min = StringField(required=True)
    feats_min = StringField(required=True)
    images_min = StringField(required=True)

    price_sum = StringField(required=True)
    surface_sum = StringField(required=True)
    rooms_sum = StringField(required=True)
    toilets_sum = StringField(required=True)
    feats_sum = StringField(required=True)
    images_sum = StringField(required=True)

    price_std = StringField(required=True)
    surface_std = StringField(required=True)
    rooms_std = StringField(required=True)
    toilets_std = StringField(required=True)
    feats_std = StringField(required=True)
    images_std = StringField(required=True))

    offers_count = StringField(required=True)

    calc_date = StringField(required=True)