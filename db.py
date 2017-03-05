from flask_sqlalchemy import SQLAlchemy
from app import app
import os.path

is_database_created = os.path.isfile("data.db")
db = SQLAlchemy(app)

from models.category import Category
from models.attribute import Attribute
from models.product import Product, ProductImage, ProductAttributes, ProductStockSize
from models.color import Color
from models.userModel import User

import crawler.deezee_spider
from scrapy.crawler import CrawlerProcess

def fill_database():
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(crawler.deezee_spider.DeeZeeSpider)
    process.start()

if not is_database_created:
    db.create_all()
    #fill_database()
    db.session.commit()