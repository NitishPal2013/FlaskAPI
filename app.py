from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
from dotenv import main
main.load_dotenv()
URI = os.getenv('URI')

app = Flask(__name__)

app.config['MONGO_URI'] = URI
mongo = PyMongo(app)

items_collection = mongo.db['ProjectName']

print(list(items_collection.find()))

@app.route('/')
def home():
    return '<h1>This is home.</h1>'

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = items_collection.find()
    result = []
    for item in items:
        item['_id'] = str(item['_id'])
        result.append(item)
    return jsonify({'items': result})

# Get a specific item
@app.route('/items/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = items_collection.find_one({'_id': item_id})
    if item:
        return jsonify({'item': item})
    return jsonify({'message': 'Item not found'}), 404

# Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    new_item = {'name': request.json['name']}
    result = items_collection.insert_one(new_item)
    return jsonify({'item': new_item}), 201

# Update an item
@app.route('/items/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item = items_collection.find_one({'_id': item_id})
    if item:
        items_collection.update_one({'_id': item_id}, {'$set': {'name': request.json['name']}})
        return jsonify({'item': item})
    return jsonify({'message': 'Item not found'}), 404

# Delete an item
@app.route('/items/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = items_collection.delete_one({"_id":item_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Item deleted'})
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
