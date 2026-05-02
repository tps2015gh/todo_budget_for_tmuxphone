from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

TODO_FILE = 'todo.json'
BUDGET_FILE = 'budget.json'
SETTINGS_FILE = 'settings.json'

START_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_json(file_path):
    if not os.path.exists(file_path):
        return [] if 'settings' not in file_path else {}
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return [] if 'settings' not in file_path else {}

def write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_settings():
    settings = read_json(SETTINGS_FILE)
    if not settings:
        settings = {'active_day': datetime.now().strftime("%Y-%m-%d")}
        write_json(SETTINGS_FILE, settings)
    return settings

@app.route('/')
def index():
    todos = read_json(TODO_FILE)
    budget = read_json(BUDGET_FILE)
    settings = get_settings()
    active_day = settings.get('active_day')
    
    # Get unique days for selection
    days = sorted(list(set([entry.get('date', active_day) for entry in budget] + [active_day])), reverse=True)
    
    # Filter budget by active day
    filtered_budget = [entry for entry in budget if entry.get('date', active_day) == active_day]
    
    # Calculate balances for the active day
    summary = {
        'total': 0,
        'money': 0,
        'creditcard': 0,
        'debt': 0
    }
    
    for entry in filtered_budget:
        amount = float(entry.get('amount', 0))
        entry_type = entry.get('type') # 'income' or 'expense'
        category = entry.get('category') # 'money', 'creditcard', 'debt'
        
        value = amount if entry_type == 'income' else -amount
        summary['total'] += value
        if category in summary:
            summary[category] += value
            
    return render_template('index.html', todos=todos, budget=filtered_budget, summary=summary, 
                           start_time=START_TIME, active_day=active_day, days=days)

@app.route('/set_active_day', methods=['POST'])
def set_active_day():
    day = request.form.get('day')
    if day:
        settings = get_settings()
        settings['active_day'] = day
        write_json(SETTINGS_FILE, settings)
    return redirect(url_for('index'))

@app.route('/add_day', methods=['POST'])
def add_day():
    new_day = request.form.get('new_day')
    if new_day:
        settings = get_settings()
        settings['active_day'] = new_day
        write_json(SETTINGS_FILE, settings)
        
        # Ensure any items without a date get this new date assigned
        budget = read_json(BUDGET_FILE)
        updated = False
        for entry in budget:
            if 'date' not in entry:
                entry['date'] = new_day
                updated = True
        if updated:
            write_json(BUDGET_FILE, budget)
            
    return redirect(url_for('index'))

@app.route('/close_day', methods=['POST'])
def close_day():
    settings = get_settings()
    active_day = settings.get('active_day')
    budget = read_json(BUDGET_FILE)
    
    # Filter entries for the active day
    day_entries = [entry for entry in budget if entry.get('date') == active_day]
    
    if not day_entries:
        return redirect(url_for('index'))
        
    # Calculate summary
    summary = {
        'total': 0,
        'money': 0,
        'creditcard': 0,
        'debt': 0
    }
    for entry in day_entries:
        amount = float(entry.get('amount', 0))
        val = amount if entry.get('type') == 'income' else -amount
        summary['total'] += val
        cat = entry.get('category')
        if cat in summary:
            summary[cat] += val
            
    # Create report
    report = {
        'date': active_day,
        'summary': summary,
        'entries': day_entries,
        'closed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not os.path.exists('reports'):
        os.makedirs('reports')
        
    report_path = os.path.join('reports', f'report_{active_day}.json')
    write_json(report_path, report)
    
    return redirect(url_for('index'))

# --- Todo Routes ---
@app.route('/add', methods=['POST'])
def add():
    description = request.form.get('description')
    if description:
        todos = read_json(TODO_FILE)
        new_todo = {
            'id': str(uuid.uuid4()),
            'description': description,
            'completed': False
        }
        todos.append(new_todo)
        write_json(TODO_FILE, todos)
    return redirect(url_for('index'))

@app.route('/update/<todo_id>', methods=['POST'])
def update(todo_id):
    todos = read_json(TODO_FILE)
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    write_json(TODO_FILE, todos)
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    todos = read_json(TODO_FILE)
    todos = [todo for todo in todos if todo['id'] != todo_id]
    write_json(TODO_FILE, todos)
    return redirect(url_for('index'))

@app.route('/move_to_budget/<todo_id>', methods=['GET'])
def move_to_budget(todo_id):
    todos = read_json(TODO_FILE)
    todo_to_move = next((t for t in todos if t['id'] == todo_id), None)
    
    if todo_to_move:
        return render_template('move.html', todo=todo_to_move)
    return redirect(url_for('index'))

@app.route('/execute_move/<todo_id>', methods=['POST'])
def execute_move(todo_id):
    todos = read_json(TODO_FILE)
    todo_to_move = next((t for t in todos if t['id'] == todo_id), None)
    
    if todo_to_move:
        # Extract details from form
        amount = request.form.get('amount')
        entry_type = request.form.get('type')
        category = request.form.get('category')
        description = request.form.get('description') or todo_to_move['description']
        
        if amount and entry_type and category:
            # Remove from todos
            todos = [t for t in todos if t['id'] != todo_id]
            write_json(TODO_FILE, todos)
            
            # Add to budget
            budget = read_json(BUDGET_FILE)
            settings = get_settings()
            new_entry = {
                'id': str(uuid.uuid4()),
                'amount': float(amount),
                'type': entry_type,
                'category': category,
                'description': description,
                'date': settings.get('active_day')
            }
            budget.append(new_entry)
            write_json(BUDGET_FILE, budget)
        
    return redirect(url_for('index'))

# --- Budget Routes ---
@app.route('/add_budget', methods=['POST'])
def add_budget():
    amount = request.form.get('amount')
    entry_type = request.form.get('type')
    category = request.form.get('category')
    description = request.form.get('description')
    
    if amount and entry_type and category:
        budget = read_json(BUDGET_FILE)
        settings = get_settings()
        new_entry = {
            'id': str(uuid.uuid4()),
            'amount': float(amount),
            'type': entry_type,
            'category': category,
            'description': description,
            'date': settings.get('active_day')
        }
        budget.append(new_entry)
        write_json(BUDGET_FILE, budget)
    return redirect(url_for('index'))

@app.route('/delete_budget/<budget_id>', methods=['POST'])
def delete_budget(budget_id):
    budget = read_json(BUDGET_FILE)
    budget = [entry for entry in budget if entry['id'] != budget_id]
    write_json(BUDGET_FILE, budget)
    return redirect(url_for('index'))

@app.route('/edit_budget/<budget_id>', methods=['GET'])
def edit_budget(budget_id):
    budget = read_json(BUDGET_FILE)
    entry = next((e for e in budget if e['id'] == budget_id), None)
    if entry:
        return render_template('edit_budget.html', entry=entry)
    return redirect(url_for('index'))

@app.route('/update_budget/<budget_id>', methods=['POST'])
def update_budget(budget_id):
    budget = read_json(BUDGET_FILE)
    for entry in budget:
        if entry['id'] == budget_id:
            entry['amount'] = float(request.form.get('amount', entry['amount']))
            entry['type'] = request.form.get('type', entry['type'])
            entry['category'] = request.form.get('category', entry['category'])
            entry['description'] = request.form.get('description', entry['description'])
            break
    write_json(BUDGET_FILE, budget)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
