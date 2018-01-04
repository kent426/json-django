from django.shortcuts import render

import json
import ast

import os
from django.conf import settings

import string

from django.http import JsonResponse

from django.views.decorators.cache import never_cache

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
    	# replace Unicode for the single left and right quote characters with the ACSII equivalent
    	text = text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    	#convert whitespace characters to a single space
    	text = text.translate(str.maketrans("\t\n\r\x0b\x0c", "     "))

    	#print(text)
    	# js_str = json.dumps(text)
    	# obj = json.loads(js_str)
    	# print(js_str)

    	#safely evaluate the string to python list
    	list_data = ast.literal_eval(text)


    fh.closed
    return JsonResponse(list_data, safe = False)
    
    # Render the HTML template index.html with the data in the context variable
    # return render(
    #     request,
    #     'index.html',
    #     context={'pt':periodtype, 'data' : obj},
    # )
