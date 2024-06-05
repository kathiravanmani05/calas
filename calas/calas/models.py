from sqlalchemy import create_engine, Column, String, ForeignKey, Integer, DECIMAL, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = 'product'

    sku = Column(String(50))
    url = Column(String(255))
    name = Column(String(255), primary_key=True)
    price = Column(String(8))
    description = Column(Text)
    #main_category = Column(String(100))
    Material = Column(String(100))
    color = Column(String(50))
    Weight = Column(String(50))
    Size = Column(String(50))
    Stock = Column(String(50))
    pdf = Column(String(255))
    LastScrappeddate = Column(DateTime, onupdate=func.now())
    Updateddate = Column(DateTime, onupdate=func.now())
    Createddate = Column(DateTime, default=func.now())
    Status = Column(String(50))
    main_image_url = Column(String(255))

class Image(Base):
    __tablename__ = 'images'

    image_url = Column(String(255), primary_key=True)
    name = Column(String(255), ForeignKey('product.name'))

class Category(Base):
    __tablename__ = 'categories'

    #id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(255), primary_key=True)
    name = Column(String(255), ForeignKey('product.name'), primary_key=True)

# Define your database connection
engine = create_engine('mariadb+mariadbconnector://calas:T2iEYtVA6QdaQIEe@localhost/calas')
#engine = create_engine('mysql://root:root@localhost/calas')

# Create the tables
Base.metadata.create_all(engine)
