from flask import Flask, redirect, render_template, Response, request, flash, session, url_for
import json # for backend sign in functionality
from google.oauth2 import id_token # for backend sign in functionality
from google.auth.transport import requests # for backend sign in functionality
from google.cloud import storage # for images
#from flask_wtf import FlaskForm # attempting to add library

import f_data # includes our data classes: User, Dinner, Food, Location
import f_datastore
from forms import FoodRegistrationForm, DinnerRegistrationForm, UploadForm, FlaskForm
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)


# logging to console
def log(msg):
    """Log a simple message."""
    # Look at: https://console.cloud.google.com/logs to see your logs.
    # Make sure you have "stdout" selected.
    print('main: %s' % msg)

@app.route('/success')
def success():
    return show_page('_base.html','Succesfully submitted!','',user=get_user())

# app routing
@app.route('/')
@app.route('/eat')
@app.route('/index.html')
def root():
    file = '/index.html'
    title = 'Food with Friends: Eat up!'
    h1 = 'Eat Leftovers'
    return show_page(file,title,h1,user=get_user())
	
@app.route('/cook', methods=['GET','POST'])
def cook():
    form = FoodRegistrationForm()
    if request.method == 'POST' and form.validate():
        # testing with 3 properties of food
        user = get_user()
        name = request.form.get('fname')
        cost = request.form.get('fcost')
        available = request.form.get('favailable')
        #image = request.form.get('fimage')#commenting out 4/18-AS
        food_type = request.form.get('fcategory')
        ingredients = request.form.get('fingredients')
        address = request.form.get('location')
        phone_number = request.form.get('fphone_number')
        lat = request.form.get('flat')
        lng = request.form.get('flng')
        log('form is valid')
        uploaded_file = request.files.get('file')
        log('uploaded file')
        filename = request.form.get('filename')
        log('got filename')
        content_type = uploaded_file.content_type
        log('got content type')
        if not uploaded_file:
            return 'FILE NOT UPLOADED'
        gcs_client = storage.Client()
        log('got storage client')
        storage_bucket = gcs_client.get_bucket('f_storage')
        log('got f_storage bucket')
        blob = storage_bucket.blob(uploaded_file.filename)
        log('got blob')
        blob.upload_from_string(uploaded_file.read(), content_type=content_type)
        log('uploaded from string')
        url = blob.public_url
        log('got url: ' + url)	
        f_datastore.save_food(user, name, cost, available, url, food_type, ingredients, address, phone_number, lat, lng) # adding to db # url == image
        # f_datastore.save_food(name, cost, available, image, food_type, ingredients, address) # adding to db
        log('loaded food_to_datastore() data')
        flash('Succesfully submitted!', 'success')
        # return 'OK' # TODO: update function to send to page where user's current food items
        return redirect('/activity')

    file = '/cook.html'
    title = 'Cook for Friends'
    h1 = 'Cook'
    return render_template(file, title=title, h1=h1, form=form, user=get_user())

@app.route('/host', methods=['GET','POST'])
def host():
    form = DinnerRegistrationForm()
    if request.method == 'POST' and form.validate():
        # testing with 3 properties of food
        user = get_user()
        name = request.form.get('fname')
        cost = request.form.get('fcost')
        available = request.form.get('favailable_seats')
        image = request.form.get('fname')
        food_type = request.form.get('fcategory')
        ingredients = request.form.get('fingredients')
        address = request.form.get('location')
        time = request.form.get('ftime')
        phone_number = request.form.get('fphone_number')
        available_seats = request.form.get('favailable_seats')
        lat = request.form.get('flat')
        lng = request.form.get('flng')
        f_datastore.save_dinner(user, name, cost, available, image, food_type, ingredients, address, phone_number, available_seats, time, lat, lng) # adding to db
        # f_datastore.save_dinner(name, cost, available, image, food_type, ingredients, address, time) # adding to db
        log('loaded dinner_to_datastore() data')
        flash('Succesfully submitted!', 'success')
        # return 'OK' # TODO: update function to send to page where user's current food items
        return redirect('/activity')

    file = '/cook.html'
    title = 'Host a Dinner & Make Friends'
    h1 = "Host"
    return render_template(file, title=title, h1=h1, form=form, user=get_user())


