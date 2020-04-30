import quart
from quart import jsonify

from services import fireservice
import asyncio
blueprint = quart.blueprints.Blueprint(__name__, __name__)


from models import offers


"""
@blueprint.route('/character/<n>', methods=['GET'])
async def character(n: str):
    character = await fireservice.characters(n)

    return quart.jsonify(character)



    Offer


@blueprint.route('/flats/', methods=['GET'])
async def flats():
    query = offers.Offer.objects.all().limit(5)
    o = query.to_json()
    return jsonify(o)

"""


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
    print(query)
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
        print(query)
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
        print(query)
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
        print(query)
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
@blueprint.route('/offerchart', methods=['GET'])
async def offerchart():
    return ""


# RETURN A LIST CATEGORY:COUNT (EXPENSIVE, CHEAP---) CATEGORY/UNITS
@blueprint.route('/categories', methods=['GET'])
async def categories():
    return ""

# RETURN A LIST SITE:COUNT (SITE, NUMBER---) CATEGORY/UNITS
@blueprint.route('/sitescount', methods=['GET'])
async def sitescounterI():
    return ""

# LIST ALL DATA RELATED TO ONE OFFER, FILTER BY NAME
@blueprint.route('/offerdetails/<o>', methods=['GET'])
async def offerdetails(o: str):
    return ""



## STATISTICAL / DATA MANAGEMENT

# GET ALL CLUSTER DATA
@blueprint.route('/getclusters', methods=['GET'])
async def getclusters():
    return ""

# RUN CLUSTER ANALYSIS WHERE N I S THE NUMBER OF CLUSTER -> RESULT GOES TO RRESULTS DB
@blueprint.route('/runcluster/<n>', methods=['GET'])
async def runcluster(n: int):
    return ""

# GET GENERAL STATS
@blueprint.route('/generalstats', methods=['GET'])
async def generalstats():
    return ""

# GET GEO POINTS RETURNS -> NAME, GEOCOORDS, ROOMS, SURFACE, TOILETS, PRICE, URL | {CITY, NUMBER OF REGISTERS}}
@blueprint.route('/getgeopoints/', methods=['POST'])
async def getgeopoints():
    return ""

# GET LIST OF MOST INFLUENCIAL ATRIBUTES FOR PRICE
@blueprint.route('/influencialfeats', methods=['GET'])
async def influencialatribs():
    return ""

# GET LIST OF CHEAPEST ZONES N IS THE MAX NUMBER, RETURN ZONE , AVG PRICE
@blueprint.route('/cheapestzones/<n>', methods=['GET'])
async def cheapestzones(o: int):
    return ""

# GET LIST OF MOST EXPENSIVE ZONES N IS THE MAX NUMBER, RETURN ZONE , AVG PRICE
@blueprint.route('/expensivestzones/<n>', methods=['GET'])
async def expensivestzones(o: int):
    return ""

# GET LIST OF ZONES / AVERAGE PRICE
@blueprint.route('/pricezone', methods=['GET'])
async def avgzone():
    return ""

# GET REGRESSION DATA
@blueprint.route('/getregression', methods=['GET'])
async def getreg():
    return ""


# RUN REGRESSION ANALYSIS
@blueprint.route('/runreg', methods=['GET'])
async def runreg():
    return ""
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


# example of a s y n c function

@blueprint.route('/pi/<n>', methods=['GET'])
async def pi(n: str):
    pi = await fireservice.compute_pi(int(n))

    return quart.jsonify( {'dec':n,'pi':pi})