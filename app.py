from flask import Flask, render_template, request, redirect
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

@app.route('/')
def home():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    new_task = request.form['task']
    tasks.append({'text': new_task, 'completed': False})
    save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<int:index>')
def complete_task(index):
    tasks = load_tasks()
    tasks[index]['completed'] = True
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_task(index):
    tasks = load_tasks()
    del tasks[index]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)