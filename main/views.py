from django.shortcuts import render
from .models import Phone, Product, Category, ProductImage, Specs, Collection, Manufacturer
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.views.generic.list import ListView

phones = Phone.objects.all()
categories = Category.objects.order_by('number')


def home(request):
    products = Product.objects.order_by('-rating')[:4]
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/index.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories})


def contacts(request):
    return render(request, 'main/contacts.html', {'phones': phones, 'categories': categories})


def catalog(request):
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': 'Каталог'})


def currentProduct(request, slug):
    current = Product.objects.get(slug=slug)
    currentImages = ProductImage.objects.filter(product=current)
    currentSpecs = Specs.objects.filter(product=current)
    new = False
    if current.date > timezone.now() - timedelta(14):
        new = True
    return render(request, 'main/product.html', {'current': current, 'currentImages': currentImages, 'currentSpecs': currentSpecs, 'phones': phones, 'categories': categories, 'new': new, 'findCategory': current.category, 'title': f'{current.name} | {current.category.name}'})


def currentCategory(request, slug):
    findCategory = Category.objects.get(slug=slug)
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        category=findCategory).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findCategory.name, 'findCategory': findCategory})


def collections(request, slug):
    findCategory = Category.objects.get(slug=slug)
    collections = Collection.objects.filter(category=findCategory)
    paginator = Paginator(collections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/collections.html', {'page_obj': page_obj, 'phones': phones, 'categories': categories, 'title': f'{findCategory.name} | Коллекции', 'findCategory': findCategory})


def currentCollection(request, slug):
    findCollection = Collection.objects.get(slug=slug)
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        collection=findCollection).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findCollection.name, 'findCollection': findCollection.name})


def sales(request):
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(isOnSale=True).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': 'Акции'})


def currentManufacturer(request, slug):
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    findManufacturer = Manufacturer.objects.get(slug=slug)
    products = Product.objects.filter(manufacturer=findManufacturer).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findManufacturer.name, 'findManufacturer': findManufacturer.name})