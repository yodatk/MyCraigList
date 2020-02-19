import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = "https://sfbay.craigslist.org/search/?query={}"


# Create your views here.
def home(request):
    return render(request, template_name='base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    stuff_for_front_end = {
        'search': search,
    }
    return render(request, 'my_app/new_search.html', stuff_for_front_end)
