from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

@app.route('/', methods=['GET'])
def get_task():
    tasks = load_tasks()
    return jsonify(tasks), 200

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'text field required'}), 400
    tasks.append({'text': data['text'] ,'completed': False})
    save_tasks(tasks)
    return jsonify({'message':'created new task'}), 201

@app.route('/complete/<int:index>', methods = ['PATCH'])
def complete_task(index):
    tasks = load_tasks()
    if index >= len(tasks) or index < 0:
        return jsonify({'error': 'task not found'}), 404
    tasks[index]['completed'] = True
    save_tasks(tasks)
    return jsonify({'message': 'task marked complete'}), 200

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_task(index):
    tasks = load_tasks()
    if index >= len(tasks) or index < 0:
        return jsonify({'error': 'task not found'}), 404
    deleted = tasks.pop(index)
    save_tasks(tasks)
    return jsonify({'deleted':deleted}), 200

if __name__ == '__main__':
    app.run(debug=True)