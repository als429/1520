# 1520 - Project

## To do

### Notes for team members:
* Alexis - next mini-goal: figuring out how to connect HTML/main.py with the f_datastore
	* HTML uses python object in {{object.property}} with dot operator
	* main.py `show_page()` needs to pass in python object
	* the `load_...()` function in the datastore.py loads object into main.py for the `show_page()` function
* Lydia - N/A
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
	* **Idea:** 
		* We should use the example from https://github.com/timothyrjames/cs1520/tree/master/week06/gae/project9
		* The URL could look like /eat/<zip_code> or /eat/<city>/<zip_code>
		* The templates are basically populated with data by main.py from the db
  * [ ] create a template for attend list
  * [ ] attend search page into /attend.html
  * [x] host into /host.html
  * [x] create a _base.html template (example: https://github.com/timothyrjames/cs1520/blob/master/week06/gae/project8/templates/_base.html) - low priority
  * [x] homepage into /index.html
  * [x] cook into /cook.html
  
* [ ] CSS into /static/style.css
  * [ ] CSS for the templated eat and attend **list** pages
  * [x] homepage/eat - added
  * [x] cook
  * [x] attend
  * [x] host
  * [x] responsive / mobile - breakpoint example in style.css
  * [x] mobile hamburger menu (could be better..)
  * [x] mobile version for /cook and /host pages
  
* [ ] Python
  * [ ] Location tracking: https://docs.google.com/presentation/d/1PqtkPX0WpzH8rFvGO3K5_62FMsdd3ZddKOEs6jNTrew/edit#slide=id.g55dc63046b_2_16
  * [ ] Maps
  * [ ] User authentication backend: https://developers.google.com/identity/sign-in/web/backend-auth
  * [ ] type checking for f_data.py classes (note: holding off until we know for sure what data types we have...)
  * [x] f_datastore.py (check out lmsdatastore.py -> https://github.com/timothyrjames/cs1520/tree/master/week06/gae/project9)
  * [x] Round 1- Routing for URLs
  * [x] User authentication front-end
  * [x] Utility function (show_page()),  for data to appear on pages
  * [x] data classes (rnd 1) - calling this f_data.py (tests: http://bit.ly/1520-classes)... we can rename later

### Low priority
* [ ] Create team name? (we sticking with A?)
* [ ] Create name
* [ ] Create logo 

## Proposal
* https://docs.google.com/presentation/d/1M7u5HtYC5hsmr09UfqeGXXkwklw4zus43RtJ9VeUGnY/edit#slide=id.g7dce42e085_0_7
