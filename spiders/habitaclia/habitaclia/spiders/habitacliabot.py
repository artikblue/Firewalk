# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import os

class HabitacliabotSpider(scrapy.Spider):
    name = 'habitacliabot'
    allowed_domains = ['habitaclia.com']
    #start_urls = ['https://www.habitaclia.com/alquiler-vivienda-en-corredor_del_henares/provincia_madrid/selarea.htm']

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', [])
        urls = os.environ.get('URLS')
        print(urls)
        if urls:
            self.start_urls = urls.split(',')
        #self.logger.info(self.start_urls)
        super(HabitacliabotSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        selector = '//ul[@class="verticalul"]/li/a/@href'
        url_content = response.xpath(selector).extract()
        print(url_content)

        selector_zona = '//div[@class="ver-todo-zona"]/a/@href'
        zona_content = response.xpath(selector_zona).extract()

        if zona_content:
            yield scrapy.Request(url = zona_content[0], callback = self.parse_page)
        else:
            for u in url_content:
                yield scrapy.Request(url = u, callback = self.parse)

    def parse_page(self, response):
        print(response)

        selector_offer = '//h3[@class="list-item-title"]/a/@href'
        offer_content = response.xpath(selector_offer).extract()

        for u in offer_content:
            yield scrapy.Request(url = u, callback = self.parse_offer)

        selector_next = '//li[@class="next"]/a/@href'
        next_content = response.xpath(selector_next).extract()

        if next_content:
            yield scrapy.Request(url = next_content[0], callback = self.parse_page)

    def parse_offer(self, response):
        selector_name = '//div[@class="summary-left"]/h1/text()'
        name_content = response.xpath(selector_name).extract()

        selector_price = '//span[@itemprop="price"]/text()'
        price_content = response.xpath(selector_price).extract()

        selector_address = '//h4[@class="address"]/text()'
        address_content = response.xpath(selector_address).extract()

        selector_distrib = '//article[@class="has-aside"]/ul/li/text()'
        distrib_content = response.xpath(selector_distrib).extract()
        
        try:
            address = address_content[1].strip()
        except:
            address = "unknown"
        try:
            name = name_content[0]
        except:
            name = "unknown"
        try:
            price = price_content[0]
            price = price.replace(".","")
            price =  re.findall(r'\d+', price)[0]
        except:
            price = 0
        try:
            rooms = distrib_content[0][:2]
        except:
            rooms = 0
        try:
            surface = distrib_content[1]
            surface =  re.findall(r'\d+', surface)[0]
        except:
            surface = 0
        selector_images = '//div[@class="flex-images"]/div/@url'
        images_content = response.xpath(selector_images).extract()
        url = response.url

        print(address)
        print(name)
        print(price)
        print(rooms)
        print(surface)

        offer_object = {
            "url":url,
            "name":name,
            "address":address,
            "price":price,
            "rooms":rooms,
            "surface":surface,
            "images":images_content
        }

        yield offer_object



