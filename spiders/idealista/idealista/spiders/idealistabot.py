# -*- coding: utf-8 -*-
import scrapy
import re
import os
import datetime
import time
import random
class IdealistabotSpider(scrapy.Spider):
    name = 'idealista'
    allowed_domains = ['idealista.com']
    #start_urls=['https://www.idealista.com/alquiler-viviendas/madrid-madrid/']

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', [])
        urls = os.environ["URLS"]
        if urls:
            self.start_urls = urls.split(',')
        #self.logger.info(self.start_urls)
        super(IdealistabotSpider, self).__init__(*args, **kwargs)
        
    def parse(self, response):

        print("RESPONSE")
        print(response)

        url_selector = '//div[@class="item-info-container"]/a/@href'
        url_content = response.xpath(url_selector).extract()
        
        for i in url_content:
            headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
            headers2= {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
            agents = [headers, headers2]
            na = random.randint(0,1)

            url = "https://idealista.com"+str(i)
            yield scrapy.Request(url = url, headers=headers,callback = self.parse_item)
            nr = random.randint(1,5)
            time.sleep(nr)
        
        next_pag_selector = '//a[@class="icon-arrow-right-after"]/@href'
        next_pag = response.xpath(next_pag_selector).extract()
        print(next_pag)
        npag = "https://idealista.com"+next_pag[0]
        if next_pag:
            print("NPAG")
            print(npag)
            nr = random.randint(1,9)
            time.sleep(nr)
            yield scrapy.Request(url = npag, headers=headers, callback = self.parse)

        #yield scrapy.Request(url = "https://idealista.com"+next_pag[0], headers=headers)

    def get_toilets(self, feats):
        toilet = 0
        for f in feats:

            if "baño" in f:
                toilet = int(f[0])
                break
        return toilet


    def parse_item(self, response):
        selector_name = '//span[@class="main-info__title-main"]/text()'
        name_content = response.xpath(selector_name).extract()

        selector_price = '//span[@class="info-data-price"]/span/text()'
        price_content = response.xpath(selector_price).extract()

        selector_space = '//div[@class="info-features"]/span/span/text()'
        space_content = response.xpath(selector_space).extract()

        selector_address = '//span[@class="main-info__title-minor"]/text()'
        address_content = response.xpath(selector_address).extract()

        selector_images = '//div[@id="multimedia-container"]'
        images_content = response.xpath(selector_images).extract()

        selector_features = '//div[@class="details-property_features"]/ul/li/text()'
        features_content = response.xpath(selector_features).extract()
        
        selector_company = '//div[@class="professional-name"]/span/text()'
        company_content = response.xpath(selector_company).extract()

        selector_features = '//div[@class="details-property_features"]/ul/li/text()'
        selector_content = response.xpath(selector_features).extract()

        selector_zone = '//span[@class="main-info__title-minor"]/text()'
        zone_content = response.xpath(selector_zone).extract()

        try:
            zone = zone_content[0]
            zone = zone.split(',')
            zone = zone[0]
            
        except:
            zone = "unknown"

        text = response.text

        try:
            # property images are loaded via javascript, so we need to parse the js code using regex
            image_list = re.findall(r'imageDataService:"+(.*?)(?:,WEB_DETAIL|$)', text, re.DOTALL)
        except:
            image_list = []
        
        feature_list = features_content
        try:
            address = address_content[0]
        except:
            address = ""
        try:
            price = price_content[0]
            price = price.replace(".","")
            price = int(price)
        except:
            price = 0
        try:
            name = name_content[0]
        except:
            name = ""
        try:
            space = space_content[0]
            space = space.replace(".","")
            space = int(space)
        except:
            space = 0
        try:
            rooms = space_content[1]
            rooms = int(rooms)
        except:
            rooms = 0
        try:
            company = company_content[0]
        except:
            company = ""
        url = response.url
        parse_date = str(datetime.datetime.now())
        toilets  = self.get_toilets(features_content)
        offer_object = {
            "url":url,
            "city":"Madrid",
            "site":"idealista",
            "company":company,
            "zone": zone,
            "toilets":toilets,
            "rooms":rooms,
            "price":price,
            "surface":space,
            "name":name,
            "address":address,
            "images":image_list,
            "feats":features_content,
            "parse_date":parse_date
        }


        """
        offer_object = {
            "site":"habitaclia",
            "city":"Madrid",
            "zone":zone,
            "url":url,
            "name":name,
            "address":address,
            "toilets":toilets,
            "price":price,
            "rooms":rooms,
            "surface":surface,
            "images":images_content,
            "company":company,
            "feats":distrib_content,
            "parse_date":parse_date
        }

        """
        yield offer_object
