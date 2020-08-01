# Strip Controller Master

This is part of the Strip Controller (sc) project and provides a backend as a REST API for the 
[sc-web](https://github.com/brunopk/sc-web). It's created with [Django Rest Framework](https://django-rest-framework.org) 
and its built on python 3.8.x.

## Starting the API

1. Create a virtual environment (venv) if it's not created yet.
2. Activate the venv: `source <path of the venv>/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`
4. Create database: `python manage.py migrate`
5. Create a superuser for Django Rest Framework.
6. Init the server: `python manage.py runserver`

> The output of `python manage.py runserver` will show URL and port of the REST API.

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
    
> This superuser is required to navigate on http://localhost:8000/admin (localhost:8000 is default hostname and port for the REST API), 
> there you can create models (on database) among other actions.  

### Creating new models

1. Create model class on `app/models.py`.
2. Create migrations with `python manage.py makemigrations` command.
3. Apply migrations to database `python manage.py migrate` command.

## Documentation

- JSON: http://localhost:8000/swagger.json
- YAML: http://localhost:8000/swagger.yaml
- swagger-ui: http://localhost:8000/swagger/

More information at: https://github.com/axnsan12/drf-yasg


## Building the circuit

1. With level shifter conversor:

![GitHub Logo](/doc/Raspberry-Pi-WS2812-Steckplatine-600x361.png)

More information: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

2. Without level shifter conversor: 
![GitHub Logo](/doc/raspberry-pi-updated-schematic.png)
More information: https://core-electronics.com.au/tutorials/ws2812-addressable-leds-raspberry-pi-quickstart-guide.html


## Future improvements:

- Authorization for endpoints (Oauth).
- PostgreSQL (currently it's working with Sqlite).

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Quickstar Django REST Framework](http://www.django-rest-framework.org/tutorial/quickstart/)
- https://github.com/axnsan12/drf-yasg)
- https://github.com/rpi-ws281x/rpi-ws281x-python 
- http://github.com/richardghirst/rpi_ws281x
