from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__)
HABIT_FILE = 'habit_tracker.json'

# Load habits from file
def load_habits():
    try:
        with open(HABIT_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save habits to file
def save_habits(habits):
    with open(HABIT_FILE, 'w') as file:
        json.dump(habits, file, indent=4)

@app.route('/')
def index():
    habits = load_habits()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    habit = request.form['habit']
    habits = load_habits()
    if habit and habit not in habits:
        habits[habit] = []
        save_habits(habits)
    return redirect(url_for('index'))

@app.route('/mark/<habit>')
def mark_habit(habit):
    habits = load_habits()
    if habit in habits:
        today = str(datetime.date.today())
        if today not in habits[habit]:
            habits[habit].append(today)
            save_habits(habits)
    return redirect(url_for('index'))

@app.route('/delete/<habit>')
def delete_habit(habit):
    habits = load_habits()
    if habit in habits:
        del habits[habit]
        save_habits(habits)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

