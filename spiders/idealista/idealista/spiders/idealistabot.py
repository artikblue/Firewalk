# -*- coding: utf-8 -*-
import scrapy
import re
import os
import time
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
            url = "https://idealista.com"+str(i)
            yield scrapy.Request(url = url, callback = self.parse_item)
            time.sleep(2)
        
        next_pag_selector = '//a[@class="icon-arrow-right-after"]/@href'
        next_pag = response.xpath(next_pag_selector).extract()

        yield scrapy.Request(url = next_pag[0])

    def parse_item(self, response):
        selector_name = '//span[@class="main-info__title-main"]/text()'
        name_content = response.xpath(selector_name).extract()

        selector_price = '//span[@class="info-data-price"]/text()'
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

        yield offer_object
