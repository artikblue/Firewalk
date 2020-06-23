import quart
from quart import jsonify
import pickle
from services import fireservice
import asyncio
blueprint = quart.blueprints.Blueprint(__name__, __name__)
import json
from quart import request

from models import offers, clusters, generalstats, regressions, classifiers



## GENERAL DATA
# CITIES
@blueprint.route('/cities/', methods=['GET'])
async def cities():
    query = offers.Offer.objects().distinct(field="city")
    print(query)
    o = jsonify(query)
    return o



# ALL FROM 1 CITY
@blueprint.route('/city/<c>', methods=['GET'])
async def city(c: str):
    query = offers.Offer.objects(city=c).limit(5)
    o = query.to_json()
    return jsonify(o)

# COMPANIES
@blueprint.route('/companies/', methods=['GET'])
async def companies():
    query = offers.Offer.objects().distinct(field="company")
    print(query)
    o = jsonify(query)
    return o

# ALL FROM 1 COMPANY
@blueprint.route('/company/<c>', methods=['GET'])
async def company(c: str):
    query = offers.Offer.objects(company=c).limit(5)
    o = query.to_json()
    return jsonify(o)

# SITES
@blueprint.route('/sites/', methods=['GET'])
async def sites():
    query = offers.Offer.objects().distinct(field="site")

    o = jsonify(query)
    return o

# ALL FROM 1 SITE
@blueprint.route('/city/<s>', methods=['GET'])
async def site(s: str):
    query = offers.Offer.objects(city=c).limit(5)
    o = query.to_json()
    return jsonify(o)


# SEARCH FOR A PARTICULAR OFFER
@blueprint.route('/search/<s>', methods=['GET'])
async def search(s: str):
    citty = str(s)
    reg = "/.*"+citty+".*/"
    reg = {"$regex": citty}
    query = offers.Offer.objects.filter(name=reg).first()
    if query:

        o = query.to_json()
        return jsonify(o)
    else:
        return "{'result':'none'}"

# offers between price and price, surface and surface
# ALL FROM 1 SITE
@blueprint.route('/offers/price/range', methods=['POST'])
async def pricerange(s: str):
    a = int(request.form['min'])
    b = int(request.form['max'])
    query = offers.Offer.objects.filter(price >= min and price <= max).first()

    if query:

        o = query.to_json()
        return jsonify(o)
    else:
        return "{'result':'none'}"

# offers between price and price, surface and surface
# ALL FROM 1 SITE
@blueprint.route('/offers/surface/range', methods=['POST'])
async def surfacerange(s: str):
    a = int(request.form['min'])
    b = int(request.form['max'])
    query = offers.Offer.objects.filter(surface >= min and surface <= max).first()

    if query:

        o = query.to_json()
        return jsonify(o)
    else:
        return "{'result':'none'}"


# COUNT TOTAL NUMBER OF OFFERS
@blueprint.route('/offers/count', methods=['GET'])
async def offercount():
    query = offers.Offer.objects.all().count()
    return jsonify(query)

# COUNT TOTAL NUMBER OF OFFERS PER CITY
@blueprint.route('/city/count/<c>', methods=['GET'])
async def citiescount(c: str):
    query = offers.Offer.objects(city=c).count()
    return jsonify(query)


# RETURN A LIST {MONTHS, COUNT} OFFERS/MONTH
@blueprint.route('/offerchart/<cat>', methods=['GET'])
async def offerchart(cat :str):
    query = offers.Offer.objects().limit(1000)
    o = query.to_json()
    v =  fireservice.make_timecount(o,"day")
    return jsonify(v)

# RETURN A LIST {MONTHS, COUNT} OFFERS/MONTH
@blueprint.route('/companieschart/', methods=['GET'])
async def companieschart():
    import json
    query = offers.Offer.objects().limit(1000)
    o = query.to_json()
    v =  fireservice.make_companychart(o)
    v = json.loads(v)
    v = v["Percentage"]
    return v

# RETURN A LIST {MONTHS, COUNT} OFFERS/MONTH
@blueprint.route('/siteschart/', methods=['GET'])
async def siteschart():
    import json
    query = offers.Offer.objects().limit(5000)
    o = query.to_json()
    v =  fireservice.make_sitechart(o)
    v = json.loads(v)
    v = v["Percentage"]
    return v

