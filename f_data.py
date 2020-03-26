'''
# # Class objects
# * User
#   * Username (string)
#   * sub (string, user id from Google) 
# * Dinner 
#   * Time (time)
#   * Available Seats (int)
#   * Name (string)
#   * Available (bool)
#   * Image (string)
#   * Cost (double)
#   * Ingredients (array of strings)
#   * Food Type (string)
#   * Address (string)
#   * Lat (double)
#   * Long (double)
# * Food (extends Dinner) (all properties are in dinner, but time and available_seats)
#   * *Name (string)*
#   * *Available (bool)*
#   * *Image (string)*
#   * *Cost (double)*
#   * *Ingredients (array of strings)*
#   * *Food Type (string)*
#   * *Address (string)*
#   * *Lat (double)*
#   * *Long (double)*
'''
# content for data.py

# TODO: needs type checking

class User(object):
    def __init__(self, username, sub):
        self.username = username
        self.sub = sub

    def to_dict(self):
        return {
            'username': self.username,
            'sub': self.sub,
	}

class Dinner(object):
    def __init__(self, code, name='', cost=0.00, available=False, 
                image='../icons/hamburger.png', food_type='', 
                ingredients=None, address=None, phone_number=None, available_seats=0,time=''):
        self.code = code
        self.name = name
        self.cost = cost
        self.available = available
        self.image = image
        self.food_type = food_type
        self.ingredients = ingredients
        self.phone_number = phone_number
        self.available_seats = available_seats
        self.time = time

    def to_dict(self):
        return {
            'code': self.code,
            'name': self.name,
            'cost': self.cost,
            'available': self.available,
            'image': self.image,
            'food_type': self.food_type,
            'ingredients': self.ingredients,
            'phone_number': self.phone_number,
            'available_seats': self.available_seats,
            'time': self.time
       }

class Food(Dinner):
    def __init__(self, code, name='', cost=0.00, available=False, 
                image='../icons/hamburger.png', food_type='', 
                ingredients=None, address=None, phone_number=None):
        self.code = code
        self.name = name
        self.cost = cost
        self.available = available
        self.image = image
        self.food_type = food_type
        self.ingredients = ingredients
        self.address = address
        self.phone_number = phone_number

    def to_dict(self):
        return {
	    'code': self.code,
            'name': self.name,
            'cost': self.cost,
            'available': self.available,
            'image': self.image,
            'food_type': self.food_type,
            'ingredients': self.ingredients,
            'address': self.address,
            'phone_number': self.phone_number
       }

class Location(object):
    def __init__(self, address, lat, long, accuracy):
        self.address = address
        self.lat = lat
        self.long = long
        self.accuracy = accuracy

    def to_dict(self):
        return {
            'address': self.address,
            'latitude': self.lat,
            'longitude': self.long,
            'accuracy': self.accuracy
       }
