import json, requests
"""
print("round 1")

url = "http://127.0.0.1:5001/runcluster"


data = {
     "vals":['price','surface','rooms','toilets','feats','images'],
     "numpca":3,
     "numclusters":5,
     "algorithm":"elkan"
}

r = requests.post(url=url, data=data)
print(r.text)

print("round 2")
data = {
     "vals":['price','surface','rooms','toilets'],
     "numpca":2,
     "numclusters":5
}

r = requests.post(url=url, data=data)
print(r.text)
"""
"""

url = "http://127.0.0.1:5001/runreg"

print("round 1")
data = {
     "feats":['surface','rooms','toilets', 'images', 'feats'],
     "val":"price"
}

r = requests.post(url=url, data=data)
print(r.text)


print("round 2")
data = {
     "feats":['surface','rooms','toilets', 'images'],
     "val":"price"
}

r = requests.post(url=url, data=data)
print(r.text)


print("round 3")
data = {
     "feats":['surface','rooms','toilets'],
     "val":"price"
}

r = requests.post(url=url, data=data)
print(r.text)


print("round 4")
data = {
     "feats":['surface','rooms'],
     "val":"price"
}

r = requests.post(url=url, data=data)
print(r.text)

print("round 5")
data = {
     "feats":['feats'],
     "val":"price",
     "random_state":42,
     "num_folds":3
}
url = "http://127.0.0.1:5001/genclassifier"

data = {
    "feats":["num_photos","num_feats","site_num","city_num","zone_num","company_num","surface","rooms","toilets"],
    "criterion":"gini",
    "random_state":99,
    "min_samples_split":20,
    "max_depth":4,
    "test_size":0.4
}

r = requests.post(url=url, data=data)
print(r.text)

"""



url = "http://127.0.0.1:5001/classify"

data = {
    "feats": [4,3,1,2,2,3,9999,6,2]
}

r = requests.post(url=url, data=data)
print(r.text)


url = "http://127.0.0.1:5001/classify"

data = {
    "feats": [4,3,1,2,2,3,100,2,2]
}

r = requests.post(url=url, data=data)
print(r.text)
