from django.db import models
import datetime
import os



class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
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

    # Define the ForeignKey relationship
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'



    #def getFileName(request, filename):
    #    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    #    new_filename = "%s%s" % (now_time, filename)
    #    return os.path.join('uploads/', new_filename)

    #class Category(models.Model):
#    name = models.CharField(max_length=100, primary_key=True)  # Making 'name' the primary key
#    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.name