from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import jwt

app = Flask(__name__)
CORS(app, origins=["https://flask123.vercel.app", "http://localhost:8080"])  # Frontend link here

# Configure MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.classroom_manager
entries_collection = db.entries
users_collection = db.users  # collection for users

# Bcrypt for password hashing
bcrypt = Bcrypt(app)

# JWT Secret Key 
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fun12313109rhvoebhvoeh")

# Helper function to convert MongoDB document to JSON
def entry_to_dict(entry):
    return {
        'id': str(entry['_id']),
        'title': entry['title'],
        'content': entry['content'],
        'date': entry['date'].isoformat()
    }

# Routes for Authentication
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        abort(400, description="Missing username or password")

    # Check if user already exists
    if users_collection.find_one({'username': data['username']}):
        abort(400, description="Username already exists")

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create new user
    new_user = {
        'username': data['username'],
        'password': hashed_password
    }
    users_collection.insert_one(new_user)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not 'username' in data or not 'password' in data:
        abort(400, description="Missing username or password")

    # Find the user
    user = users_collection.find_one({'username': data['username']})
    if not user or not bcrypt.check_password_hash(user['password'], data['password']):
        abort(401, description="Invalid username or password")

    # Generate JWT token
    token = jwt.encode({
        'username': user['username'],
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token}), 200

# Routes for Entries 
@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = list(entries_collection.find().sort('date', -1))
    return jsonify([entry_to_dict(entry) for entry in entries])

@app.route('/api/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    if not data or not 'title' in data or not 'content' in data:
        abort(400, description="Missing title or content")

    new_entry = {
        'title': data['title'],
        'content': data['content'],
        'date': datetime.utcnow()
    }
    result = entries_collection.insert_one(new_entry)
    new_entry['_id'] = result.inserted_id
    return jsonify(entry_to_dict(new_entry)), 201

@app.route('/api/entries/<string:id>', methods=['PUT'])
def update_entry(id):
    data = request.get_json()
    if not data or not 'title' in data or not 'content' in data:
        abort(400, description="Missing title or content")

    updated_entry = {
        'title': data['title'],
        'content': data['content'],
        'date': datetime.utcnow()
    }
    result = entries_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_entry})
    if result.matched_count == 0:
        abort(404, description="Entry not found")

    updated_entry['_id'] = ObjectId(id)
    return jsonify(entry_to_dict(updated_entry)), 200

@app.route('/api/entries/<string:id>', methods=['DELETE'])
def delete_entry(id):
    result = entries_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        abort(404, description="Entry not found")
    return jsonify({'message': 'Entry deleted successfully'}), 200



# Protected route
@app.route('/api/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        abort(401, description="Missing or invalid token")
    
    token = auth_header.split(" ")[1]  # Extract the token part
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Hello, {decoded["username"]}'}), 200
    except jwt.ExpiredSignatureError:
        abort(401, description="Token expired")
    except jwt.InvalidTokenError:
        abort(401, description="Invalid token")

if __name__ == '__main__':
    app.run(debug=True)