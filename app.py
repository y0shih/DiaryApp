from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Default MongoDB URI
client = MongoClient(mongo_uri)
db = client.classroom_manager  # Use the `classroom_manager` database
entries_collection = db.entries  # Use the `entries` collection

# Helper function to convert MongoDB document to JSON
def entry_to_dict(entry):
    return {
        'id': str(entry['_id']),
        'title': entry['title'],
        'content': entry['content'],
        'date': entry['date'].isoformat()
    }

# Routes
@app.route('/api/entries', methods=['GET'])
def get_entries():
    entries = list(entries_collection.find().sort('date', -1))  # Sort by date descending
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

if __name__ == '__main__':
    app.run(debug=True)