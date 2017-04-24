import simplejson
import json
from django.shortcuts import render
from taobao.models import product
from django.core import serializers
# Create your views here.

def products(request):
	context = {}
	context['price'] = 12
	context['sale'] =10
	shop = "shop"
	posts = product.objects.all()[:5]
	priceList = []
	priceList.append(1)
	priceList.append(2)
	priceList.append(3)
	priceList.append(4)
	priceList.append(5)
	price = simplejson.dumps(priceList)
	# json_serializer = serializers.get_serializer("json")()
	# posts = serializers.serialize('json', product.objects.all()[:5])
	post = posts[0].shop
	return render(request, 'index.html', {
	'shop' : shop,
	'posts' : post,
	'priceList' : json.dumps(priceList),
	'price' : price,
    'context' : simplejson.dumps(context)})
