# Google api books/volume DRF copy

## General info
A simple REST application that allows you to store data from google api, and retrieve it.

## Technologies
* docker 20.10.8
* docker-compose 2.0.0
* python 3.9
* django 3.2.6
* django-rest-framework 3.12.4
## Quickstart
### Requirements
Docker and docker-compose are only requirements.
The project was only tested on the docker and docker-compose versions listed above.
### Setup
Clone the repository and run the following commands inside project directory.
```bash
docker-compose up --build
```
If you are running it for the first time run also.
```bash
docker-compose exec web python manage.py collectstatic
```
After this, the app should be available at localhost:8000
## Usage
### POST
App accepts json data from google api books/v1/volumes.
```python
import requests
r = requests.get('https://www.googleapis.com/books/v1/volumes?q=keyword')
requests.post('http://localhost:8000/books/', json=r.json())
```
It is also capable of accepting single records

## Structure

Endpoint | HTTP method | CRUD Method | Result
---------|-------------|-------------|-------
books| GET | READ | Get all books
books/:id | GET | READ | Get a single book
books | POST | CREATE | Add book or books
books/:id | PATCH | UPDATE | Partially update book
books/:id | DELETE | DELETE | Delete a single book