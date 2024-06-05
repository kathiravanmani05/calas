from django.db import models
import datetime
import os



class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, primary_key=True)
    price = models.CharField(max_length=8)
    description = models.TextField()
    #main_category = models.CharField(max_length=100)
    Material = models.CharField(max_length=100)  # If "Material" is a field you want to include
    color = models.CharField(max_length=50)
    Weight = models.CharField(max_length=50)
    Size = models.CharField(max_length=50)
    Stock = models.CharField(max_length=50)
    pdf = models.CharField(max_length=255)
    LastScrappeddate = models.DateTimeField(auto_now=True)
    Updateddate = models.DateTimeField(auto_now=True)
    Createddate = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50)
    main_image_url = models.CharField(max_length=255)
    class Meta:
        db_table = 'product'

class Image(models.Model):
    image_url = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'images'

class Category(models.Model):

    category = models.CharField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'
