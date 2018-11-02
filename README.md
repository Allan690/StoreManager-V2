[![Build Status](https://travis-ci.com/Allan690/StoreManager-V2.svg?branch=develop)](https://travis-ci.com/Allan690/StoreManager-V2)
[![Maintainability](https://api.codeclimate.com/v1/badges/c64c6681c99f2aac3ff2/maintainability)](https://codeclimate.com/github/Allan690/StoreManager-V2/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Allan690/StoreManager-ADC3/badge.svg?branch=ch-database-setup-161438646)](https://coveralls.io/github/Allan690/StoreManager-ADC3?branch=ch-database-setup-161438646)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/3b5f48196e4b3a68d97c)

# Store Manager-API v2
Store Manager API is a flask RESTful API that implements token based authentication with endpoints that enable the user
to:
- register and login to the store
- add, modify and delete products from the store
- view sale records 
- Create sale records

## Example request with response
```
curl --request POST \
  --url https://store-manager-api-app-v1.herokuapp.com/api/v1/auth/register \
  --header 'Content-Type: application/json' \
  --data '{
  "email": "testuser999@gmail.com",
  "password": "testuserpass"
}'

Response body
{
"message": "User registered successfully"
}

Response code 
{
201
}
Response header
{
"connection":"keep-alive"
"content-length" :"48"
"content-type": "application/json"
"date": "Sat, 20 Oct 2018 12:37:59 GMT"
"server": "gunicorn/19.9.0"
"via": "1.1 vegur"
}

```

## Getting Started

1) Clone the repository by doing: `git clone https://github.com/Allan690/StoreManager-API.git`

2) Create a virtual environment: `virtualenv env`

3) Activate the virtual environment: `source venv/bin/activate` on Linux/Mac  or `source venv/Scripts/activate` on windows.

4) Install the requirements : `pip install -r requirements.txt`

5) Create a development and test database in psql: `createdb stores` and `createdb stores_testdb`

6) Create a file called `db.ini` and enter the following:
```
[postgresql]
host=localhost
database=stores
user=postgres
password=postgres
port=5432
```
- Create a similar file for the test database, only changing the database name to `stores_testdb`. Call it `testdb.ini`

## Running tests
- Run this command on the terminal:  ` py.test --cov=app tests/`

### Prerequisites

-  Python 3.6
-  virtual environment
-  Postgres database

## Running it on machine
- Create a .env file to store your environment variables: `touch .env`
- In the `.env` file add this lines: `export SECRET=<your-secret-key-here` and `export FLASK_APP="run.py"`
- Create a file at the root directory called `db.ini` and enter the following into it:
- On terminal do: `source .env`
- Run the application: `flask run`
- The api endpoints can be consumed using postman.

## Endpoints
| Endpoint                                   | FUNCTIONALITY                      |
| ----------------------------------------   |:----------------------------------:|
| POST /api/v2/auth/register                 | This will register  the user       |
| POST /api/v2/auth/login                    | This will login a registered user  |
| POST  /api/v2/products                     | This will add a product            |
| POST  /api/v2/sales                        | This will add a sale               | 
| GET  /api/v2/products                      | This will get all products         |
| GET  /api/v2/products/productId            | retrieve a single product by id    |
| GET  /api/v2/sales                         | retrieve all sale records          |
| GET  /api/v2/sales/salesId                 | retrieves a single sale record     | 
| PUT  /api/v2/products                      | This will modify a product         | 


## Heroku application
https://store-manager-api-app-v1.herokuapp.com/

## API documentation
- *Note*: if using the above documentation for running the application on your local machine, just replace the heroku app
link with your localhost e.g `localhost:5000/api/v1/auth/register` for the registration endpoint

## Built With
* [Flask](http://flask.pocoo.org/) -  The web framework used
* [Pip](https://pypi.python.org/pypi/pip) -  Dependency Management

## Authors
* **Allan Mogusu** 

## License

This project is licensed under the MIT License

