from django import forms
import urllib, urllib2, json

from containers import category_container

def get_categories():
    url_for_cat = 'https://www.eventbriteapi.com/v3/categories/?token=BKKRDKVUVRC5WG4HAVLT'
    #categories = ['a','b','c']
    
    f = urllib2.urlopen(url_for_cat) 

    json_string = f.read() 

    parsed_json = json.loads(json_string) 
    
    categories = parsed_json['categories']
    
    catarray = []
    
    for i in categories:
        catarray.append(category_container())
        
        catarray[-1].name = i['name']
        catarray[-1].id = i['id']
        catarray[-1].resource_uri = i['resource_uri']
        catarray[-1].name_localized = i['name_localized']
        catarray[-1].short_name = i['short_name']
        catarray[-1].short_name_localized = i['short_name_localized']
        
        #catnames.append(i['name'])
        #catids.append(i['id'])    
    
    #return dict(categories=categories)
    return catarray


class CategoryForm(forms.Form):
    
    categories = get_categories()
    
    category_name_list = []
    
    for i in categories:
        category_name_list.append((i.id,i.name))

    #category_name_list = ['a','b','c']
    field0 = forms.ChoiceField(required=True, choices=category_name_list)
    field1 = forms.ChoiceField(required=True, choices=category_name_list)
    field2 = forms.ChoiceField(required=True, choices=category_name_list)
