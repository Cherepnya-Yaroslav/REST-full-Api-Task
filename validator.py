from datetime import datetime

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