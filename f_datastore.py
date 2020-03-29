from google.cloud import datastore

import f_data # the classes we defined

# kind is they type of entity that for the query 
# definition here: https://cloud.google.com/appengine/docs/flexible/go/configuring-datastore-indexes-with-index-yaml
_USER_ENTITY = 'User' 
_FOOD_ENTITY = 'Food'
_DINNER_ENTITY = 'Dinner'

##############################################################
##################### Utility functions ######################
##############################################################

def _get_client():
    """Build a datastore client."""
    # documentation on datastore: https://googleapis.dev/python/datastore/latest/client.html
    # definition: Convenience wrapper for invoking APIs/factories w/ a project.
    return datastore.Client()

def log(msg):
    """Log a simple message."""
    # logging information to Log Viewer
    # here: https://console.cloud.google.com/logs/viewer?resource=gae_app&_ga=2.13944496.640558531.1583523379-933297884.1578420671
    print('datastore: %s' % msg)

def _load_key(client, entity_type, entity_id=None, parent_key=None):
    """Load a datastore key using a particular client, and if known, the ID.
    Note that the ID should be an int - we're allowing datastore to generate
    them in this example."""
    key = None
    if entity_id:
        # client.key is a proxy to google.cloud.datastore.key.Key
        # documentation here: https://googleapis.dev/python/datastore/latest/keys.html#google.cloud.datastore.key.Key
        key = client.key(entity_type, entity_id, parent=parent_key)
    else:
        # this will generate an ID
        key = client.key(entity_type)
    return key # this is an int

def _load_entity(client, entity_type, entity_id, parent_key=None):
    """Load a datstore entity using a particular client, and the ID."""
    key = _load_key(client, entity_type, entity_id, parent_key) # getting our int key here
    entity = client.get(key)
    log('retrieved entity for ' + str(entity_id))
    return entity # this is an Entity object (google.cloud.datastore.entity.Entity) or NoneType
    # documentation here: https://googleapis.dev/python/datastore/latest/entities.html
    # You can the set values on the entity just like you would on any other dictionary. (e.g., lesson_entity['title'] = 'blah')
    # Note: Lesson object's title is defined in lmsdata.py (but not our index.yaml)

# TODO: build this function
# Creates a new Food key for the datastore food item
def get_food_code(phone_number, name):
    return phone_number + '_' + name
    #food code is just the user phone number, underscore, and then the name of their dish

# TODO: build get_dinner_code()
def get_dinner_code(phone_number, name):
    return phone_number + '_' + name
    #food code is just the user phone number, underscore, and then the name of their dish

##############################################################
############ translate entities to python objects ############
##############################################################

def _food_from_entity(food_entity): # input: Entity
    # Translate the Food entity to a regular old Python object.
    code = food_entity.key.name # this is a string version of the key
	
    # food(name='', cost=0.00, available=False, 
    #      image='../icons/hamburger.png', food_type='', 
    #      ingredients=None, address=None)
    
    # parameters for Food object
    name = food_entity['name'] # acessing Entity as a dictionary element to pull out name value (for us to use within our object)
    cost = food_entity['cost']
    available = food_entity['available']
    image = food_entity['image']
    food_type = food_entity['food_type']
    ingredients = food_entity['ingredients']
    address = food_entity['address']
    phone_number = food_entity['phone_number']
    lat = food_entity['lat']
    lng = food_entity['lng']

    log('parameters for object set')
    # creating Python object
    food = f_data.Food(code, name, cost, available, image, food_type, ingredients, address, phone_number, lat, lng) # creating our object
	
    # logging to https://console.cloud.google.com/logs/viewer
    log('built object from food entity: ' + str(code))
	
    return food # returning our python Food object