@app.route('/edit_cook/<food>', methods=['GET','POST'])
def edit_cook(food):
    food_entity = f_datastore.query_food(food)
    form = FoodRegistrationForm(obj=food_entity)
    if request.method == 'POST' and form.validate():
        # testing with 3 properties of food
        user = get_user()
        name = request.form.get('fname')
        cost = request.form.get('fcost')
        available = request.form.get('favailable')
        food_type = request.form.get('fcategory')
        ingredients = request.form.get('fingredients')
        address = request.form.get('location')
        phone_number = request.form.get('fphone_number')
        lat = request.form.get('flat')
        lng = request.form.get('flng')
        if not lat:
            lat = food_entity.get('lat')
            lng = food_entity.get('lng')
        log('form is valid')
        uploaded_file = request.files.get('file')
        log('uploaded file')
        filename = request.form.get('filename')
        log('got filename')
        content_type = uploaded_file.content_type
        log('got content type')
        if uploaded_file:
            gcs_client = storage.Client()
            log('got storage client')
            storage_bucket = gcs_client.get_bucket('f_storage')
            log('got f_storage bucket')
            blob = storage_bucket.blob(uploaded_file.filename)
            log('got blob')
            blob.upload_from_string(uploaded_file.read(), content_type=content_type)
            log('uploaded from string')
            url = blob.public_url
            log('got url: ' + url)	
        else:
            url = food_entity.get('image')
        f_datastore.save_food(user, name, cost, available, url, food_type, ingredients, address, phone_number, lat, lng) # adding to db # url == image
        log('loaded food_to_datastore() data')
        flash('Changes have been applied!', 'success')
        return redirect('/activity')

    form.fname.data = food_entity.get('name')
    form.fcost.data = food_entity.get('cost')
    form.favailable.data = food_entity.get('available')
    form.fcategory.data = food_entity.get('food_type')
    form.fingredients.data = food_entity.get('ingredients')
    form.location.data = food_entity.get('address')
    form.fphone_number.data = food_entity.get('phone_number')
    form.file.data = food_entity.get('image')
    form.flat.data = food_entity.get('lat')
    form.flng.data = food_entity.get('lng')
       
    file = '/cook.html'
    title = 'Cook for Friends'
    h1 = 'Edit Cook'
    return render_template(file, title=title, h1=h1, form=form, user=get_user())


@app.route('/edit_host/<dinner>', methods=['GET','POST'])
def edit_host(dinner):
    form = DinnerRegistrationForm()
    if request.method == 'POST' and form.validate():
        # testing with 3 properties of food
        user = get_user()
        name = request.form.get('fname')
        cost = request.form.get('fcost')
        available = request.form.get('favailable_seats')
        image = request.form.get('fname')
        food_type = request.form.get('fcategory')
        ingredients = request.form.get('fingredients')
        address = request.form.get('location')
        time = request.form.get('ftime')
        phone_number = request.form.get('fphone_number')
        available_seats = request.form.get('favailable_seats')
        lat = request.form.get('flat')
        lng = request.form.get('flng')
        if not lat:
            lat = food_entity.get('lat')
            lng = food_entity.get('lng')
        f_datastore.save_dinner(user, name, cost, available, image, food_type, ingredients, address, phone_number, available_seats, time, lat, lng) # adding to db
        log('loaded dinner_to_datastore() data')
        flash('Succesfully submitted!', 'success')
        return redirect('/activity')

    form.fname.data = food_entity.get('name')
    form.fcost.data = food_entity.get('cost')
    form.favailable.data = food_entity.get('available')
    form.fcategory.data = food_entity.get('food_type')
    form.fingredients.data = food_entity.get('ingredients')
    form.location.data = food_entity.get('address')
    form.fphone_number.data = food_entity.get('phone_number')
    form.file.data = food_entity.get('image')
    form.flat.data = food_entity.get('lat')
    form.flng.data = food_entity.get('lng')
    form.favailable_seats.data = food_entity.get('available_seats')
    form.ftime.data = food_entity.get('time')

    file = '/cook.html'
    title = 'Host a Dinner & Make Friends'
    h1 = "Edit Host"
    return render_template(file, title=title, h1=h1, form=form, user=get_user())


@app.route('/attend')
def attend():
    file = '/attend.html'
    title = 'Attend a Dinner & Make Friends'
    h1 ="Attend"
    return render_template(file, title=title, h1=h1, user=get_user())


@app.route('/eat-list') 
def eatlist():
    food_list = f_datastore.load_foods() # TODO: filter by distance
    return show_page('/eat-list.html','Nearby Leftovers','Nearby Leftovers',foods=food_list, user=get_user()) 


# utility function that allows us to 
# consolidate on the render_template function
# will allow us to expand on parameters, as week04/gae/project2/main
# start to get user, location, food, and dinner data
def show_page(page, title, h1, user=None,
			  food=None, foods=None, dinner=None, dinners=None, errors=None):
	return render_template(page, 
			       page_title=title, #on-page = parameter
			       h1=h1,
			       user=user,
			       food=food,
			       foods=foods,
			       dinner=dinner,
			       dinners=dinners,
			       errors=errors)


# We should only use this to populate our data for the first time.
@app.route('/createdata')
def createdata():
    f_datastore.create_data()
    return 'OK'


# backend sign in functionality	
@app.route('/tokensignin', methods=['POST'])
def authtoken():
    log('in contoller')
    token = request.form.get('idtoken')
    log('Received token by HTTPS POST: ' + token)
    given_name = request.form.get('username')
    log('Received given name by HTTPS POST: ' + given_name)
    CLIENT_ID = '1024466557558-monvg7ism1u12feg47r8296nh44bq500.apps.googleusercontent.com'
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        log('ID token is valid.')
        userid = idinfo['sub']
        session['user'] = userid
        log('Got the user\'s Google Account ID from the decoded token')
        f_datastore.save_user(given_name, userid)
    except ValueError:
        log('ID is not valid, in Error')
        pass
    return redirect('/')


