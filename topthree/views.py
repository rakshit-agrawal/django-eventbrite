from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

import urllib, urllib2, json

from containers import event_container


from forms import CategoryForm


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            category1 = form.cleaned_data['field0']
            category2 = form.cleaned_data['field1']
            category3 = form.cleaned_data['field2']
            page = 1
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('listings/'+ category1 + '/' + category2 + '/' + category3 + '/' + str(page))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CategoryForm()

    return render(request, 'index.html', {'form': form})



def listings(request, category1, category2, category3, page = 1):
 
    #https://www.eventbriteapi.com/v3/events/search/?token=BKKRDKVUVRC5WG4HAVLT&page=45&categories=110%2C107
    base_url = "https://www.eventbriteapi.com/v3/events/search/"
    token_component = "token=BKKRDKVUVRC5WG4HAVLT"
    category_component = "categories=" + category1 + ',' + category2 + ',' + category3
    page_component = "page=" + str(page)
    url_without_page = base_url + "?" + token_component + "&" + category_component
    url_complete = url_without_page + "&" + page_component
    f = urllib2.urlopen(url_complete) 

    json_string = f.read() 

    parsed_json = json.loads(json_string) 
    
    events = parsed_json['events']

    eventsList = []
    
    for i in events:
        eventsList.append(event_container())
        
        eventsList[-1].name = i['name']['text']
        eventsList[-1].id = i['id']
        eventsList[-1].url = i['url']
        try:
            eventsList[-1].description = i['description']['text']
        except:
             eventsList[-1].description = "No description available"
        eventsList[-1].resource_uri = i['resource_uri']
    
        
    listings_url = '/topthree/listings/'+ category1 + '/' + category2 + '/' + category3 + '/'
    
    
    
    next_page = int(page) + 1
    next_page_url = listings_url + str(next_page)   
    
    if int(page)>1:
        prev_page = int(page) - 1
        prev_page_url = listings_url + str(prev_page)   

    else:
        prev_page = 0
        prev_page_url = "#"
    
    
    template = loader.get_template('listings.html')

    context = RequestContext(request, {
        'eventsList': eventsList,
        'prev_page_url':prev_page_url,
        'next_page_url':next_page_url,
        'prev_page':prev_page,
        'page':page,
        'category1':category1,
        'category2':category2,
        'category3':category3,
    })
    
    return HttpResponse(template.render(context))
    
    
    