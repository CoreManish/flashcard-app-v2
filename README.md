### This is graded project for the course Modern Application development 2 (MAD2) at IITM

### Introduction
This project is a SPA (single page application) designed using VueJS. Data at UI is being populated via API call.
### Author
* Manish Kumar
* I’m passionate to write code from scratch, but also like library and framework
### Description
* A user can register then create a deck and add cards to it.
* He/She can choose a deck to review
* Each card in a deck will have question and answer (hidden)
  * He has to think and recall the answer
  * He can verify the answer by clicking on `show answer` button
  * Now he can submit response by selecting difficulty of that question
  * Depending on the difficulty selection, that question will be shown after a predefined time-interval

### Technologies used
#### Frontend
* JavaScript
* VueJS 2
* Vue Router
* HTML
* Bootstrap
* CSS
#### Backend
* Programming language - Python
* Library
  * flask - For Server
  * flask-restful - API design
  * jwt - Authentication (json web token)
  * datetime
  * sqlite3
  * redis database - for caching and celery broker
  * celery - for async batch jobs 
* Templating - Jinja
* Database - SQLite
* ORM - flask-sqlalchemy

### Structure of the project
* All the controller for the request end point are present in `main.py` file
* Model for the database and table is present in `models.py`
* `static/vue/app.js` is the main controller file for SPA
* `static/vue/components` folder contains all the component for the SPA
* Redis server configuration is present in `redis_config` file
* Celery job is being handled in `schedule_job.py` file
