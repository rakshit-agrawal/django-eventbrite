from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

import urllib2, json

from containers import event_container


from forms import CategoryForm


def index(request):
    """
    This defines the index page. It holds form available at the page. 
    """
    
    # Writing action of form when categories are submitted
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            
            # Fetching the three categories listed by user
            category1 = form.cleaned_data['field0']
            category2 = form.cleaned_data['field1']
            category3 = form.cleaned_data['field2']
            page = 1 #Setting initial search page to 1
            
            redirect_url = 'listings/'+ category1 + '/' + category2 + '/' + category3 + '/' + str(page)

            return HttpResponseRedirect(redirect_url)

    # Action of form otherwise
    else:
        form = CategoryForm()

    return render(request, 'index.html', {'form': form})



def listings(request, category1, category2, category3, page = 1):
    """
    This defines the listing page. 
    It uses input categories to fetch data from Eventbrite service.
    It lists the data on a page with name and URL for now.
    """
 
    # Creating URL for request
    base_url = "https://www.eventbriteapi.com/v3/events/search/"
    token_component = "token=BKKRDKVUVRC5WG4HAVLT" #I had this token in my mail link
    category_component = "categories=" + category1 + ',' + category2 + ',' + category3
    page_component = "page=" + str(page)
    url_without_page = base_url + "?" + token_component + "&" + category_component
    url_complete = url_without_page + "&" + page_component
    
    # GET events from Eventbrite
    f = urllib2.urlopen(url_complete) 
    json_string = f.read() 
    parsed_json = json.loads(json_string) 

    # Parse through JSON
    events = parsed_json['events']
    eventsList = []
    
    for i in events:
        eventsList.append(event_container())
        
        # Parse further through JSON
        eventsList[-1].name = i['name']['text']
        eventsList[-1].id = i['id']
        eventsList[-1].url = i['url']
        try:
            eventsList[-1].description = i['description']['text']
        except:
            eventsList[-1].description = "No description available"
        eventsList[-1].resource_uri = i['resource_uri']
    
        
    listings_url_base = '/topthree/listings/'+ category1 + '/' + category2 + '/' + category3 + '/'
    
    # Pagination
    
    """
    Performing manual pagination instead of Django pagination 
    because GET request for events pulls in paginated data already
    """
    
    next_page = int(page) + 1
    next_page_url = listings_url_base + str(next_page)   
    
    if int(page)>1:
        prev_page = int(page) - 1
        prev_page_url = listings_url_base + str(prev_page)   

    else:
        prev_page = 0
        prev_page_url = "#"
    
    
    # Sending values to template
    
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
    
    
    