# Strip Controller Master

Provides a backend as a REST API for [sc-web](https://github.com/brunopk/sc-web). It's built on [Django Rest Framework](https://django-rest-framework.org) for Python 3.8.

## Starting the API

1. Create a virtual environment (if wasn't done before).
2. Activate the virtual environment: `source <path of the venv>/bin/activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create migrations on `app/migrations` : python manage.py makemigrations`
5. Create database and apply migrations: `python manage.py migrate`
6. [Create a Django user](#Creating-Django-users).
7. [Configure authentication](#Authentication).  
8. Start the server: `python manage.py runserver`

> Steps 4 and 5 are only required the first time running the server or when [creating new models](#Creating-new-models).

The output of `python manage.py runserver` will show URL where the API is exposed.

> The default URL for the API is: http://localhost:8000. 

To run the server on different port use:

```
python manage.py runserver localhost:<port>
```

## Creating a virtual environment (venv)

```
python3 -m venv <path of the venv>
```

or

```
virtualenv -m <path to the python interpreter> <path of the venv>
```

In order for VSCode to autodetect virtual environment and use it for debugging, it is recommended to create it on a folder named `.direnv` within the workspace folder.

## Creating Django users

```python manage.py createsuperuser```

It is also possible to create normal user (not superusers).

## Authentication

Authentication to the API is done using Oauth2 protocol ("password" flow) to protect endpoints.

Before invoking any endpoint, **register an application** (entity or person which consumes endpoints) on http://localhost:8000/o/applications/ filling the form following this considerations:

- Name: just a name of your choice
- Client Type: confidential
- Authorization Grant Type: Resource owner password-based

> Remember the client id and the client secret (see [Testing the API](#Testing-the-API)).

## Creating new models

1. Create a new module with the model class on `app/models/`.
2. Import the model on `app/models/__init__.py` (for instance `from .new_model import NewModel`)
3. Delete `db.sqlite3`.
4. Create migrations: `python manage.py makemigrations`.
5. Apply migrations on database: `python manage.py migrate`.

> This will destroy the database so it would be necessary to repeat all step mentioned at the beginning of this README to start the API again.

## Testing the API

> The API can be tested using the interactive Swagger API documentation opening http://localhost:8000 on any browser.

- JSON: http://localhost:8000/swagger.json
- YAML: http://localhost:8000/swagger.yaml
- swagger-ui: http://localhost:8000/swagger/

To authenticate open the authorize dialog on  http://localhost:8000, and complete the corresponding fields:

![Swagger online documentation](doc/swagger.png)

The user and password credentials are set when [creating django users](#Creating-Django-users).

## Editing the code

Recommended IDEs:

- Pycharm
- VSCode

For VSCode it's recommended to install "Python" and "Pylance" extensions and enabling linting. To enabling linting search for "Linting: Pycodestyle Enabled" configuration and check the "Whether to lint Python files using pycodestyle". Also to enable typechecking on VSCode, set the configuration `python.analysis.typeCheckingMode` with "basic" or "strict".

## Future improvements

- PostgreSQL or MongoDB (currently it's working with Sqlite).
- Implement endpoint for token refreshing.

## Links

- [Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Quickstar Django REST Framework](http://www.django-rest-framework.org/tutorial/quickstart/)
- [Django OAuth Toolkit](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html)
- [Django API Documentation](https://github.com/axnsan12/drf-yasg)
