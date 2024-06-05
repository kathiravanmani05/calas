from shop.models import Product,Image,Category

def fetch_categories():
    unique_categories = Category.objects.values_list('category', flat=True).distinct()
    return unique_categories

def fetch_products(category):
    products = []
    category_instances = Category.objects.filter(category=category).distinct()
    
     # Print queryset to check if it contains all instances
    for category_instance in category_instances:
        category_name = category_instance.name
        product = Product.objects.filter(name=category_name).values('name', 'sku', 'main_image_url', 'price')
        products.extend(product)
    return products 

def fetch_product_detail(name):
    product = Product.objects.filter(name=name).values().first()
    images = Image.objects.filter(name=name).values_list('image_url', flat=True)
    Categories = Category.objects.filter(name=name).values_list('category', flat=True)

    return product, images ,Categories

def search_product(search_variable):
    if not search_variable:
        return None, None
    product = Product.objects.filter(sku=search_variable).values().first()
    if not product:
        product = Product.objects.filter(name__icontains=search_variable).values().first()
    if product:
        sku = product.get('sku')
        name = product.get('name')
    else:
        return None, None
    images = Image.objects.filter(name=name).values_list('image_url', flat=True)
    category = Category.objects.filter(name=name).values_list('category', flat=True)
    return product,images,category