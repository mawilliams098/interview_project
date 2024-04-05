# Weather App

For this project I used Django and Redis for the backend, and added Bootstrap to style the HTML frontend.  

This app uses a Python Celery task to asynchronously call the OpenWeather API while the page renders, so before starting this app locally you will first need to start the Celery task. 

## Setup Instructions: 

### Download .env 

I've emailed Deborah a `.env` file containing all of my API keys, please download this and put it into the main project folder `interview_project/interview_project`

### Start & activate virtualenv 

Create virtualenv: `$ python -m env weather-env`

Activate virtualenv: `$ source weather-env/bin/activate`

### Install redis 
Linux:   
`$ sudo apt update`  
`$ sudo apt install redis`

macOS:  
`$ brew install redis`

### Install packages 

`$ pip install -r requirements.txt`

### Starting redis server & celery worker
Open up a new terminal and start redis with:  

`$ redis-server`

This terminal will stay the dedicated window for Redis and will need to be left open while running the app. 

Next, open up a new terminal and navigate to the root of this interview project folder `../interview_project` and start the celery worker by running 
 
`$ python -m celery -A interview_project worker -l info`

### Start the app 

Thank you for going along with all of these setup shenanigans so far, the app is ready to be run. In a new terminal navigate to the folder that holds `manage.py` and run 

`python manage.py runserver`

The app should now be available in `http://localhost:8000/`


Note: These "how to setup redis" instructions are taken from here: [https://realpython.com/asynchronous-tasks-with-django-and-celery/#install-redis-as-your-celery-broker-and-database-back-end](https://realpython.com/asynchronous-tasks-with-django-and-celery/#install-redis-as-your-celery-broker-and-database-back-end)