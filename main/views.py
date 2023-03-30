from django.shortcuts import render
from .models import Phone, Product, Category, ProductImage, Specs, Collection, Manufacturer, Address
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.http import Http404

phones = Phone.objects.all()
categories = Category.objects.order_by('number')
address = Address.objects.order_by('pk')

def home(request):
    products = Product.objects.order_by('-rating')[:4]
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/index.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories, 'address': address})


def contacts(request):
    return render(request, 'main/contacts.html', {'phones': phones, 'categories': categories, 'address': address})


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
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': 'Каталог', 'address': address})


def currentProduct(request, slug):
    current = Product.objects.get(slug=slug)
    currentImages = ProductImage.objects.filter(product=current)
    currentSpecs = Specs.objects.filter(product=current)
    new = False
    if current.date > timezone.now() - timedelta(14):
        new = True
    return render(request, 'main/product.html', {'current': current, 'currentImages': currentImages, 'currentSpecs': currentSpecs, 'phones': phones, 'categories': categories, 'new': new, 'findCategory': current.category, 'title': f'{current.name} | {current.category.name}', 'address': address})


def currentCategory(request, slug):
    try:
        findCategory = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return tr_handler404(request, 'Error')
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

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findCategory.name, 'findCategory': findCategory, 'address': address})


def collections(request, slug):
    findCategory = Category.objects.get(slug=slug)
    collections = Collection.objects.filter(category=findCategory)
    paginator = Paginator(collections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/collections.html', {'page_obj': page_obj, 'phones': phones, 'categories': categories, 'title': f'{findCategory.name} | Коллекции', 'findCategory': findCategory, 'address': address})


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

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findCollection.name, 'findCollection': findCollection.name, 'address': address})


def currentCollectionFromCategory(request, slug, slug2):
    findCollection = Collection.objects.get(slug=slug2)
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        collection=findCollection).filter(collectionCategory__slug=slug).order_by(ordering)
    findCategory = Category.objects.get(slug=slug)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findCollection.name, 'findCollection': findCollection.name, 'findCategory': findCategory, 'address': address})


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
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': 'Акции', 'address': address})


def currentManufacturer(request, slug):
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    findManufacturer = Manufacturer.objects.get(slug=slug)
    products = Product.objects.filter(
        manufacturer=findManufacturer).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': findManufacturer.name, 'findManufacturer': findManufacturer.name, 'address': address})


def searchHendler(request):
    ordering = request.GET.get('orderby')
    search = request.GET.get('search')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(Q(name__icontains=search) | Q(
        manufacturer__name__icontains=search) | Q(collection__name__icontains=search)).order_by(ordering)
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/catalog.html', {'page_obj': page_obj, 'phones': phones, 'new': new, 'categories': categories, 'title': 'Поиск', 'isSearch': True, 'search_data': search, 'address': address})


def tr_handler404(request, exeption):
    products = Product.objects.order_by('-rating')[:4]
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/error.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories, 'address': address, 'title': '404', 'message': 'К сожалению, такой мебели мы не нашли : (', 'message2': 'Посмотрите другие наши товары:'}, status=404)

def tr_handler505(request):
    products = Product.objects.order_by('-rating')[:4]
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/error.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories, 'address': address, 'title': '505', 'message': 'Наш программист накосячил', 'message2': 'Пожалуйста посмотрите другие товары в каталоге, а он исправит ошибку : )'}, status=505)
