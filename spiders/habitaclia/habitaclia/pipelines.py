# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from kafka import KafkaProducer
import json
import os

class HabitacliaPipeline(object):

    collection_name = 'habitaclia'

    def __init__(self, kafka_server, kafka_queue):
        self.kafka_server = kafka_server
        self.kafka_queue = kafka_queue


    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        # kafka_server=crawler.settings.get('KAFKA_SERVER'),
        return cls(
            kafka_server=os.environ['KAFKA_SERVER'],
            kafka_queue=os.environ['KAFKA_QUEUE']
        )
    
    def open_spider(self, spider):
        ## initializing spider
        ## opening db/kafka connection
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    def close_spider(self, spider):
        ## clean up when spider is closed
        self.producer.close()
        # self producer.close


    def process_item(self, item, spider):
        #self.db[self.collection_name].insert(item)
        self.producer.send(self.kafka_queue,item)
        logging.debug("Post sent to kafka")
        return item
