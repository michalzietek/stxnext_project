# stxnext_project
##Deployment
```
https://library-stxnextproject.herokuapp.com/
```
##Local installation
**STEPS**
* Create virtual enviroment and activate it
```
$: virtualenv venv
$: source venv/bin/activate
```
* Clone git repository
```
$: git clone link_to_repository
```
* Go to library directory
```
$: cd library
```
* Install requirements
```
$: pip install -r requirements.txt
```
* Set up local settings from local_settings.template

* Create database

* Run the migrations
```
$: python manage.py migrate
```
* Run the application
```
$: python manage.py runserver
```
If everything went well you should see your app running :)