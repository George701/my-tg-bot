import json
import os

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def setItem(item):
    data = load_data()
    data.append(item)
    save_data(data)

def getItemById(item_id):
    data = load_data()
    for item in data:
        if item['id'] == item_id:
            return item
    return None

def editItem(item_id, updated_item):
    data = load_data()
    for i, item in enumerate(data):
        if item['id'] == item_id:
            data[i] = updated_item
            save_data(data)
            return
    raise ValueError(f"Item with id {item_id} not found")

def deleteItem(item_id):
    data = load_data()
    data = [item for item in data if item['id'] != item_id]
    save_data(data)