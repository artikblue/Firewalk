import decimal
import asyncio
import aiohttp
import functools
import json
import datetime
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from pandas import DataFrame, DatetimeIndex
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold



def force_async(fn):
    '''
    turns a sync function to async function using threads
    '''
    
    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)  # make it awaitable

    return wrapper


def get_numerical_data(d):
    dj = json.loads(d)
    cluster_data = []
    for v in dj:
        obj = {
            "price":int(v["price"]),
            "surface":int(v["surface"]),
            "rooms":int(v["rooms"]),
            "toilets":int(v["toilets"]),
            "feats":len(v["feats"]),
            "images":len(v["images"])
        }
        cluster_data.append(obj)

    df = DataFrame(cluster_data)
    return df
@force_async
def make_regression(d):
    df = get_numerical_data(d)
    model = LinearRegression()
    X = DataFrame(df["price"])
    y = DataFrame(df[["surface", "rooms", "toilets", "feats", "images"]])
    scores = []
    kfold = KFold(n_splits=3, shuffle=True, random_state=42)
    for i, (train, test) in enumerate(kfold.split(X, y)):
        model.fit(X.iloc[train,:], y.iloc[train,:])
        score = model.score(X.iloc[test,:], y.iloc[test,:])
        scores.append(score)

    regression_obj = {
        "coefs":model.coef_,
        "rank":model.rank_,
        "singular":model.singular_,
        "intercept":model.intercept_,
        "scores":scores
    }    

    return regression_obj

    #print(scores)

@force_async
def make_clusters(d, numclusters=6):
    
    df = get_numerical_data(d)

    kmeans = KMeans(n_clusters=numclusters).fit(df)
    centroids = kmeans.cluster_centers_
    list_categories = []
    for c in centroids:

        obj = {
            "price":int(c[0]),
            "surface":int(c[1]),
            "rooms":int(c[2]),
            "toilets":int(c[3]),
            "feats":int(c[4]),
            "images":int(c[5])
        }
        list_categories.append(obj)
    return list_categories

def make_zonemean(d, val):
    dj = json.loads(d)
    df = DataFrame(dj)
    zone_priceman = (df.groupby('zone').mean())

    return (zone_priceman[val].to_json())

def make_catcount(d, val="site"):
    dj = json.loads(d)
    df = DataFrame(dj)

    df['month'] = DatetimeIndex(df['parse_date']).month

    print(df.head())
    valcount = (df.groupby(val).size())
    
    return(valcount.to_json())

def make_timecount(d, val="month"):
    dj = json.loads(d)
    df = DataFrame(dj)

    if val == "month":
        df['month'] = DatetimeIndex(df['parse_date']).month
        valcount = (df.groupby("month").size())
    
    if val == "year":
        df['year'] = DatetimeIndex(df['parse_date']).year
        valcount = (df.groupby("year").size())

    if val == "day":
        df['day'] = DatetimeIndex(df['parse_date']).day
        valcount = (df.groupby("day").size())
    
    return(valcount.to_json())    

def make_cheap_zones(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    price_mean = df["price"].mean()
    dfc = df[df.price < price_mean]
    return dfc.to_json()

def make_expensive_zones(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    price_mean = df["price"].mean()
    dfc = df[df.price > price_mean]
    return dfc.to_json()

@force_async
def make_stats(d):
    df = get_numerical_data(d)

    price_mean = df["price"].mean()
    surface_mean = df["surface"].mean()
    rooms_mean = df["rooms"].mean()
    toilets_mean = df["toilets"].mean()
    feats_mean = df["feats"].mean()
    images_mean = df["images"].mean()

    price_max = df["price"].max()
    surface_max = df["surface"].max()
    rooms_max = df["rooms"].max()
    toilets_max = df["toilets"].max()
    feats_max = df["feats"].max()
    images_max = df["images"].max()


    price_min = df["price"].min()
    surface_min = df["surface"].min()
    rooms_min = df["rooms"].min()
    toilets_min = df["toilets"].min()
    feats_min = df["feats"].min()
    images_min = df["images"].min()

    price_sum = df["price"].sum()
    surface_sum = df["surface"].sum()
    rooms_sum = df["rooms"].sum()
    toilets_sum = df["toilets"].sum()
    feats_sum = df["feats"].sum()
    images_sum = df["images"].sum()

    price_std = df["price"].std()
    surface_std = df["surface"].std()
    rooms_std = df["rooms"].std()
    toilets_std = df["toilets"].std()
    feats_std = df["feats"].std()
    images_std = df["images"].std()

    offers_count = df["price"].count()



    general_stats_obj = {
        "price_mean":str(price_mean),
        "surface_mean":str(surface_mean),
        "rooms_mean":str(rooms_mean),
        "toilets_mean":str(toilets_mean),
        "images_mean":str(images_mean),
        "feats_mean":str(feats_mean),
        "price_max":str(price_max),
        "surface_max":str(surface_max),
        "rooms_max":str(rooms_max),
        "toilets_max":str(toilets_max),
        "feats_max":str(feats_max),
        "images_max":str(images_max),
        "price_min":str(price_min),
        "surface_min":str(surface_min),
        "rooms_min":str(rooms_min),
        "toilets_min":str(toilets_min),
        "feats_min":str(feats_min),
        "images_min":str(images_min),
        "price_sum":str(price_sum),
        "surface_sum":str(surface_sum),
        "rooms_sum":str(rooms_sum),
        "toilets_sum":str(toilets_sum),
        "feats_sum":str(feats_sum),
        "images_sum":str(images_sum),
        "price_std":str(price_std),
        "surface_std":str(surface_std),
        "rooms_std":str(rooms_std),
        "toilets_std":str(toilets_std),
        "feats_std":str(feats_std),
        "images_std":str(images_std),
        "offers_count":str(offers_count),
        "calc_date": str(datetime.datetime.now())
    }
    return general_stats_obj
    