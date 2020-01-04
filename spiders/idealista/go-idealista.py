from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from idealista.spiders.idealistabot import IdealistabotSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(IdealistabotSpider)
process.start()