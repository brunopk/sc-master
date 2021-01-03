# Strip Controller Master

Provides a backend as a REST API for [sc-web](https://github.com/brunopk/sc-web). It's built on [Django Rest Framework](https://django-rest-framework.org) for Python 3.8.

## Starting the API

1. Create a virtual environment (if wasn't done before).
2. Activate the virtual environment: `source <path of the venv>/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create migrations on `app/migrations` : python manage.py makemigrations`.
5. Create database and apply migrations: `python manage.py migrate`.
6. Create Django superuser (see section *Creating Django superuser*).
7. Configure the API (see section *Configuration*).
8. Init the server: `python manage.py runserver`
9. Register consumer applications for OAuth2 (if wasn't done before).  

The output of `python manage.py runserver` will show URL and port, default is http://localhost:8000 (open it on any browser to see API documentation).`Steps 4 y 5 are only required the first time running the server or when adding new models (see also *Creating new models*).


### Configuration

Most properties are defined as constants on `project/settings.py` .

Connection to [sc-rpi](https://github.com/brunopk/sc-rpi) is disabled by default to facilitate development. If you want to enable the connection again, for instance to probe the system with all components ([sc-rpi](https://github.com/brunopk/sc-rpi), [sc-master](https://github.com/brunopk/sc-master) and [sc-web](https://github.com/brunopk/sc-web)):

1. Set `SC_CONNECTION_DISABLED = True` on `project/settings.py` 
2. Run django with `--noreload` argument: `python manage.py runserver --noreload`.

To disable connection to [sc-rpi](https://github.com/brunopk/sc-rpi) and run [sc-master](https://github.com/brunopk/sc-master) with hot-reloading again:

1. Set `SC_CONNECTION_DISABLED = False` on `project/settings.py` 
2. Run django **without** arguments.

### Creating a virtual environment (venv)

```
python3 -m venv <path of the venv>
```

or

```
virtualenv -m <path to the python interpreter> <path of the venv>
```

### Creating Django superuser

```python manage.py createsuperuser```


### Register consumer applications for OAuth2

This is **requiered** to allow sc-web to connect to sc-master and to test services with Postman or another client. To obtain 
a valid access_token first we must register an application. Point your browser at:

http://localhost:8000/o/applications/
Click on the link to create a new application and fill the form with the following data:

- Name: just a name of your choice
- Client Type: confidential
- Authorization Grant Type: Resource owner password-based

It will show the client secret and the client id, put it `CLIENT_ID` variable on `project/settings.py`.


### Creating new models

1. Create model class on `app/models.py`.
2. Delete `db.sqlite3`.
3. Create migrations: `python manage.py makemigrations`.
4. Apply migrations on database: `python manage.py migrate`.

To run the API again, repeat steps 6 y 7 mentioned on *Starting the API* to recreate OAuth2 configurations which are saved on database.

## Authentication

URL :  http://localhost:8000/token/

Request body example : 

```json
{
    "username": "admin",
    "password": "admin"
}
```

## Swagger documentation

- JSON: http://localhost:8000/swagger.json
- YAML: http://localhost:8000/swagger.yaml
- swagger-ui: http://localhost:8000/swagger/

More information at: https://github.com/axnsan12/drf-yasg

To authenticate swagger, get the token with `curl` or Postman, copy-paste it on the authorization dialog and add 
"Bearer " at the beginning, for instance "Bearer PnoA4DtzklANjjcrOrUxQoKXIv6ajc" :

![Swagger online documentation](doc/swagger.png)



## Future improvements:

- PostgreSQL (currently it's working with Sqlite).
- Generalize @swagger_auto_schema(status.HTTP_400_BAD_REQUEST: serializers.ErrorResponse()}) for all APIViews.
- Implement endpoint for token refreshing.
- Periodically check if sc-driver is online.
- Multiple user (not only and admin user).

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Quickstar Django REST Framework](http://www.django-rest-framework.org/tutorial/quickstart/)
- [Django Rest Framework » Getting started](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html)
