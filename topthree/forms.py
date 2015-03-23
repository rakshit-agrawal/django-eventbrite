from django import forms
import urllib, urllib2, json

from containers import category_container

def get_categories():
    """
    This function fetches the list of categories from Eventbrite.
    """
    base_url = "https://www.eventbriteapi.com/v3/categories/" 
    token_component = "token=BKKRDKVUVRC5WG4HAVLT" #I had this token in my mail link
    url_complete = base_url + '?' + token_component
    
    # GET categories
    f = urllib2.urlopen(url_complete) 
    json_string = f.read() 
    parsed_json = json.loads(json_string) 
    
    # Parse through JSON
    categories = parsed_json['categories']
    
    category_array = []
    
    for i in categories:
        category_array.append(category_container())
        
        category_array[-1].name = i['name']
        category_array[-1].id = i['id']
        category_array[-1].resource_uri = i['resource_uri']
        category_array[-1].name_localized = i['name_localized']
        category_array[-1].short_name = i['short_name']
        category_array[-1].short_name_localized = i['short_name_localized']


    return category_array


class CategoryForm(forms.Form):
    
    """
    Holder form for category selection. Index page form in this app.
    """
    
    categories = get_categories()
    
    category_name_list = []
    
    for i in categories:
        category_name_list.append((i.id,i.name))

    field0 = forms.ChoiceField(required=True, choices=category_name_list, label="Category 1")
    field1 = forms.ChoiceField(required=True, choices=category_name_list, label="Category 2")
    field2 = forms.ChoiceField(required=True, choices=category_name_list, label="Category 3")
