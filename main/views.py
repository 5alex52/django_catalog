from django.shortcuts import render, redirect
from .models import Phone, Product, Category, ProductImage, Specs, Collection, Manufacturer, Address
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse, HttpRequest
from .forms import AddFeedbackForm
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.core.cache import cache

categories = Category.objects.order_by('number')


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def home(request):
    products = Product.objects.order_by(
        '-rating')[:4].select_related('manufacturer', 'collection').only('name', 'mainImage', 'date', 'isOnSale', 'price', 'slug', 'rating', 'manufacturer__name', 'collection__name')
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    content = {'phones': phones,
               'products': products,
               'new': new,
               'categories': categories,
               'address': address
               }
    return render(request, 'main/index.html', content)


@cache_page(60 * 60 * 12)
@require_GET
def contacts(request):
    phones = Phone.objects.all()
    address = Address.objects.order_by('pk')
    return render(request, 'main/contacts.html', {'phones': phones, 'categories': categories, 'address': address})


@require_GET
def catalog(request):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.order_by(
        ordering).select_related('manufacturer', 'collection').only('name', 'mainImage', 'date', 'isOnSale', 'price', 'slug', 'rating', 'manufacturer__name', 'collection__name')
    paginator = Paginator(products, 12)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'new': new,
               'categories': categories,
               'title': 'Каталог',
               'address': address
               }

    return render(request, 'main/catalog.html', content)


def currentProduct(request, slug):
    isFeedback = 'false'
    feedback_title = ''
    feedback_message = ''
    icon = ''
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    try:
        current = Product.objects.select_related(
            'manufacturer', 'collection').get(slug=slug)
    except Product.DoesNotExist:
        return tr_handler404(request, 'Error')
    currentImages = ProductImage.objects.filter(product=current)
    currentSpecs = Specs.objects.filter(product=current)
    new = False
    if current.date > timezone.now() - timedelta(14):
        new = True
    if request.method == 'POST':
        isFeedback = 'true'
        form = AddFeedbackForm(request.POST)
        if form.is_valid():
            product = Product.objects.get(slug=slug)
            form.instance.product = product
            form.instance.product_name = product.name
            form.instance.link = request.build_absolute_uri(product.get_absolute_url())
            form.instance.date = timezone.now()
            form.save()
            feedback_title = 'Заявка отправлена'
            feedback_message = 'Наш менеджер перезвонит вам.'
            icon = 'success'
            form = AddFeedbackForm()
        else:
            feedback_title = 'Ошибка'
            feedback_message = 'Пожалуйста, заполните все поля'
            icon = 'error'
    else:
        form = AddFeedbackForm()

    content = {'current': current,
               'currentImages': currentImages,
               'currentSpecs': currentSpecs,
               'phones': phones,
               'categories': categories,
               'new': new,
               'findCategory': current.category,
               'title': f'{current.name} | {current.category.name}',
               'address': address, 'feedback': form,
               'isFeedback': isFeedback,
               'feedback_title': feedback_title,
               'feedback_message': feedback_message,
               'icon': icon,
               }

    return render(request, 'main/product.html', content)


@require_GET
def currentCategory(request, slug):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    try:
        findCategory = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return tr_handler404(request, 'Error')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        category=findCategory).order_by(ordering).select_related('manufacturer', 'collection')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'new': new,
               'categories': categories,
               'title': findCategory.name,
               'findCategory': findCategory,
               'address': address
               }

    return render(request, 'main/catalog.html', content)


@require_GET
def collections(request, slug):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    try:
        findCategory = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return tr_handler404(request, 'Error')
    collections = Collection.objects.filter(category=findCategory)
    paginator = Paginator(collections, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'categories': categories,
               'title': f'{findCategory.name} | Коллекции',
               'findCategory': findCategory,
               'address': address
               }

    return render(request, 'main/collections.html', content)


@require_GET
def currentCollection(request, slug):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    try:
        findCollection = Collection.objects.get(slug=slug)
    except Collection.DoesNotExist:
        return tr_handler404(request, 'Error')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        collection=findCollection).order_by(ordering).select_related('manufacturer', 'collection')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'new': new,
               'categories': categories,
               'title': findCollection.name,
               'findCollection': findCollection.name,
               'address': address
               }

    return render(request, 'main/catalog.html', content)


@require_GET
def currentCollectionFromCategory(request, slug, slug2):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    try:
        findCollection = Collection.objects.get(slug=slug2)
    except Collection.DoesNotExist:
        return tr_handler404(request, 'Error')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(
        collection=findCollection).filter(collectionCategory__slug=slug).order_by(ordering).select_related('manufacturer', 'collection')
    try:
        findCategory = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return tr_handler404(request, 'Error')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'new': new,
               'categories': categories,
               'title': findCollection.name,
               'findCollection': findCollection.name,
               'findCategory': findCategory,
               'address': address
               }

    return render(request, 'main/catalog.html', content)


@require_GET
def sales(request):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    products = Product.objects.filter(isOnSale=True).order_by(
        ordering).select_related('manufacturer', 'collection').only('name', 'mainImage', 'date', 'isOnSale', 'price', 'slug', 'rating', 'manufacturer__name', 'collection__name')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj,
               'phones': phones,
               'new': new,
               'categories': categories,
               'title': 'Акции',
               'address': address
               }

    return render(request, 'main/catalog.html', content)


@require_GET
def currentManufacturer(request, slug):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    ordering = request.GET.get('orderby')
    if not ordering:
        ordering = '-rating'
    findManufacturer = Manufacturer.objects.get(slug=slug)
    products = Product.objects.filter(
        manufacturer=findManufacturer).order_by(ordering).select_related('manufacturer', 'collection')
    paginator = Paginator(products, 16)
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {'page_obj': page_obj, 
               'phones': phones, 
               'new': new, 
               'categories': categories,
               'title': findManufacturer.name, 
               'findManufacturer': findManufacturer.name, 
               'address': address
               }

    return render(request, 'main/catalog.html', content)


def searchHendler(request):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    ordering = request.GET.get('orderby')
    search = request.GET.get('search')
    if not ordering:
        ordering = '-rating'
    if search:
        products = Product.objects.filter(Q(name__icontains=search) | Q(manufacturer__name__icontains=search) | Q(
            collection__name__icontains=search) | Q(category__name__icontains=search)).order_by(ordering).select_related('manufacturer', 'collection')
    else:
        products = Product.objects.none()

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


@require_GET
def tr_handler404(request, *args, **kwargs):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    products = Product.objects.order_by(
        '-rating')[:4].select_related('manufacturer', 'collection')
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/error.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories, 'address': address, 'title': '404', 'message': 'К сожалению, такой мебели мы не нашли : (', 'message2': 'Посмотрите другие наши товары:'}, status=404)


@require_GET
def tr_handler505(request):
    phones = Phone.objects.all().select_related('store')
    address = Address.objects.order_by('pk')
    products = Product.objects.order_by(
        '-rating')[:4].select_related('manufacturer', 'collection')
    new = {}
    for x in products:
        if x.date > timezone.now() - timedelta(14):
            new[x.name] = True
        else:
            new[x.name] = False

    return render(request, 'main/error.html', {'phones': phones, 'products': products, 'new': new, 'categories': categories, 'address': address, 'title': '505', 'message': 'Наш программист накосячил', 'message2': 'Пожалуйста посмотрите другие товары в каталоге, а он исправит ошибку : )'}, status=505)
