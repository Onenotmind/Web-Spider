# -*- coding: UTF-8 -*-
import simplejson
import json
import re
from django.shortcuts import render
from taobao.models import product
from django.http import HttpResponse
from taobao.models import jd_product
from django.forms.models import model_to_dict
from django.core import serializers
from json import JSONEncoder
import pymongo
from taobao.search import test_search
from taobao.jd import jd_test_search
# Create your views here.

# json_serializer = serializers.get_serializer("json")()
# posts = serializers.serialize('json', product.objects.all()[:5])
# 'priceList' : json.dumps(priceList),

def query_by_city(city1,city2):
	query = {
		'__raw__': {
			'location': {'$in': [re.compile(city1), re.compile(city2)]},
		},
	}
	location_query = product.objects(**query).order_by('-deal')[:5].to_json()
	location_result = {'num':product.objects(**query).count(),'data':location_query}
	return location_result



def products(request):
	if 'target' in request.GET and request.GET['target']:
		target = request.GET['target']
		if target == '淘宝':
			if 'q' in request.GET and request.GET['q']:
				q = request.GET['q']
				test_search(q)
			query_result_zhejiang = query_by_city('浙江','杭州')
			query_result_beijing = query_by_city('北京', '北京')
			query_result_shanghai = query_by_city('上海', '上海')
			query_result_fujian = query_by_city('福建', '厦门')
			query_result_sichuan = query_by_city('四川', '成都')
			query_result_jiangsu = query_by_city('江苏', '南京')
			query_result_chongqing = query_by_city('重庆', '重庆')
			query_result_hubei = query_by_city('湖北', '武汉')
			query_result_shanxi = query_by_city('陕西', '西安')
			query_result_guangdong = query_by_city('广州', '广东')
			return render(request, 'search.html', {
				'location_query_zhejiang': query_result_zhejiang,
				'location_query_beijing': query_result_beijing,
				'location_query_shanghai': query_result_shanghai,
				'location_query_fujian': query_result_fujian,
				'location_query_sichuan': query_result_sichuan,
				'location_query_jiangsu': query_result_jiangsu,
				'location_query_chongqing': query_result_chongqing,
				'location_query_hubei': query_result_hubei,
				'location_query_shanxi': query_result_shanxi,
				'location_query_guangdong': query_result_guangdong,
		})
		else:
			xiaomi = jd_product.objects(shop='小米官方旗舰店').to_json()
			aiguozhe = jd_product.objects(shop='爱国者官方旗舰店').to_json()
			return render(request, 'jd.html', {
				'xiaomi': xiaomi,
				'aiguozhe': aiguozhe
		})


def search_pro(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		print(q)
	return HttpResponse('Please submit a search term.')

def index_init(request):
	return render(request, 'index.html', {})
# query_by_city('浙江','杭州')

# def jd_product(request):
# 	xiaomi = jd_product.objects(shop='小米官方旗舰店').to_json()
# 	aiguozhe= jd_product.objects(shop='爱国者官方旗舰店').to_json()
# 	return render(request, 'jd.html', {
# 		'xiaomi': xiaomi,
# 		'aiguozhe': aiguozhe
# })

