from __future__ import unicode_literals

from django.db import models

from mongoengine import *

connect('taobao')

# Create your models here.

class product(Document):
	shop = StringField()
	deal = StringField()
	title = StringField()
	image = StringField()
	location = StringField()
	price = StringField()

# for e in product.objects.all():
# 	print e['shop']

