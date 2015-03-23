

class category_container:

    counter = 0
    indx = None
    
    resource_uri = ''
    id = 0
    name = ''
    name_localized = ''
    short_name = ''
    short_name_localized = ''


    def __init__(self):
        category_container.counter = category_container.counter + 1


class event_container:

    counter = 0
    indx = None
    
    resource_uri = ''
    id = 0
    name = ''
    description = ''
    url = ''


    def __init__(self):
        category_container.counter = category_container.counter + 1
