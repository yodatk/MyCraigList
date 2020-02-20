import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = "https://sfbay.craigslist.org/search/?query={}"

BASE_IMG_URL = "https://images.craigslist.org/{}_300x300.jpg"


# Create your views here.
def home(request):
    """
    rendering the home page
    :param request: Request param
    :return: rendered page of the home page
    """
    return render(request, template_name='base.html')


def new_search(request):
    """
    fishing the information from craiglist.org according to input search field, and then rendering the search result page
    :param request:     request param
    :return:   rendered search page according to the given input
    """
    search = request.POST.get('search')
    min_price = request.POST.get('min_price').strip()
    max_price = request.POST.get('max_price').strip()
    min_price, max_price = create_filter_if_needed(max_price, min_price)
    models.Search.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings = create_final_postings(post_listings, min_price, max_price)
    stuff_for_front_end = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'TGCraiglist/new_search.html', stuff_for_front_end)


def create_filter_if_needed(max_price, min_price):
    """
    converting max and min fields from the html form to int values if possible.
    if there was an error, or if one of the fields is empty -> it will convert that field to -1
    :param max_price: string of the max field
    :param min_price: string of the min field
    :return: None
    """
    is_converted = False
    try:
        if min_price != "":
            min_price = int(min_price)
        else:
            min_price = -1
        if max_price != "":
            max_price = int(max_price)
        else:
            max_price = -1
        is_converted = True
    except:
        print("Error in conversion")
    if not is_converted:
        min_price = -1
        max_price = -1
    return min_price, max_price


def create_final_postings(post_listings, min, max):
    """
    extracting the wanted information from the raw html objects, to proper tuples of text values to each listing
    :param post_listings:  list of html object (from beautiful soups) to extract data from
    :return:    list of tuples of: (post_title, post_url, post_price, post_image_url) for each listing
    """
    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        is_filter_approved = check_price_filters(post_price, min, max)
        if is_filter_approved:
            if post.find(class_='result-image').get('data-ids'):
                post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                post_image_url = BASE_IMG_URL.format(post_image_id)
            else:
                post_image_url = 'https://craiglist.org/images/peace.jpg'
            final_postings.append((post_title, post_url, post_price, post_image_url))
    return final_postings


def check_price_filters(price, min_price, max_price):
    """
    checks the current listing price is in price range
    :param price: current listing price
    :param min_price: min filter. if -1 there is no filter
    :param max_price: max filter. if -1 there is no filter
    :return: True if the filter values are valid , False otherwise
    """

    if (min_price == -1) and (max_price == -1):
        return True
    elif price == "N/A":
        return False
    else:
        real_price = int(price[1:])
        if (
                ((min_price != -1) and (min_price > real_price)) or  # min condition fail
                ((max_price != -1) and (max_price < real_price))  # max condition fail
        ):
            return False
        else:
            return True
