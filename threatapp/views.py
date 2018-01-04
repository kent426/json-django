from django.shortcuts import render

import json

import os
from django.conf import settings




def index(request, periodtype):
    """
    View function for home page of site.
    """
    fh = open(settings.THREAT_FILE)

    x = json.load(fh)

    print(x)

    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'pt':periodtype},
    )
