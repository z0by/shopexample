# -*- coding: utf-8 -*-
import operator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category, ProductImage, ProductReview,Characteristic
from django.db.models import Q
import simplejson as json
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse
from django.http import JsonResponse
from filter import product_filter
from utils import get_im_source,get_im_20, get_im_30

def all(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'products/all.html', context)


def index_view(request):
    template_name = "index.html"

    new_products = Product.objects.all().filter(is_active=True).order_by('-created_at')[:6]
    for p in new_products:
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    best_products = Product.objects.all().filter(is_active=True).order_by('-average_review')[:6]
    for p in best_products:
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    sale_products = Product.objects.all().filter(is_active=True)
    result = {}
    for product in sale_products:
        if product.old_price:
            if product.price < product.old_price:
                diff = product.old_price - product.price
                result[product.id] = diff

    result = sorted(result.items(), key=lambda (k, v): v,reverse=True)
    sale_products = []
    for key,value in result:
        p = Product.objects.get(id = key)
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
        sale_products.append(p)
    request.breadcrumbs('Главная', request.path_info)
    context = {'new_products': new_products, 'best_products': best_products, 'sale_products':sale_products}
    return render(request, template_name, context)


def change_view(request):
    if request.method == "GET":
        request.session['view'] = request.GET['view']
        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def sort_view(request):
    if request.method == "GET":
        request.session['sort_view'] = request.GET['sort_view']
        return HttpResponse('ok', content_type='text/html')
    else:
        return HttpResponse('no', content_type='text/html')


def search(request):
    template_name = "products/category.html"
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).filter(is_active=True)

    for p in products:
        descipriton_small = p.description.split(' ')
        if descipriton_small > 30:
            p.descipriton_small = ' '.join(descipriton_small[:30]) + ' ...'
        else:
            p.descipriton_small = ' '.join(descipriton_small)
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)

    if request.is_ajax():
        results = []
        for p in products:
            product_json = {}
            product_json['id'] = p.id
            product_json['title'] = p.title
            product_json['description'] = p.description
            product_json['price'] = p.price
            product_json['url'] = p.get_absolute_url()
            results.append(product_json)
            data = json.dumps(results)
        return JsonResponse(data, safe=False)

    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products, }
    return render(request, template_name, context)

def new_products(request):
    template_name = "products/category.html"

    new_products = Product.objects.all().order_by('-created_at')
    (new_products, features_dict, get_dict, get_valuelist,get_keylist) = product_filter(request,new_products)
    for p in new_products:
        descipriton_small = p.description.split(' ')
        if descipriton_small > 30:
            p.descipriton_small = ' '.join(descipriton_small[:30]) + ' ...'
        else:
            p.descipriton_small = ' '.join(descipriton_small)
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    paginator = Paginator(new_products, 12)
    page = request.GET.get('page')
    try:
        new_products = paginator.page(page)
    except PageNotAnInteger:
        new_products = paginator.page(1)
    except EmptyPage:
        new_products = paginator.page(paginator.num_pages)
    request.breadcrumbs([
        (('Главная'), '/'),
        (('Каталог'), '/products/catalog'),
        (('Новинки'),'%s' % (request.path_info)),
    ])
    context = {'products': new_products,'features_dict':features_dict, 'get_dict':get_dict,
               'get_valuelist':get_valuelist,'get_keylist':get_keylist}
    return render(request, template_name, context)

def catalog(request):
    template_name = "products/category.html"

    catalog_products = Product.objects.all().filter(is_active=True)
    (catalog_products, features_dict, get_dict, get_valuelist,get_keylist) = product_filter(request,catalog_products)
    for p in catalog_products:
        descipriton_small = p.description.split('.')
        if descipriton_small > 30:
            p.descipriton_small = ' '.join(descipriton_small[:30]) + ' ...'
        else:
            p.descipriton_small = ' '.join(descipriton_small)
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    paginator = Paginator(catalog_products, 12)
    page = request.GET.get('page')
    try:
        catalog_products = paginator.page(page)
    except PageNotAnInteger:
        catalog_products = paginator.page(1)
    except EmptyPage:
        catalog_products = paginator.page(paginator.num_pages)
    request.breadcrumbs([
        (('Главная'), '/'),
        (('Каталог'), '/products/catalog'),
         ])
    context = {'products': catalog_products,'features_dict':features_dict, 'get_dict':get_dict,
               'get_valuelist':get_valuelist,'get_keylist':get_keylist}
    return render(request, template_name, context)

