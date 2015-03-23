
#Container for elements of a category as fetched from Eventbrite
class category_container:

    counter = 0
        
    resource_uri = ''
    id = 0
    name = ''
    name_localized = ''
    short_name = ''
    short_name_localized = ''


    def __init__(self):
        category_container.counter = category_container.counter + 1


#Container for elements of an event as fetched from Eventbrite
class event_container:

    counter = 0   
     
    resource_uri = ''
    id = 0
    name = ''
    description = ''
    url = ''


    def __init__(self):
        event_container.counter = event_container.counter + 1
