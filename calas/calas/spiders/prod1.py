import scrapy
from scrapy import Request
import os
import requests


class ProdSpider(scrapy.Spider):
    name = "prod1"
    allowed_domains = ["calas.cl"]
    start_urls = ["https://calas.cl"]

    def parse(self, response):
        links = response.xpath('//*[@class="sub-menu color-scheme-dark"]/li/a/@href').extract()
        unique_links = list(set(links))
        for url in unique_links:
            yield Request(url, callback=self.data_link, meta={'url': url})

    def data_link(self, response):
        product_links = response.xpath('//*[@class="product-element-top"]/a/@href').extract()
        unique_product_links = list(set(product_links))
        for product_url in unique_product_links:
            print(product_url)
            yield Request(product_url, callback=self.data_parser)

        next_page = response.xpath('//*[@class="next page-numbers"]/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.data_link)

    def check_file_in_folder(self, folder, file):
        return os.path.exists(os.path.join(folder, file))

    def save_image(self, temp_images, folder="Image"):
        for url in temp_images:
            abs_url = url
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = url.split('/')[-1]
            if self.check_file_in_folder(folder, file_name):
                continue
            filepath = os.path.join(folder, file_name)

            response = requests.get(abs_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                    print(f"Image saved as {filepath}")
            else:
                print(f"Failed to download image from {abs_url}")

    def data_parser(self, response):
        title = response.xpath('//*[@class="product_title entry-title"]/text()').extract_first()
        descriptions = response.xpath('//*[@class="woocommerce-product-details__short-description"]//text()').extract()
        description = ' '.join(item.strip() for item in descriptions if item.strip())
        sku = response.xpath('//*[@class="sku"]/text()').extract_first()
        price = response.xpath('//*[@class="price"]/span/bdi/text()').extract_first()
        images = response.xpath('//*[@class="woocommerce-product-gallery__image"]/@data-thumb').extract()
        self.save_image(images)
        
        allowed_categories = [
            'Poliester', 'Spandex', 'Tulip', 'Taburete', 'Juegos', 'Mesa', 'Mobiliario niño', 
            'Eames', 'Lazo', 'Manteles', 'Toldo', 'Sillas', 'Mobiliario Hogar', 'Mesas', 
            'Oficina', 'Alto', 'Pisos', 'Fijas', 'Plegables'
        ]
        
        categories = response.xpath('//*[@class="posted_in"]//text()').extract()
        categories_cleaned = [item.strip() for item in categories if item.strip() and item.strip() in allowed_categories]

        for cat in categories_cleaned:
            item = {
                'url': response.url,
                'name': title,
                'description': description,
                'sku': sku,
                'price': price,
                'category_id': cat,
                'images': images
            }
            yield item
