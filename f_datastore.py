from google.cloud import datastore

import f_data # the classes we defined

# these entity name values are defined within our index.yaml file as "kind"
# kind is they type of entity that for the query 
# definition here: https://cloud.google.com/appengine/docs/flexible/go/configuring-datastore-indexes-with-index-yaml
_USER_ENTITY = 'User' 
_LOCATION_ENTITY = 'Location'
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

    # creating Python object
    food = f_data.Food(code, name, cost, available, image, fodd_type, ingredients, address) # creating our object
	
    # logging to https://console.cloud.google.com/logs/viewer
    log('built object from food entity: ' + str(code))
	
    return food # returning our python Food object

# TODO: add _dinner_from_entity
# TODO: add _location_from_entity
# TODO: add _user_from_entity (example does not include...)

##############################################################
############# Load Python objects from Datastore #############
##############################################################

def load_food(food_code): # inputing the food code to get information from datastore
    # Load a Food entity from the datastore, based on the course code.
    log('loading food: ' + str(food_code))
    client = _get_client() # gets you a datastore client
    food_entity = _load_entity(client, _FOOD_ENTITY, food_code) # loads the Entity from the datastore
    log('loaded food: ' + food_code)
    food = _food_from_entity(food_entity) # translated the Entity to a Course python object
    return food # returns python Food object
	
def load_user(username, passwordhash): # note: our User object does not contain passwordhash (it's only in datastore)
    """Load a user based on the passwordhash; if the passwordhash doesn't match
    the username, then this should return None."""

    client = _get_client() # get the datastore client
    q = client.query(kind=_USER_ENTITY) # prep a query that looks at user entities
    
    # .add_filter('<property>', '<operator>', <value>)
    # Filter the query based on a property name, operator and a value.
    # Documentation: https://googleapis.dev/python/datastore/latest/queries.html#google.cloud.datastore.query.Query.add_filter
    q.add_filter('username', '=', username) # must equal username 
    q.add_filter('passwordhash', '=', passwordhash) # must equal passwordhash
    
    for user in q.fetch(): # fetch the information on the user
        # get the information from the datastore (accessing as one accesses a dictionary)
        # use that information as a parameter to insert in our python User object
        # return object
        return f_data.User(user['username'], user['email']) 
    return None # if info doesn't exist return None

# TODO: add load_dinner
# TODO: add load_location

##############################################################
################ Saving entities to datastore ################
##############################################################

def save_user(user, passwordhash):
    """Save the user details to the datastore."""
    client = _get_client() # get datastore client
    entity = datastore.Entity(_load_key(client, _USER_ENTITY, user.username)) # load information relating to the entity
    entity['username'] = user.username
    entity['email'] = user.email
    entity['passwordhash'] = passwordhash # this is only accessible within the datastore
    entity['testing_random'] = [] # these are only accessible within the datastore
    client.put(entity) # update entity within datastore

# TODO: add save_sold_food
# TODO: add save_sold_dinner

##############################################################
####################### Testing objects ######################
##############################################################

def create_data():
    """You can use this function to populate the datastore with some basic
    data."""
    client = _get_client() # get a datastore client
    
    """USER"""
    # create a test user 
    entity = datastore.Entity(client.key(_USER_ENTITY, 'testuser'), exclude_from_indexes=[])
    
    # update information
    entity.update({
        'username': 'testuser',
        'passwordhash': '',
        'email': 'test@blah.com',
        'testing_random': [],
    })

    client.put(entity) # save information to datastore
	
    """FOOD"""
    # create a fake food as an entity, Food01
    entity = datastore.Entity(client.key(_FOOD_ENTITY, 'Food01'),
                              exclude_from_indexes=['code'])
    # add information about Food01
    entity.update({
        'code': 'Food01',
        'name': 'Pizza',
	    'cost': 10.99,
        'available': True,
        'image': '../static/icons/hamburger.png',
        'food_type': 'Italian',
        'ingredients': ['cheese','pineapple'],
        'available_seats': None,
        'time': '10:00PM',
    })
    client.put(entity) # save information to datastore 
	
# TODO: create fake dinner entity
# TODO: create fake location entity
