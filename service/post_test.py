import json, requests
"""
print("round 1")
data = {
     "vals":['price','surface','rooms','toilets','feats','images'],
     "numpca":3,
     "numclusters":5
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

r = requests.post(url=url, data=data)
print(r.text)
