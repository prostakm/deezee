from crawler.deezee_spider import DeeZeeSpider
from scrapy.crawler import CrawlerProcess

def fill_database():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_EXPORT_ENCODING': 'utf-8'
    })
    process.crawl(DeeZeeSpider)
    process.start()