def sale_products(request):
    template_name = "products/category.html"

    sale_products = Product.objects.all().filter(is_active=True)

    result = {}
    for product in sale_products:
        if product.old_price:
            if product.price < product.old_price:
                diff = product.old_price - product.price
                result[product.id] = diff

    result = sorted(result.items(), key=lambda (k, v): v,reverse=True)
    sale_products = []
    for key,value in result:
        p = Product.objects.get(id = key)
        sale_products.append(p)
    (sale_products, features_dict, get_dict, get_valuelist,get_keylist) = product_filter(request,sale_products)
    for p  in sale_products:
        descipriton_small = p.description.split(' ')
        if descipriton_small > 30:
            p.descipriton_small = ' '.join(descipriton_small[:30]) + ' ...'
        else:
            p.descipriton_small = ' '.join(descipriton_small)
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    paginator = Paginator(sale_products, 12)
    page = request.GET.get('page')
    try:
        sale_products = paginator.page(page)
    except PageNotAnInteger:
        sale_products = paginator.page(1)
    except EmptyPage:
        sale_products = paginator.page(paginator.num_pages)
    request.breadcrumbs([
        (('Главная'), '/'),
        (('Каталог'), '/products/catalog'),
        (('Скидки'),'%s' % (request.path_info)),
    ])
    context = {'products': sale_products,'features_dict':features_dict, 'get_dict':get_dict,
               'get_valuelist':get_valuelist,'get_keylist':get_keylist}
    return render(request, template_name, context)

def category_view(request, category_slug):
    template_name = "products/category.html"
    category = get_object_or_404(Category.active, slug=category_slug)
    products = Product.objects.filter(categories=category,is_active=True)

    request.session.get('view', 'grid')
    sort_view = request.session.get('sort_view', '')
    if sort_view == 'price_l':
        products = products.order_by('-price')
    elif sort_view == 'price_h':
        products = products.order_by('price')
    images = []
    (products, features_dict, get_dict, get_valuelist,get_keylist) = product_filter(request,products)
    for p in products:
        descipriton_small = p.description.split(' ')
        if descipriton_small > 30:
            p.descipriton_small = ' '.join(descipriton_small[:30]) + ' ...'
        else:
            p.descipriton_small = ' '.join(descipriton_small)
        print p.descipriton_small
        p.image_url = get_im_source(p)
        p.image_20 = get_im_20(p)
        p.image_30 = get_im_30(p)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:

        products = paginator.page(paginator.num_pages)
    request.breadcrumbs([
        (('Главная'), '/'),
        (('Каталог'), '/products/catalog'),
        (('%s') % ((category.title)), '%s' % (request.path_info)),
    ])

    context = {'category': category, 'products': products, 'images': images,
               'category_slug': category_slug, 'features_dict':features_dict, 'get_dict':get_dict,
               'get_valuelist':get_valuelist,'get_keylist':get_keylist}
    return render(request, template_name, context)


def product_view(request, brand_slug, product_slug, id):
    template_name = "products/product_detail.html"
    product = get_object_or_404(Product.active, id=id)
    reviews = ProductReview.objects.filter(product=product)
    features = product.characteristic_set.all().select_related()
    try:
        product.image_url = ProductImage.objects.get(product=product).url
    except Exception:
        product.image_url = "/media/images/350_260.png"
    reviewexist = False
    if request.user.is_authenticated():

        if ProductReview.objects.filter(user=request.user, product=product).exists():
            reviewexist = True

    context = {'product': product, 'reviews': reviews, 'reviewexist': reviewexist,'features':features}
    return render(request, template_name, context)


@login_required(login_url='/accounts/login/')
def product_review(request):
    id = request.GET.get('id')
    next = request.GET.get('next')
    product = get_object_or_404(Product.active, id=id)

    user = request.user

    if request.POST:
        form = ReviewForm(request.POST)

    if form.is_valid():
        score = form.cleaned_data['score']
        review = form.cleaned_data['review']
        if not ProductReview.objects.filter(user=user, product=product).exists():
            productreview = ProductReview.objects.create(user=user, product=product, score=score, review=review)
        else:
            print('gafgafg')

    print request.GET
    print request.POST
    return HttpResponseRedirect(next)
