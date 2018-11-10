[![Build Status](https://travis-ci.com/Allan690/StoreManager-V2.svg?branch=develop)](https://travis-ci.com/Allan690/StoreManager-V2)
![Coverage Status](https://coveralls.io/repos/github/Allan690/StoreManager-V2/badge.svg?branch=develop)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a3f6bf3305b4b7576318)

# Store Manager-API v2
Store Manager API is a flask RESTful API that implements token based authentication with endpoints that enable the user
to:
- register and login to the store
- add, modify and delete products from the store
- view sale records 
- Create sale records

## Example request with response
```
curl -X POST \
  --url 'http://localhost:5000/api/v2/auth/signup' \
  -H 'Authorization: Bearer OAuthAccessToken'\
  -H 'Accept: application/json'\
  -H 'Content-Type: application/json' \
  --data-raw '{
  "email": "sam1@andela.com",
  "password": "sam1234567"
}'
Response body
{
  "Message": "Attendant user registered successfully"
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
https://store-manager-api-app-v2.herokuapp.com/

## API documentation
https://apimatic.io/apidocs/storemanager-api-v2
- *Note*: if using the above documentation for running the application on your local machine, just replace the heroku app
link with your localhost e.g `localhost:5000/api/v2/auth/signup` for the registration endpoint

## Built With
* [Flask](http://flask.pocoo.org/) -  The web framework used
* [Pip](https://pypi.python.org/pypi/pip) -  Dependency Management

## Authors
* **Allan Mogusu** 

## License

This project is licensed under the MIT License

