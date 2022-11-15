# IMDB Clone

This repository contains flask app for backend of app. It contains basic functionality of creating users which can be admin and non-admin, and also apis for browsing and updating movies.

# APIs
Corresponding testing can be found in file `imdb_postman_collection.json` which contains example of calling those APIs as well. They are explained below:


### Routes
```bash
$ flask routes
Endpoint                 Methods           Rule
-----------------------  ----------------  -----------------------
login_blueprint.login    POST              /login
movies                   DELETE, GET, PUT  /movies/<int:id>
movies_blueprint.search  GET               /movies/search
static                   GET               /static/<path:filename>
user_management          POST              /users
users                    DELETE, GET, PUT  /users/<int:id>
```
Out of above static currently does not have any files as frontend is not developed.


### How to start development server

1. Create a new python virtual env and activate it
2. Install packages via `pip install -r requirements.txt`
3. Run `flask run`, you should see a server running on 5000 port.


### Code structure
Code has three major apps:
1. App (./app): Root app which is main app we run, it contains routes for all other apps.
2. Auth(./auth): Contains crud operation on users as well provides api for login and signup.
3. Movies(./movies): Contains crud operations on movies and also provides search functionality.

