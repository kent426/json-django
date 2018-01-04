from django.shortcuts import render

import json
import ast

import os
from django.conf import settings

import string

from django.http import JsonResponse





def index(request, periodtype):
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
    	
    	js_data = json.dumps(list_data)


    fh.closed	
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'pt':periodtype, 'jsdata' : js_data},
    )
