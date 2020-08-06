# Strip Controller Master

This is part of the Strip Controller (sc) project and provides a backend as a REST API for the 
[sc-web](https://github.com/brunopk/sc-web). It's created with [Django Rest Framework](https://django-rest-framework.org) 
and Python 3.8.x.

## Starting the API

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`
4. Create database: `python manage.py migrate`
5. Create a superuser for Django Rest Framework.
6. Init the server: `python manage.py runserver`
7. Register consumer applications for OAuth2.  

> The output of `python manage.py runserver` will show URL and port, by default it run on http://localhost:8000. 
> Open it on any browser to see API documentation. 

### Creating a virtual environment (venv)

```
python3 -m venv <path of the venv>
```

or

```
virtualenv -m <path to the python interpreter> <path of the venv>
```

### Creating superuser for Django Rest Framework

```python manage.py createsuperuser```


### Register consumer applications for OAuth2

This is **requiered** to allow sc-web to connect to sc-master and to test services with Postman or another client. To obtain 
a valid access_token first we must register an application. Point your browser at:

http://localhost:8000/o/applications/
Click on the link to create a new application and fill the form with the following data:

Name: just a name of your choice
Client Type: confidential
Authorization Grant Type: Resource owner password-based
It will show the client secret and the client id.


### Creating new models

1. Create model class on `app/models.py`.
2. Create migrations with `python manage.py makemigrations` command.
3. Apply migrations to database `python manage.py migrate` command.


## Authentication

URL :  http://localhost:8000/o/token/

Request body example : 

```json
{
    "username": "admin",
	"password": "admin",
	"client_id" : "QhRNkdPf6v5KXkR4huEi7grQoQDLigHcX7sVGKV9",
    "client_secret": "1yTSz4BSnl1EjItbNsgrFHvsGfH5s89Cc48P4PJCOZuoeC9f55d082nwsfaz2Iw45vdVRmZM0rr7C1vaLzY17IQ8YKRiB7RsFZVmnqDkfoNsOX5IDBgOwhUuhz4mR6KW",
    "grant_type": "password"
}
```

## Swagger documentation

- JSON: http://localhost:8000/swagger.json
- YAML: http://localhost:8000/swagger.yaml
- swagger-ui: http://localhost:8000/swagger/

More information at: https://github.com/axnsan12/drf-yasg

> To authenticate swagger, get the token with `curl` or Postman, copy-paste it on the authorization dialog and add 
> "Bearer " at the beginning, for instance "Bearer PnoA4DtzklANjjcrOrUxQoKXIv6ajc".  



## Building the circuit

1. With level shifter conversor:

![GitHub Logo](/doc/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

More information: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

2. Without level shifter conversor: 
![GitHub Logo](/doc/raspberry-pi-updated-schematic.png)
More information: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html


## Future improvements:

- PostgreSQL (currently it's working with Sqlite).
- Generalize @swagger_auto_schema(status.HTTP_400_BAD_REQUEST: serializers.ErrorResponse()}) for all APIViews

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Quickstar Django REST Framework](http://www.django-rest-framework.org/tutorial/quickstart/)
- [Django Rest Framework » Getting started](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html)
- https://github.com/axnsan12/drf-yasg)
- https://github.com/rpi-ws281x/rpi-ws281x-python 
- http://github.com/richardghirst/rpi_ws281x
