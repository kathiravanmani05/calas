from django.shortcuts import render
from shop.extraction.data_extraction import fetch_categories,fetch_products,fetch_product_detail,search_product
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, Product

def index(request):
    categorys = fetch_categories()

    return render(request, 'index.html',{'categorys':categorys})

def category_view(request, category,page=1):
    products = fetch_products(category)
    total_products = len(products)
    page = request.GET.get('page', 1)
    page_count = 16
    paginator = Paginator(products, 16)
    try:
        items = paginator.page(page)
        page_count = len(items)
    except PageNotAnInteger:
        items = paginator.page(1)
        page_count = len(items)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, 'category.html',{'products':items,'page':items,'page_count':page_count,'total_products':total_products,'category':category})

def product_detail(request, category,name):
    product,images,Categories = fetch_product_detail(name)
    return render(request, 'product_detail.html',{'product':product,'images':images,'Categories':Categories,'category':category})

def search(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        product, images, category = search_product(query)
        if product :
            return render(request, 'product_detail.html', {'product': product, 'images': images, 'Categories':category})
    
    categorys = fetch_categories()
    return render(request, 'index.html', {'categorys': categorys})