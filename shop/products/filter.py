# -*- coding: utf-8 -*-
import operator
from django.db.models import Q
from models import Product

def product_filter(request, products):
    features_dict = {}
    features_dict_new = {}
    for p in products:
        features = p.characteristic_set.all().select_related()
        for feature in features:
            values = features_dict.get(feature.characteristic_type, [])
            if feature.value not in values:
                features_dict[feature.characteristic_type] = values + [feature.value]
                features_dict_new[feature.characteristic_type.slug] = values + [feature.value]



    get_dict = {}
    get_valuelist = []
    for key in request.GET.iterkeys():
        valuelist = request.GET.getlist(key)
        get_dict[key] = valuelist
        get_valuelist.extend(valuelist)
    get_keylist = list(request.GET.iterkeys())

    result_dict = {}
    if get_dict:

        for key,value in get_dict.iteritems():

            if key in features_dict_new.keys():
                for v in value:
                    if v in features_dict_new[key]:
                        values = result_dict.get(key, [])
                        if v not in values:
                            result_dict[key] = values + [v]


    q = []
    M = ['characteristic__characteristic_type__slug','characteristic__value']
    for key in result_dict.keys():
        print key
        predicates1 = []
        predicates2 = []
        predicates1.append((M[0],key))
        for v in result_dict[key]:


            predicates2.append((M[1],v))
        q_list1 = [Q(x) for x in predicates1]

        q_list2 = [Q(x) for x in predicates2]

        q_object1 = reduce(operator.and_, q_list1)
        q_object2 = reduce(operator.or_, q_list2)

        q.append(q_object1)
        q.append(q_object2)



    products = Product.objects.filter(pk__in=[x.pk for x in products])
    for el in q:

        products = products.filter(el)
    return (products, features_dict, get_dict, get_valuelist,get_keylist)