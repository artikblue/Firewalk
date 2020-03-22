# -*- coding: utf-8 -*-
import scrapy
import re
import os
import datetime

# scrapy crawl pisoscombot -a "urls=https://www.pisos.com/alquiler/pisos-madrid_sur/"

class PisoscombotSpider(scrapy.Spider):
    name = 'pisoscombot'
    allowed_domains = ['www.pisos.com']

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', [])
        urls = os.environ.get('URLS')
        if urls:
            self.start_urls = urls.split(',')
        #self.logger.info(self.start_urls)
        super(PisoscombotSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        selector_item = '//div[@class="row  clearfix"]/@data-navigate-ref'
        item = response.xpath(selector_item).extract()
        base_url = "https://www.pisos.com/"

        selector_next_pag = '//a[@id="lnkPagSig"]/@href'
        next_pag_content = response.xpath(selector_next_pag).extract()
        
        for i in item:
            yield scrapy.Request(url = base_url+ str(i), callback = self.parse_item)

        u = base_url + str(next_pag_content[0])

        yield scrapy.Request(url = u , callback = self.parse)

    def parse_item(self, response):

        selector_price = '//div[@class="priceBox-price"]/span/text()'
        price_content = response.xpath(selector_price).extract()

        selector_name = '//div[@class="maindata-info"]/h1/text()'
        name_content = response.xpath(selector_name).extract()

        selector_address = '//h2[@class="position"]/text()'
        address_content = response.xpath(selector_address).extract()

        selector_basicinfo = '//div[@class="basicdata-info"]/div/text()'
        basicinfo_content = response.xpath(selector_basicinfo).extract()

        selector_property = '//div[@class="owner-data-info"]/a/text()'
        property_content = response.xpath(selector_property).extract()

        selector_gallery = '//input[@name="PhotosPath"]/@value'
        gallery_content = response.xpath(selector_gallery).extract()

        selector_basicatribs = '//li[@class="charblock-element element-with-bullet"]/span/text()'
        basicatribs_content = response.xpath(selector_basicatribs).extract()

        selector_company = '//div[@class="owner-data-info"]/a/text()'
        company_content = response.xpath(selector_company).extract()

        selector_feats = '//li[@class="charblock-element element-with-bullet"]/span/text()'
        feats_content = response.xpath(selector_feats).extract()

        try:
            company = company_content[0]
        except:
            company = "unknown"

        try:
            gallery_content = gallery_content[0].replace('!','').split(',')
        except:
            gallery_content = []
        try:
            name = name_content[0]
        except:
            name = ""
        try:
            price =  re.findall(r'\d+', price_content[0])[0]
            price = price.replace('.','')
            price = int(price)
        except:
            price = 0
        try:
            space = re.findall(r'\d+', basicinfo_content[0])[0]
            space = int(space)
        except:
            space = 0
        try:
            address = address_content[0]
        except:
            address = 0
        try:
            rooms = re.findall(r'\d+', basicinfo_content[1])[0]
            rooms = int(rooms)
        except:
            rooms = 0
        try:
            toilets = re.findall(r'\d+', basicinfo_content[2])[0]
            toilets = int(toilets)
        except:
            toilets = 0
        
        
        url = response.url
        parse_date = str(datetime.datetime.now())
        #debug info:
        print(url)
        print(name)
        print(price)
        print(space)
        print(address)
        print(rooms)
        print(company)
        print(parse_date)
        print(feats_content)

        

        offer_object = {
            "name":name,
            "price":price,
            "space":space,
            "address":address,
            "rooms":rooms,
            "url":url,
            "gallery":gallery_content,
            "company":company,
            "feats":feats_content,
            "toilets":toilets,
            "parse_date":parse_date
        }

        yield offer_object

        
        
        
        