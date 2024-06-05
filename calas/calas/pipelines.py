import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from calas.models import Image, Product, Category

class CalasPipeline:
    def __init__(self):
        # Create a connection to the database
        self.engine = create_engine('mariadb+mariadbconnector://calas:T2iEYtVA6QdaQIEe@localhost/calas')
        self.Session = sessionmaker(bind=self.engine)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        # Create a session
        with self.Session() as session:
            try:
                main_image_url = item['images'][0].split('/')[-1] if item['images'] else None
                #pdf = item['pdf'].split('/')[-1] if item['pdf'] else None

                # Convert lists to JSON strings
                material = json.dumps(item['material']) if item['material'] else None
                color = json.dumps(item['color']) if item['color'] else None
                weight = json.dumps(item['weight']) if item['weight'] else None
                dimensions = json.dumps(item['dimensions']) if item['dimensions'] else None
                stock = json.dumps(item['stock']) if item['stock'] else None
                pdf = item['pdf'] if item['pdf'] else None

                # Query the database for the record you want to update
                record = session.query(Product).filter_by(url=item['url']).first()

                # Update the record if found, else create a new record
                if record:
                    self.logger.info(f"Updating existing product with URL: {item['name']}")
                    record.price = item['price']
                    record.name = item['name']
                    record.description = item['description']
                    record.url = item['url']
                    record.Material = material
                    record.color = color
                    record.Weight = weight
                    record.Size = dimensions
                    record.Stock = stock
                    record.pdf = pdf
                    record.main_image_url = main_image_url
                    spider.logger.info("Record updated successfully.")

                else:
                    self.logger.info(f"Creating new product with URL: {item['name']}")
                    new_record = Product(
                        sku=item['sku'],
                        url=item['url'],
                        name=item['name'],
                        price=item['price'],
                        description=item['description'],
                        Material=material,
                        color=color,
                        Weight=weight,
                        Size=dimensions,
                        Stock=stock,
                        pdf=pdf,
                        main_image_url=main_image_url
                    )
                    session.add(new_record)
                    spider.logger.info("New record created successfully.")

                session.commit()

                # Handle images
                for image in item['images']:
                    image_value = image.split('/')[-1]
                    img_record = session.query(Image).filter_by(image_url=image_value).first()
                    if not img_record:
                        self.logger.info(f"Creating new image record for URL: {item['name']} with image URL: {image_value}")
                        image_record = Image(image_url=image_value, name=item['name'])
                        session.add(image_record)
                        session.commit()
                        spider.logger.info("Image record created successfully.")
                    else:
                        self.logger.info(f"Updating existing image record for URL: {item['name']} with image URL: {image_value}")
                        img_record.image_url = image_value
                        session.add(img_record)
                        session.commit()
                        spider.logger.info("Image updated.")

                # Handle categories
                for category in item['category_id']:
                    category_value = category
                    cat_record = session.query(Category).filter_by(category=category_value).first()
                    if not cat_record:
                        self.logger.info(f"Creating new category record for URL: {item['name']} with category: {category_value}")
                        cat_record = Category(category=category_value, name=item['name'])
                        session.add(cat_record)
                        session.commit()
                        spider.logger.info("Category record created successfully.")
                    else:
                        self.logger.info(f"Updating existing category record for URL: {item['name']} with category: {category_value}")
                        cat_record.category = category_value
                        session.add(cat_record)
                        session.commit()
                        spider.logger.info("Category updated.")

            except Exception as e:
                # Rollback the changes in case of an error
                session.rollback()
                self.logger.error(f"Failed to process item: {e}", exc_info=True)

        return item
