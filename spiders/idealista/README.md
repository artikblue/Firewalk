## Habitaclia.com bot

### Installing
This docker carries the task of retrieving data (offers) realted to the site idealista.com and sending it through kafka.

The docker image can be built by:

```
docker build -t idealista1 .
```
### Running
And after the spider can be easily launched by:
```
docker run  -e KAFKA_SERVER=10.0.2.15:9092 -e KAFKA_QUEUE=idealista -e URLS=https://www.idealista.com/alquiler-viviendas/madrid-madrid/ idealista1
```
And you should start getting objects such as:

### Data dictionary
```
offer_object = {
            "url":url,
            "company":company,
            "rooms":rooms,
            "price":price,
            "space":space,
            "name":name,
            "address":address,
            "gallery":image_list
}
```