import decimal
import asyncio
import aiohttp
import functools
import json
import datetime
import numpy as np
from sklearn import decomposition
from concurrent.futures import ThreadPoolExecutor
from pandas import DataFrame, DatetimeIndex
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import pickle
import googlemaps

from sklearn.preprocessing import StandardScaler


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


def get_numerical_data(d, vals=['price','surface','rooms','toilets','feats','images']):
    dj = json.loads(d)
    df = DataFrame(dj)
    df = df[vals]
    if "feats" in vals:
        df["feats"]=df["feats"].apply(lambda x: len(x))
    if "images" in vals:
        df["images"]=df["images"].apply(lambda x: len(x))
    return df
@force_async
def make_geopoints(d):
    d = json.loads(d)
    gmaps = googlemaps.Client(key='XXX')

    located_offers = []
    for val in d:
        address=val["address"]
        lat, lng = gmaps.address_to_latlng(address)

        geo_object = {
            "geo":[lat, lng],
            "url":val["url"],
            "address":val["address"],
            "price":val["price"],
            "space":val["surface"],
            "rooms":val["rooms"]
        }
        located_offers.append(geo_object)

    return located_offers

def map_pricelabel(data,labels):
    price = int(data["price"])

    for k in labels.keys():
        minprice = int(k)
        if price >= minprice:
            if price <= int(labels[k]["maxval"]):
                return(labels[k]["tag"])

def encode_target(df, target_column, newcolumn):

    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod[newcolumn] = df_mod[target_column].replace(map_to_int)

    return (df_mod, targets)


@force_async
def make_dtree(d,c):
    data = json.loads(d)
    df = DataFrame(data)
    
    prices_category = make_categories(c)

    df['price_label'] = df.apply (lambda row: map_pricelabel(row,prices_category), axis=1)
    df['num_photos'] = df.apply (lambda row: len(row["images"]), axis=1)
    df['num_feats'] = df.apply (lambda row: len(row["feats"]), axis=1)
    df2, sites = encode_target(df, "site", "site_num")
    df2, cities = encode_target(df2, "city", "city_num")
    df2, zones = encode_target(df2, "zone", "zone_num")
    df2, companies = encode_target(df2, "company", "company_num")
    df2, labels = encode_target(df2, "price_label", "label_num")

    df2=df2.drop(columns=['price','site','city','zone','company','address','url','name','parse_date','price_label','feats','images'])

    y = df2["label_num"]
    X = df2[["num_photos","num_feats","site_num","city_num","zone_num","company_num","surface","rooms","toilets"]]
    dt = DecisionTreeClassifier(min_samples_split=20, random_state=99, criterion="gini", max_depth=4)
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1) # 60% training and 40% test
    dt = dt.fit(X_train,y_train)
    y_pred = dt.predict(X_test)
    scores = cross_val_score(dt, X, y, cv=5)

    sdt = pickle.dumps(dt)
    tree_obj = {
        'accuracy':metrics.accuracy_score(y_test, y_pred),
        'crossvalscores':scores.tolist()
    }
    return tree_obj,sdt

@force_async
def make_regression(d, n_splits=3, random_state=42, val="price",feats=["surface", "rooms", "toilets", "feats", "images"]):
    feats.append(val)  
    df = get_numerical_data(d, vals=feats)
    model = LinearRegression()
    X = DataFrame(df[val])
    y = DataFrame(df[feats])
    scores = []
    kfold = KFold(n_splits=3, shuffle=True, random_state=42)
    for i, (train, test) in enumerate(kfold.split(X, y)):
        model.fit(X.iloc[train,:], y.iloc[train,:])
        score = model.score(X.iloc[test,:], y.iloc[test,:])
        scores.append(score)

    regression_obj = {
        "coefs":model.coef_.tolist(),
        "rank":model.rank_,
        "singular":model.singular_.tolist(),
        "intercept":model.intercept_.tolist(),
        "scores":scores
    }    

    return regression_obj


@force_async
def make_clusters(d, numclusters=6, numpca=3, vals=['price','surface','rooms','toilets','feats','images'], algorithm="elkan"):
    if numpca >= len(vals):
        numpca=3
        numclusters=6
        vals=['price','surface','rooms','toilets','feats','images']
        

    scal = StandardScaler()
    df = get_numerical_data(d, vals=vals)
    print(df)
    df = scal.fit_transform(df)
    pca = decomposition.PCA(n_components=numpca)
    pca.fit(df)
    df = pca.transform(df)

    kmeans = KMeans(n_clusters=numclusters, algorithm=algorithm).fit(df)
    centroids =  scal.inverse_transform(pca.inverse_transform(kmeans.cluster_centers_))

    
    
    return centroids.tolist()

def make_categories(c):
    clusters = json.loads(c)
    prices = []
    #extract prices
    print(clusters)
    for c in clusters[0]["clusters"]:
        prices.append(c[0])
    
    prices.sort()
    prices_category = {}
    midval = len(prices) / 2
    
    for count in range(0,len(prices)-1):
        actualprice = prices[count]

        if count == 0:
            minval = 0
            nv = prices[count+1]
            maxval = (actualprice+nv) / 2

        elif count == len(prices)-1:
            maxval = 1000000
            prev = prices[count-1]
            minval = ((actualprice+prev) / 2 )+1
        else:
            nv = prices[count+1]
            prev = prices[count-1]
            maxval = (actualprice+nv) / 2
            minval = ((actualprice+prev) / 2 )+1

        if count < midval:
            tag = "CHEAP-"+str(count)
        else:
            tag = "EXPENSIVE-"+str(count)


        prices_category[minval] = {
            "minval":minval,
            "maxval":maxval,
            "tag":tag,
            "centroid":prices[count]
        }
        count = count +1
    return prices_category

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

def make_companychart(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    df = DataFrame({'Percentage': df.groupby([ 'company']).size() / len(df)})
    #return(valcount.to_json())    
    return df.to_json()

def make_sitechart(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    print(df.head())
    df = DataFrame({'Percentage': df.groupby([ 'site']).size() / len(df)})
    print(df.head())
    #return(valcount.to_json())    
    return df.to_json()

def make_cheap_zones(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    price_mean = df["price"].mean()
    dfc = df[df.price < price_mean]
    dfc = dfc.groupby('zone')['price'].mean()
    return dfc.to_json()

def make_expensive_zones(d):
    dj = json.loads(d)
    df = DataFrame(dj)
    price_mean = df["price"].mean()
    dfc = df[df.price > price_mean]
    dfc = dfc.groupby('zone')['price'].mean()
    return dfc.to_json()

@force_async
def make_stats(d):
    df = get_numerical_data(d)

    price_mean = df["price"].mean()
    price_mode = df["price"].mode()
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
        "price_mode":str(price_mode),
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
    