def _dinner_from_entity(dinner_entity): # input: Entity
    # Translate the Dinner entity to a regular old Python object.
    code = dinner_entity.key.name # this is a string version of the key
    
    # dinner(code, name='', cost=0.00, available=False, 
    #         image='../icons/hamburger.png', food_type='', 
    #         ingredients=None, address=None, available_seats=0,time='')
    
    # parameters for Dinner object
    name = dinner_entity['name'] # acessing Entity as a dictionary element to pull out name value (for us to use within our object)
    cost = dinner_entity['cost']
    available = dinner_entity['available']
    image = dinner_entity['image']
    food_type = dinner_entity['food_type']
    ingredients = dinner_entity['ingredients']
    address = dinner_entity['address']
    phone_number = dinner_entity['phone_number']
    available_seats = dinner_entity['available_seats']
    time = dinner_entity['time']
    lat = dinner_entity['lat']
    lng = dinner_entity['lng']

    # creating Python object
    dinner = f_data.Dinner(code, name, cost, available, 
					   image, food_type, ingredients, 
					   address, phone_number, available_seats, time, lat, lng) # creating our object
	
    # logging to https://console.cloud.google.com/logs/viewer
    log('built object from dinner entity: ' + str(code))
	
    return dinner # returning our python Dinner object

##############################################################
############# Load Python objects from Datastore #############
##############################################################

def load_user(sub):
    """Load a user based on their sub; if no sub then this should return None."""

    client = _get_client() # get the datastore client
    q = client.query(kind=_USER_ENTITY) # prep a query that looks at user entities
    
    # .add_filter('<property>', '<operator>', <value>)
    # Filter the query based on a property name, operator and a value.
    # Documentation: https://googleapis.dev/python/datastore/latest/queries.html#google.cloud.datastore.query.Query.add_filter
    q.add_filter('sub', '=', sub) # must equal sub (i.e., Google's user id) 
    
    for user in q.fetch(): # fetch the information on the user
        # get the information from the datastore (accessing as one accesses a dictionary)
        # use that information as a parameter to insert in our python User object
        # return object
        return f_data.User(user['username'], user['sub']) # get user from datastore, translate to python User object
    return None # if info doesn't exist return None

def load_food(food_code): # inputing the food code to get information from datastore
    # Load a food entity from the datastore, based on the food code.
    log('loading food: ' + str(food_code))
    client = _get_client() # gets you a datastore client
    food_entity = _load_entity(client, _FOOD_ENTITY, food_code) # loads the Entity from the datastore
    log('loaded food: ' + food_code)
    food = _food_from_entity(food_entity) # translated the Entity to a Course python object
    log('we have translated food entity to Python object')
    return food # returns python Food object
	
def load_dinner(dinner_code): # inputing the dinner code to get information from datastore
    # Load a dinner entity from the datastore, based on the dinner code.
    log('loading dinner: ' + str(dinner_code))
    client = _get_client() # gets you a datastore client
    dinner_entity = _load_entity(client, _DINNER_ENTITY, dinner_code) # loads the Entity from the datastore
    log('loaded dinner: ' + dinner_code)
    dinner = _dinner_from_entity(dinner_entity) # translated the Entity to a Course python object
    log('we have translated dinner entity to Python object')
    return dinner # returns python Dinner object

def load_foods(): # TODO: we will want to add [city] or [zip] to add query filters (q.add_filter('zip', '=', zip))
    client = _get_client()
    q = client.query(kind=_FOOD_ENTITY)
    q.add_filter('available', '=', "on") # Filters data by Availablity; Needs to be one equal...  https://googleapis.dev/python/datastore/latest/queries.html#google.cloud.datastore.query.Query.add_filter
    result = []
    for food in q.fetch(): # q.fetch() returns the iterator for the query
        result.append(food)
    return result # returns an array of Entities

# TODO: add load_dinners()

##############################################################
################ Saving entities to datastore ################
##############################################################

def save_user(username, sub):
    """Save the user details to the datastore."""
    client = _get_client() # get datastore client
    entity = datastore.Entity(_load_key(client, _USER_ENTITY, sub)) # load information relating to the entity
    entity['username'] = username
    entity['sub'] = sub
    client.put(entity) # update entity within datastore
		
