# 1520 - Project

## To do

### Notes for team members:
* Alexis - next mini-goal: figuring out how to work with the Google Maps API, so we can develop Location data object further
* Lydia - type checking for data that goes into datastore
* Vicky - mini-goal: create a functioning login
* Naina - N/A

### Highest Priority
  * [ ] Review this example: https://github.com/timothyrjames/cs1520/tree/master/week06/gae/project9
	* [ ] Lydia
	* [x] Vicky
	* [ ] Naina
	* [x] Alexis

### High priority
* [x] set up github, invite people 
* [ ] HTML 
  * [ ] create a template for an eating list
	* **Random Idea (up for discussion):** 
		* We should use the example from https://github.com/timothyrjames/cs1520/tree/master/week06/gae/project9
		* The URL could look like /eat/<zip_code> or /eat/<city>/<zip_code>
		* The templates are basically populated with data by main.py from the db
	* [x] get available foods from datastore to be added in
	* [ ] get available foods BEAR to address to be loaded from datastore to be added in
  * [ ] create a template for attend list
  * [ ] attend search page into /attend.html
  * [x] host into /host.html
  * [x] create a _base.html template (example: https://github.com/timothyrjames/cs1520/blob/master/week06/gae/project8/templates/_base.html) - low priority
  * [x] homepage into /index.html
  * [x] cook into /cook.html
  
* [ ] CSS into /static/style.css
  * [ ] CSS for the templated /eat-list and /attend-list **list** pages
  * [ ] Maps / Toggle alignment CSS
  * [x] Toggle on/ off CSS of maps
  * [x] homepage/eat - added
  * [x] cook
  * [x] attend
  * [x] host
  * [x] responsive / mobile - breakpoint example in style.css
  * [x] mobile hamburger menu (could be better..)
  * [x] mobile version for /cook and /host pages
  
* [ ] Python
  * [ ] Location tracking: https://docs.google.com/presentation/d/1PqtkPX0WpzH8rFvGO3K5_62FMsdd3ZddKOEs6jNTrew/edit#slide=id.g55dc63046b_2_16
  * [ ] Setting up Location logic... feel like we have a lot to do here...
  * [ ] User authentication backend: https://developers.google.com/identity/sign-in/web/backend-auth
  * [ ] load_foods_by_zip() // maybe we could do by city here too...; up for convo
  * [ ] get_food_code() (i.e., the unique key for food)
  * [ ] Setting up user -> food code association 
    	* [ ] Add association within f_data.py (maybe foodcodes stored in array within user)
    	* [ ] Creating method in main.py with app route
   	* [ ] Get user, and all of their food info from DS
    	* [ ] add a load_user_food() method in f_datastore.py
  * [ ] type checking for f_data.py classes (note: holding off until we know for sure what data types we have...)
  * [ ] type checkig for data that goes into datastore
  * [x] Maps - get API (key is currently in /test2.html)
  * [x] Maps - identify needed values for Location (lat, long, zoom (default we should set some between 15-18, which is like road level)
  * [x] f_datastore.py (check out lmsdatastore.py -> https://github.com/timothyrjames/cs1520/tree/master/week06/gae/project9)
  * [x] Round 1- Routing for URLs
  * [x] User authentication front-end
  * [x] Utility function (show_page()),  for data to appear on pages
  * [x] data classes (rnd 1) - calling this f_data.py (tests: http://bit.ly/1520-classes)... we can rename later
  * [x] load_foods() // filters by available food
  * [x] save_food()
  * [x] food_to_datastore() (view -> controller -> datastore)
  	* [x] adding all in values into to cook form (view + controller updates)
  * Dinner methods to mirror food: // holding off, to keep things in f_datastore.py clean
 	 * [ ] save_dinner() // will mirror save_food()
 	 * [ ] load_dinners() // will mirror load_foods(), no need to write unless we need
 	 * [ ] load_dinner_by_zip() // will mirror load_foods_by_zip()
 	 * [ ] dinner_to_datastore() // should mirror food_to_datastore()
 	 * [ ] get_dinner_code() // should mirror get_food_code()


### Low priority
* [ ] Create team name? (we sticking with A?)
* [ ] Create name
* [ ] Create logo 

## Proposal
* https://docs.google.com/presentation/d/1M7u5HtYC5hsmr09UfqeGXXkwklw4zus43RtJ9VeUGnY/edit#slide=id.g7dce42e085_0_7

## Current Appspot
* https://bit.ly/food--friends
