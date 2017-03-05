from scrapy import Spider, Request
import db
import models.category
import models.color
import models.attribute
import models.product

database = db.db


def create_categories(categories):
    category_models = map(lambda x: models.category.Category(x), categories)
    for category in category_models:
        db.db.session.add(category)
    db.db.session.commit()

def create_colors(colors):
    color_models = map(lambda x: models.color.Color(x, '000000'), colors)
    for color in color_models:
        db.db.session.add(color)
    db.db.session.commit()

def create_attributes(attributes):
    attribute_models = map(lambda x: models.attribute.Attribute(x), attributes)
    for attribute in attribute_models:
        db.db.session.add(attribute)
    db.db.session.commit()

def create_products(products):
    attribute_models = []
    for product_dict in products:
        product = models.product.Product(product_dict['name'])
        product.current_price = float(product_dict['current_price'])
        product.standard_price = float(product_dict['standard_price'])
        product.color = models.color.Color.query.filter_by(name=product_dict['color']).first()
        set_attributes_for_product(product_dict['attributes'], product)
        set_images_for_product(product_dict['images'], product)
        set_sizes_for_product(product_dict['av_sizes'], product_dict['un-sizes'], product)
        set_categories_for_product(product_dict['categories'], product)
        database.session.add(product)
    database.session.commit()

def set_categories_for_product(categories, product):
    for category in categories:
        category_model = models.category.Category.query.filter_by(name=category).first()
        print models.category.Category.query.first()
        if category_model:
            product.categories.append(category_model)

def set_attributes_for_product(attributes, product):
    hash_string = ""
    for key_value in attributes:
        attribute_name = key_value[0]
        attribute_value = key_value[1]
        attribute = models.attribute.Attribute.query.filter_by(name=attribute_name).first()
        product_attribute = models.product.ProductAttributes()
        product_attribute.product = product
        product_attribute.attribute = attribute
        product_attribute.value = attribute_value
        product.attributes.append(product_attribute)
        hash_string = hash_string + attribute_value + attribute_name
    product.attributes_hash = hash(hash_string)

def set_images_for_product(images, product):
    for image in images:
        product_image = models.product.ProductImage()
        product_image.product_id = product.id
        product_image.image_url = image
        product.images.append(product_image)

def set_sizes_for_product(available, unavailable, product):
    for available_size in available:
        size = models.product.ProductStockSize()
        size.product_id = product.id
        size.size = available_size
        size.stock = 5
        product.stockSize.append(size)

    for unavailable_size in unavailable:
        size = models.product.ProductStockSize()
        size.product_id = product.id
        size.size = unavailable_size
        size.stock = 0
        product.stockSize.append(size)



class DeeZeeSpider(Spider):

    name = 'Tarantula'
    _categoryItemsXPath = '//*[@id="js-header"]/div[2]/div/div[2]/nav/ul/li[1]/div/div/div/div/div[1]/div[1]/nav/li'

    categories = []
    products = []

    start_urls = ['https://www.deezee.pl/']

    def parse(self, response):
        categoriesSelector = response.xpath(self._categoryItemsXPath)
        for category_item in [categoriesSelector[0], categoriesSelector[1], categoriesSelector[3]]:
            category_name = category_item.select('./a/text()').extract_first()
            normalized_name = ' '.join(category_name.split())
            self.categories.append(normalized_name)
            category_url = category_item.select('./a/@href').extract_first()
            if category_url is not None:
                print category_url
                next_page = "https://www.deezee.pl" + category_url
                productsRequest = Request(next_page, callback=self.parse_category_item_list)
                productsRequest.meta['category'] = normalized_name
                yield productsRequest

    def parse_category_item_list(self, response):
        category = response.meta['category']
        productUrls = response.xpath('//*[@class="m-offerBox_image js-offerBox-img g-posr"]/a/@href').extract()
        for product_url in productUrls:
            print product_url + ' ' + category
            request = Request('https://www.deezee.pl' + product_url, callback=self.parse_product_details)
            request.meta['category'] = category
            yield request

    def parse_product_details(self, response):
        name = response.xpath('//*[@id="js-product-view"]/div[1]/div/h1/text()').extract_first()
        standard_price = response.xpath('//div[@id="js-product-view"]/@data-offer-price').extract_first()
        current_price = response.xpath('//div[@itemprop="offers"]/meta[@itemprop="price"]/@content').extract_first()
        colors = response.xpath('//*[@class="m-offerColors_container clearfix2"]/a[@class="m-offerColors_item offer"]/@title').extract()
        unavailable_sizes = response.xpath('//li[contains(@class,"m-offerSizes_listItem js-offerSizes_item") and contains(@class, "is-disabled")]/p/text()').extract()
        available_sizes = response.xpath('//li[contains(@class,"m-offerSizes_listItem js-offerSizes_item") and not(contains(@class, "is-disabled"))]/p/text()').extract()
        attributes = response.xpath('//dl[@class="m-offerShowData_row clearfix2"]/p/text()').extract()
        images = response.xpath('//*[@class="m-offerGallery_picture"]/@src').extract()
        ext_id = response.xpath('//div[@class="js-ajaxChain_item"]/@data-offer-id').extract_first()
        category = response.meta['category']

        print ' '.join(name.split())
        print standard_price
        print current_price
        for attribute in attributes:
            print ' '.join(attribute.split()).split(': ')
        print images
        print colors
        print list(map(lambda x: ' '.join(x.split()), unavailable_sizes))
        print list(map(lambda x: ' '.join(x.split()), available_sizes))

        atribute_name_value = list(map(lambda x: ' '.join(x.split()).split(': '), attributes))
        product = {
            'name': ' '.join(name.split()),
            'standard_price': standard_price,
            'current_price' : current_price,
            'colors': colors,
            'color': colors[0],
            'av_sizes': list(map(lambda x: x.replace(' - ', ''), available_sizes)),
            'un-sizes': list(map(lambda x: x.replace(' - ', ''), unavailable_sizes)),
            'attributes': atribute_name_value,
            'images': images,
            'external_id': ext_id,
            'categories': [category]
        }
        self.products.append(product)

    def closed(self, reason):

        distinct_attributes = self.get_distinct_attributes(self.products)
        distinct_colors = self.get_distinct_colors(self.products)
        distinct_products = self.get_distinct_products(self.products)

        print distinct_attributes
        print distinct_colors

        create_categories(self.categories)
        create_colors(distinct_colors)
        create_attributes(distinct_attributes)
        create_products(distinct_products)

    def get_distinct_attributes(self, products):
        uniqueAttributes = set()
        for product in products:
            uniqueAttributes.update(map(lambda x: x[0], product['attributes']))
        return uniqueAttributes

    def get_distinct_colors(self, products):
        unique_colors = set()
        for product in products:
            unique_colors.update(map(lambda x: x, product['colors']))
        print unique_colors
        return unique_colors

    def get_distinct_products(self, products):
        unique_products = dict()
        for product in products:
            if not product['name'] in unique_products:
                unique_products[product['name']] = product
            else:
                prod_dict = unique_products[product['name']]
                prod_dict['categories'] = prod_dict['categories'].append(product['categories'])
                unique_products[product['name']] = prod_dict

        return unique_products.values()