def save_food(name, cost, available="on", image="", food_type="", ingredients="", address="", phone_number="", lat=0.00, lng=0.00): #Note may need to update later
    code = get_food_code(phone_number, name)
    log('in save_food() have code')
    client = _get_client()
    food = datastore.Entity(client.key(_FOOD_ENTITY, code),
                              exclude_from_indexes=['code'])
    food['name'] = name
    food['cost'] = cost
    food['available'] = available
    food['image'] = image
    food['food_type'] = food_type
    food['ingredients'] = ingredients	
    food['address'] = address
    food['phone_number'] = phone_number
    food['lat'] = lat
    food['lng'] = lng

    client.put(food)
	

def save_dinner(name, cost, available="on", image="", food_type="", ingredients="", address="", phone_number="", available_seats = 0, time="", lat=0.00, lng=0.00): #Note may need to update later
    code = get_dinner_code(phone_number, name)
    log('in save_dinner() have code')
    client = _get_client()
    dinner = datastore.Entity(client.key(_DINNER_ENTITY, code),
                              exclude_from_indexes=['code'])
    dinner['name'] = name
    dinner['cost'] = cost
    dinner['available'] = available
    dinner['image'] = image
    dinner['food_type'] = food_type
    dinner['ingredients'] = ingredients	
    dinner['address'] = address
    dinner['phone_number'] = phone_number
    dinner['available_seats'] = available_seats
    dinner['time'] = time
    dinner['lat'] = lat
    dinner['lng'] = lng

    client.put(dinner)

##############################################################
####################### Testing objects ######################
##############################################################

def create_data():
    """You can use this function to populate the datastore with some basic
    data."""
    client = _get_client() # get a datastore client
    
    """USER"""
    # create a test user 
    entity = datastore.Entity(client.key(_USER_ENTITY, 'blahblahblah'), exclude_from_indexes=[])
    
    # update information
    entity.update({
        'username': 'testuser',
	    'sub':'blahblahblah',
    })

    client.put(entity) # save information to datastore
	
    """FOOD"""
    # create a fake food as an entity, Food01
    entity = datastore.Entity(client.key(_FOOD_ENTITY, 'Food01'),
                              exclude_from_indexes=['code'])
    # add information about Food01
    entity.update({
        #'code': 'Food01', # putting this here makes a code column that isn't created when the user creates food
        'name': 'Pizza',
	    'cost': 10.99,
        'available': True,
        'image': '../static/icons/hamburger.png',
        'food_type': 'Italian',
        'ingredients': ['cheese','pineapple'],
	    'address': 'main street, pa',
    	'phone_number': '1234567890',
        'lat': 0.000,
        'lng': -10.023,
    })
    client.put(entity) # save information to datastore 
	
    """FOOD #2 (to test pulling multiple datastore entities)"""
    # create a fake food as an entity, Food01
    entity = datastore.Entity(client.key(_FOOD_ENTITY, 'Food02'),
                              exclude_from_indexes=['code'])
    # add information about Food01
    entity.update({
        #'code': 'Food02',  # putting this here makes a code column that isn't created when the user creates food
        'name': 'Hamburgers',
	    'cost': 19.99,
        'available': False,
        'image': '../static/icons/hamburger.png',
        'food_type': 'American',
        'ingredients': ['hamburger','lettuce'],
	    'address': 'biddles ave, pa',	    
    	'phone_number': '1234567890',
        'lat': 0.000,
        'lng': -10.023,
    })
    client.put(entity) # save information to datastore 
    
    """Dinner"""	
    # create a fake dinner as an entity, Dinner01
    entity = datastore.Entity(client.key(_DINNER_ENTITY, 'Dinner01'),
                              exclude_from_indexes=['code'])
    # add information about Dinner01
    entity.update({
        #'code': 'Dinner01',    # putting this here makes a code column that isn't created when the user creates food
        'name': 'Yums yums at Sarah\'s',
	    'cost': 12.99,
        'available': True,
        'image': '../static/icons/hamburger.png',
        'food_type': 'Italian',
        'ingredients': ['vegetables','cumin'],
        'available_seats': 5,
        'time': '10:00PM',
	    'address': 'dinner main street, pa',
    	'phone_number': '1234567890',        
        'lat': 0.000,
        'lng': -10.023,
    })
    client.put(entity) # save information to datastore
