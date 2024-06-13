REST-full API 1
REST-full API
It is necessary to create a RESTful API service that allows you to manage the list
movies.
The following methods must be implemented:
1. GET /api/movies - list of all movies
you need to return a response with code 200 (OK) and attach the following JSON
structures:
{
"list": [
{
"id": 1,
"title": "Example movie",
"year": 2018,
"director": "Somebody",
"length": "02:30:00",
"rating": 8
},
...
]
}
2. GET /api/movies/:id - information about the movie with the specified id
you need to return a response with code 200 (OK) and attach the following JSON
structures:
"movie": {
"id": 1,
"title": "Example movie",
REST-full API 2
"year": 2018,
"director": "Somebody",
"length": "02:30:00",
"rating": 8
}
}
if no record with the specified id is found, you must return a response with
code 404 (Not Found)
3. POST /api/movies - adding a new movie entry
In the body of the incoming request, you should expect JSON of the following structure:
"movie": {
"id": 1,
"title": "Example movie",
"year": 2018,
"director": "Somebody",
"length": "02:30:00",
"rating": 8
}
}
if successfully added to the list, you must return a response with a code
200 (OK) and attach JSON with the following structure:
{
"movie": {
"id": <unique identifier of the entry>,
"title": "Example movie",
"year": 2018,
"director": "Somebody",
REST-full API 3
"length": "02:30:00",
"rating": 8
}
}
in case of failure, you must return a response with code 500 (Internal Server Error) and
insert JSON of the following structure:
{
"status": 500,
"reason": "<Reason for failure>"
}
4. PATCH /api/movies/:id - changing information about the movie with the specified id
incoming request and response format for successful and unsuccessful changes
same as the previous method
if no record with the specified id is found, you must return a response with
code 404 (Not Found)
5. DELETE /api/movies/:id - deleting an entry with the specified id
if successful, return a response with code 202 (Accepted)
if no record with the specified id is found, you must return a response with
code 404 (Not Found)
in case of other errors, a response with code 500 must be returned (Internal Server
Error) and attach JSON with the following structure:
{
"status": 500,
"reason": "<Reason for failure>"
}
A movie entry has the following fields (all fields are required for
filling):
1. id - integer unique identifier of the record
REST-full API 4
2. title - title of the movie, a line of up to 100 characters
3. year - year of manufacture, an integer from 1900 to 2100;
4. director - full name of the director, line up to 100 characters;
5. length - duration of the film, type - time;
6. rating - movie rating (integer from 0 to 10).
It is necessary to validate incoming field values ​​when creating and changing
records.
In case of a validation error, you must generate a response with code 400 (Bad
Request), indicate the reason for the validation error in the response body.
An example of a response to an attempt to insert a record without specifying the title of the movie:
{
"status": 400,
"reason": "Field 'title' is required"
}
Example response to an attempt to insert a record with a year greater than the maximum
permissible value:
{
"status": 400,
"reason": "Field 'year' should be less then 2100"
}
