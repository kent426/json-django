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

from . import myfunc

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
    	text = data.decode('utf-8')

    	text = myfunc.sanitize_text(text)



    	#safely evaluate the string to python list
    	list_data = ast.literal_eval(text)
    	print(list_data)
    	js_data = []
    	"""
    	determine returned json
    	0(default): for 24 hours
    	1: for 7 days
    	2: for 4 weeks
    	"""
    	js_data =  myfunc.filter_by_period(periodtype,list_data)
    	print(js_data)
    fh.closed
    return JsonResponse(js_data, safe = False)
