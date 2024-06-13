from flask import Flask, request, jsonify
from flask_restx import Resource, Api, fields
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Movie API',
          description='A simple Movie API')

ns = api.namespace('movies', description='Movie operations')

movie_model = api.model('Movie', {
    'id': fields.Integer(required=True, description='The movie unique identifier'),
    'title': fields.String(required=True, description='The movie title'),
    'year': fields.Integer(required=True, description='The movie release year'),
    'director': fields.String(required=True, description='The movie director'),
    'length': fields.String(required=True, description='The movie length'),
    'rating': fields.Integer(required=True, description='The movie rating')
})

movies = []

# Helper function to validate movie data
def validate_movie_data(data):
    errors = []
    if 'id' not in data:
        errors.append("Field 'id' is required")
    if 'title' not in data or not isinstance(data['title'], str) or len(data['title']) > 100:
        errors.append("Field 'title' is required and should be a string with max length 100")
    if 'year' not in data or not (1900 <= data['year'] <= 2100):
        errors.append("Field 'year' should be an integer between 1900 and 2100")
    if 'director' not in data or not isinstance(data['director'], str) or len(data['director']) > 100:
        errors.append("Field 'director' is required and should be a string with max length 100")
    if 'length' not in data:
        errors.append("Field 'length' is required")
    else:
        try:
            datetime.strptime(data['length'], '%H:%M:%S')
        except ValueError:
            errors.append("Field 'length' should be in format HH:MM:SS")
    if 'rating' not in data or not (0 <= data['rating'] <= 10):
        errors.append("Field 'rating' should be an integer between 0 and 10")
    return errors

@ns.route('/')
class MovieList(Resource):
    @ns.marshal_list_with(movie_model)
    def get(self):
        return movies, 200

    @ns.expect(movie_model)
    @ns.marshal_with(movie_model, code=200)
    def post(self):
        data = request.json
        errors = validate_movie_data(data)
        if errors:
            api.abort(400, ', '.join(errors))
        movies.append(data)
        return data, 200

@ns.route('/<int:movie_id>')
@ns.response(404, 'Movie not found')
@ns.param('movie_id', 'The movie identifier')
class Movie(Resource):
    @ns.marshal_with(movie_model)
    def get(self, movie_id):
        movie = next((m for m in movies if m['id'] == movie_id), None)
        if not movie:
            api.abort(404, 'Movie not found')
        return movie, 200

    @ns.expect(movie_model)
    @ns.marshal_with(movie_model)
    def patch(self, movie_id):
        data = request.json
        movie = next((m for m in movies if m['id'] == movie_id), None)
        if not movie:
            api.abort(404, 'Movie not found')
        errors = validate_movie_data(data)
        if errors:
            api.abort(400, ', '.join(errors))
        movie.update(data)
        return movie, 200

    @ns.response(202, 'Movie deleted')
    def delete(self, movie_id):
        global movies
        movie = next((m for m in movies if m['id'] == movie_id), None)
        if not movie:
            api.abort(404, 'Movie not found')
        movies = [m for m in movies if m['id'] != movie_id]
        return '', 202

api.add_namespace(ns, path='/api/movies')

if __name__ == '__main__':
    app.run(debug=True)
