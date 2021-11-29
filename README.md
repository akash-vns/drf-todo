# drf-todo #

### About  ###

* DRF-todo is used to manage a daily todo and used to schedule todo task.
* this app is only depends on rest framework so there is no front end associated.
* all the API doc is under the url swagger-ui with (domain name)
* for the testing purpose, I created some django fixture that will help you to Run and test application with sufficient data
* cron task is running on every hour, and it's create notification 


run and helpful commands
------------
App going to urn on 127.0.0.1:8001 (if you hit the url, and it's shows server is running on page it means you project is successfully running)
* for creating virtual env run, it will also install a project related pip requirements  
    - make setup_python_env
* to start project 
    - make start
* to dump dummy data (create a fixture file are into the todo app)
  - make dummy_data
* to rebuild app
  - make rebuild
* to restart
  - make restart
* to loaddata in to database (used fixture file from todo app)
  - make loaddata
* to perform or you have to run any terminal command you have to use
  - make shell
* to run test 
  - make test
* to migrate and run makemigrations 
  - make migrate / makemigrations
* to  add task to cron job 
  - make runcrons
* to  show/list cron task 
  - make showcrons


Used libraries
-----------------
django_crontab  # to manage scheduling task
django-rest-framework
django-rest-auth # to manage login and logout
