from django.shortcuts import render



def index(request, periodtype):
    """
    View function for home page of site.
    """

    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'pt':periodtype},
    )
