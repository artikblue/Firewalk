from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from habitaclia.spiders.habitacliabot import HabitacliabotSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(HabitacliabotSpider)
process.start()