# RETURN A LIST SITE:COUNT (SITE, NUMBER---) CATEGORY/UNITS
@blueprint.route('/sitescount', methods=['GET'])
async def sitescounterI():
    query = offers.Offer.objects().limit(1000)
    o = query.to_json()
    v =  fireservice.make_catcount(o,"site")
    return jsonify(v)

# LIST ALL DATA RELATED TO ONE OFFER, FILTER BY NAME
@blueprint.route('/offerdetails/<o>', methods=['GET'])
async def offerdetails(o: str):
    i = str(o) # 5e7a7baeb3ebdb96a6f17fd7
    query = offers.Offer.objects().distinct(_id=i)
    print(query)
    return jsonify(query)



## STATISTICAL / DATA MANAGEMENT

# GET ALL CLUSTER DATA
@blueprint.route('/getclusters', methods=['GET'])
async def getclusters():
    query = clusters.Cluster.objects()
    o = query.to_json()
    return jsonify(o)

# RUN CLUSTER ANALYSIS WHERE N I S THE NUMBER OF CLUSTER -> RESULT GOES TO RRESULTS DB
@blueprint.route('/runcluster/', methods=['POST'])
async def runcluster():
    data = await request.form
    
    query = offers.Offer.objects.all().limit(1000)
    o = query.to_json()
    numclusters = data['numclusters']
    numpca = data['numpca']
    algorithm = data['algorithm']
    vals = data.getlist('vals')
    a = await fireservice.make_clusters(o, numclusters=int(numclusters), numpca=int(numpca), vals=vals, algorithm=algorithm)
    
    clusters.Cluster(tags=vals, clusters=a, algorithm=algorithm, numpca=numpca).save()
    res = {"tags":vals, "clusters":a}
    return jsonify(res)

# GET GENERAL STATS
@blueprint.route('/generalstats', methods=['GET'])
async def getgeneralstats():
    query = offers.Offer.objects().all()
    o = query.to_json()
    v = await fireservice.make_stats(o)

    generalstats.Stats(
            price_mean = v["price_mean"],
            price_mode = v["price_mode"],
            surface_mean = v["surface_mean"],
            rooms_mean = v["rooms_mean"],
            toilets_mean = v["toilets_mean"],
            feats_mean = v["feats_mean"],
            images_mean = v["images_mean"],
            price_max = v["price_max"],
            surface_max = v["surface_max"],
            rooms_max = v["rooms_max"],
            toilets_max = v["toilets_max"],
            feats_max = v["feats_max"],
            images_max = v["images_max"],
            price_min = v["price_min"],
            surface_min = v["surface_min"],
            rooms_min = v["rooms_min"],
            toilets_min = v["toilets_min"],
            feats_min = v["feats_min"],
            images_min = v["images_min"],
            price_sum = v["price_sum"],
            surface_sum = v["surface_sum"],
            rooms_sum = v["rooms_sum"],
            toilets_sum = v["toilets_sum"],
            feats_sum = v["feats_sum"],
            images_sum = v["images_sum"],
            price_std = v["price_std"],
            surface_std = v["surface_std"],
            rooms_std = v["rooms_std"],
            toilets_std = v["toilets_std"],
            feats_std = v["feats_std"],
            images_std = v["images_std"],
            offers_count = v["offers_count"],
            calc_date = v["calc_date"]
    ).save()
    return jsonify(v)

# GET GEO POINTS RETURNS -> NAME, GEOCOORDS, ROOMS, SURFACE, TOILETS, PRICE, URL | {CITY, NUMBER OF REGISTERS}}
@blueprint.route('/getgeopoints/', methods=['GET'])
async def getgeopoints():
    query = offers.Offer.objects().limit(1000)
    o = query.to_json()
    v = await fireservice.make_geopoints(o)
    return jsonify(v)

# GENERATE, TRAIN AND EVALUATE A DECISSIONTREE CLASSIFIER FOR OFFERS
@blueprint.route('/genclassifier', methods=['POST'])
async def genclassifier():
    data = await request.form 
    querygeneral = offers.Offer.objects().all()
    queryclusters = clusters.Cluster.objects()

    feats = data.getlist('feats')
    criterion = data["criterion"]
    random_state = int(data["random_state"])
    min_samples_split = int(data["min_samples_split"])
    max_depth = int(data["max_depth"])
    test_size = float(data["test_size"])

    v, sdt = await fireservice.make_dtree(querygeneral.to_json(), queryclusters.to_json(), feats=feats, criterion=criterion, 
                                            random_state=random_state, min_samples_split=min_samples_split, max_depth=max_depth, test_size=test_size)
    
    classifiers.Classifier(
        classifier_type = "decissiontree",
        object_data = sdt,
        accuracy = v["accuracy"],
        scores = v["crossvalscores"],
        categories = json.dumps(v["prices_category"])
    ).save()

    return jsonify(v)

