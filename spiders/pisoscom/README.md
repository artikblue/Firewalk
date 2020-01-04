## Habitaclia.com bot

### Installing
This docker carries the task of retrieving data (offers) realted to the site pisos.com and sending it through kafka.

The docker image can be built by:

```
docker build -t pisoscom1 .
```
### Running
And after the spider can be easily launched by:
```
docker run  -e KAFKA_SERVER=10.0.2.15:9092 -e KAFKA_QUEUE=habitaclia -e URLS=https://www.habitaclia.com/alquiler-vivienda-en-corredor_del_henares/provincia_madrid/selarea.htm pisoscom1
```
And you should start getting objects such as:

### Data dictionary
```
offer_object = {
            "name":name,
            "price":price,
            "space":space,
            "address":address,
            "rooms":rooms,
            "url":url,
            "gallery":gallery_content
        }
```
