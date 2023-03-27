from django.shortcuts import render
from .models import Phone, Product, Category, ProductImage, Specs, Collection
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator

phones = Phone.objects.all()
categories = Category.objects.all()


def home(request):
    products = Product.objects.order_by('-rating')[:4]
    return render(request, 'main/index.html', {'phones': phones, 'products': products})


def catalog(request):
    products = Product.objects.order_by('-rating')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories})


def currentProduct(request, slug):
    current = Product.objects.get(slug=slug)
    currentImages = ProductImage.objects.filter(product=current)
    currentSpecs = Specs.objects.filter(product=current)
    new = False
    if current.date > timezone.now() - timedelta(14):
        new = True
    return render(request, 'main/product.html', {'current': current, 'currentImages': currentImages, 'currentSpecs': currentSpecs, 'phones': phones, 'categories': categories, 'new': new})


def currentCategory(request, slug):
    findCategory = Category.objects.get(slug=slug)
    products = Product.objects.filter(
        category=findCategory).order_by('-rating')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories})


def collections(request):
    collections = Collection.objects.all()
    paginator = Paginator(collections, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'categories': categories})