@app.route('/activity', methods=['GET','POST'])
def activity():
    edit = request.form.get('edit')
    if edit is not None:
        return redirect(url_for('edit_cook', food=edit))
    delete = request.form.get('delete')
    if delete is not None:
        f_datastore.delete_food(delete)
    file = '/activity.html'
    title = 'Attend a Dinner & Make Friends'
    h1 ="My Foods"
    user = get_user()
    food_list = f_datastore.query_food_list(user)
    form = FlaskForm()
    return render_template(file, title=title, h1=h1, food_list=food_list, form=form, user=get_user())


@app.route('/logout')
def logout():
    session['user'] = None
    return redirect('/')

def get_user():
    return session.get('user', None)

##############################Test goes below this line vvvvvvvvvv

@app.route('/test') 
def test():
    f_datastore.save_food('Blue Slurpie', 1213.99) # adding to db
    log('saved food!')   
    food_code = 'Food01'
    dinner_code = 'Dinner01'
    username = 'testuser'
    sub = 'blahblahblah'
    food = f_datastore.load_food(food_code)
    log('loaded food: ' + food_code)
    dinner = f_datastore.load_dinner(dinner_code)
    log('loaded dinner: ' + dinner_code)
    user = f_datastore.load_user(sub)
    log('loaded user: ' + sub)
    food_list = f_datastore.load_foods()
    log('loaded food list!')
    return show_page('/test.html','title here','h1 here', user=user, food=food, foods=food_list, dinner=dinner)

@app.route('/test2')
def test_two():
    return show_page('/test2.html','Testing Maps API', 'Maps API Testing')

@app.route('/upload', methods=['GET','POST'])
def test_three():
    log('test3 loaded')
    form = UploadForm()
    log('form good')
    if request.method == 'POST':
        log('in post for test3')
        if form.validate_on_submit():
            log('form is valid')
            uploaded_file = request.files.get('file')
            log('uploaded file')
            filename = request.form.get('filename')
            log('got filename')
            content_type = uploaded_file.content_type
            log('got content type')
            if not uploaded_file:
                return 'FILE NOT UPLOADED'
            gcs_client = storage.Client()
            log('got storage client')
            storage_bucket = gcs_client.get_bucket('f_storage')
            log('got f_storage bucket')
            blob = storage_bucket.blob(uploaded_file.filename)
            log('got blob')
            blob.upload_from_string(uploaded_file.read(), content_type=content_type)
            log('uploaded from string')
            url = blob.public_url
            log('got url: ' + url)
            return 'OK'
        return 'OK - in POST'
    file = '/test3.html'
    title = 'Test3 - images'
    h1 = 'Test3 - images'
    return render_template(file, title=title, h1=h1, form=form)


@app.route('/test-post', methods=['POST'])
def latlongtest():
    lat = request.form.get('lat')
    long = request.form.get('long')
    log('lat=' + lat)
    log('long=' + long)
    return 'Lat/long recieved'

@app.route('/cookvalues', methods=['GET','POST'])
def food_to_datastore():
    # testing with 3 properties of food
    name = request.form.get('fname')
    cost = request.form.get('fcost')
    available = request.form.get('favailable')
    image = request.form.get('fimage')
    food_type = request.form.get('fcategory')
    ingredients = request.form.get('fingredients')
    address = request.form.get('autocomplete')
    phone_number = request.form.get('fphone_number')
    lat = request.form.get('flat')
    lng = request.form.get('flng')
    f_datastore.save_food(name, cost, available, image, food_type, ingredients, address, phone_number, lat, lng) # adding to db
    log('loaded food_to_datastore() data')
    return 'OK' # TODO: update function to send to page where user's current food items

@app.route('/hostvalues', methods=['POST'])
def dinner_to_datastore():
    # testing with 3 properties of food
    name = request.form.get('dname')
    cost = request.form.get('dcost')
    available = request.form.get('davailable')
    image = request.form.get('dimage')
    food_type = request.form.get('dcategory')
    ingredients = request.form.get('dingredients')
    address = request.form.get('autocomplete')
    phone_number = request.form.get('dphone_number')
    available_seats = request.form.get('davailable_seats')
    time = request.form.get('dtime')
    lat = request.form.get('dlat')
    lng = request.form.get('dlng')
    f_datastore.save_dinner(name, cost, available, image, food_type, ingredients, address, phone_number, available_seats, time, lat, lng) # adding to db
    log('loaded dinner_to_datastore() data')
    return 'OK' # TODO: update function to send to page where user's current food items

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8082, debug=True) # updated port, so that when it runs locally, it runs on 8030