# GET CLASSIFFIERS
@blueprint.route('/getclassifiers', methods=['GET'])
async def getclassifiers():
    query = classifiers.Classifier.objects().first()
    o = query.to_json()
    
    
    return (o)

# MAP CATEGORY INTO NUM
@blueprint.route('/mapvalue', methods=['POST'])
async def mapvalue():
    data = await request.form
    query = offers.Offer.objects().all()
    o = query.to_json()
    val = data["val"]
    category = data["category"]

    num_val = fireservice.map_encode(o, val, category)
    
    res_num = {
        "category_num":num_val
    }
    return jsonify(res_num)

# CLASSIFY AN OFFER INTO A PRICE RANGE
@blueprint.route('/classify', methods=['POST'])
async def classify():
    data = await request.form
    query = classifiers.Classifier.objects().first()
    feats = data.getlist('feats')
    feats = [feats]
    o = query["object_data"]

    v = fireservice.classify(o, feats)

    ret_obj = {
        "category":v.tolist(),
        "query":json.loads(query["categories"])
    }
    return jsonify(ret_obj)
# GET CATEGORIES FOR OFFERS
@blueprint.route('/categories', methods=['GET'])
async def getcategories():
    queryclusters = clusters.Cluster.objects()
    v = fireservice.make_categories(queryclusters.to_json())

    return jsonify(v)
# GET LIST OF CHEAPEST ZONES N IS THE MAX NUMBER, RETURN ZONE , AVG PRICE
@blueprint.route('/cheapestzones', methods=['GET'])
async def cheapestzones():
    query = offers.Offer.objects().all()
    o = query.to_json()
    v =  fireservice.make_cheap_zones(o)
    
    return (v)

# GET LIST OF MOST EXPENSIVE ZONES N IS THE MAX NUMBER, RETURN ZONE , AVG PRICE
@blueprint.route('/expensivestzones', methods=['GET'])
async def expensivestzones():
    query = offers.Offer.objects().all()
    o = query.to_json()
    v =  fireservice.make_expensive_zones(o)
    return jsonify(v)

# GET LIST OF ZONES / AVERAGE PRICE
@blueprint.route('/pricezone', methods=['GET'])
async def avgzone():
    query = offers.Offer.objects().all()
    o = query.to_json()
    v =  fireservice.make_zonemean(o,"price")
    regressions.Regression(
        coefs=v["coefs"],
        rank=v["rank"],
        singular=v["singular"],
        intercept=v["intercept"],
        scores=v["scores"]
    ).save()
    return jsonify(v)

# GET REGRESSION DATA
@blueprint.route('/getregressions', methods=['GET'])
async def getreg():
    query = regressions.Regression.objects()
    o = query.to_json()
    return jsonify(o)


# RUN REGRESSION ANALYSIS
@blueprint.route('/runreg', methods=['POST'])
async def runreg():
    data = await request.form 
    val = data["val"]
    random_state = data["random_state"]
    n_splits = data["n_splits"]
    feats = data.getlist('feats')

    query = offers.Offer.objects().limit(1000)
    o = query.to_json()
    v = await fireservice.make_regression(o, val=val, feats=feats, n_splits=n_splits, random_state=random_state)
    return jsonify(v)
## BOTS MANAGEMENT

# LIST ALL BOTS
@blueprint.route('/bots', methods=['GET'])
async def botsdetails():
    return ""

# ADD A NEW BPAT
@blueprint.route('/addbot/', methods=['POST'])
async def addbot():
    return ""

# DELBOT
@blueprint.route('/delbot/<o>', methods=['GET'])
async def delbot(o: int):
    return ""

# LIST ALL DATA RELATED TO ONE OFFER, FILTER BY NAME
@blueprint.route('/runbot/<o>', methods=['GET'])
async def runbot(o: str):
    return ""

@blueprint.route('/flats/<n>', methods=['GET'])
async def flatsn(n: int):
    query = offers.Offer.objects.all().limit(int(n))
    o = query.to_json()
    return jsonify(o)


@blueprint.route('/flats/', methods=['GET'])
async def flats():
    query = offers.Offer.objects.all().limit(5)
    o = query.to_json()
    return jsonify(o)


