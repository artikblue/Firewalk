from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pisoscom.spiders.pisoscombot import PisoscombotSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(PisoscombotSpider)
process.start()