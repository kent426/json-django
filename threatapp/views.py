from django.shortcuts import render

import json
import ast

import os
from django.conf import settings

import string

from django.http import JsonResponse

from django.views.decorators.cache import never_cache

from datetime import datetime
from datetime import timedelta

@never_cache
def index(request):

     return render(
         request,
         'index.html',
     )


@never_cache
def getmeta(request, periodtype):
    """
    View function for home page of site.
    """
    with open(settings.THREAT_FILE, 'rb') as fh:
    	
    	data = fh.read()
    	#convert from byte data to text
    	text = data.decode('utf-8')
    	# replace Unicode for the single left and right quote characters with the ACSII equivalent
    	text = text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    	#convert whitespace characters(defined in string.whitespace) to a single space
    	text = text.translate(str.maketrans("\t\n\r\x0b\x0c", "     "))


    	#safely evaluate the string to python list
    	list_data = ast.literal_eval(text)
    	print(list_data)

    	cur_date = datetime.now()

    	js_data = []
    	"""
    	determine returned json
    	0(default): for 24 hours
    	1: for 7 days
    	2: for 4 weeks
    	"""
    	if periodtype == "1" :
    		start_week = cur_date - timedelta(7)
    		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_week and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
    	elif periodtype == "2" :
    		start_four_weeks = cur_date - timedelta(28)
    		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_four_weeks and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
    	else:
    		start_today = cur_date - timedelta(1)
    		js_data = list(filter(lambda record: datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') > start_today and datetime.strptime(record["date"], '%b %d, %Y %H:%M:%S') < cur_date, list_data))
    	#print(js_data)
    fh.closed
    return JsonResponse(js_data, safe = False)
