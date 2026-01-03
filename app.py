from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Database configuration
# Use /tmp for App Engine Standard (read-only filesystem)
DATABASE = '/tmp/tasks.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Display all tasks"""
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the database"""
    title = request.form.get('title')
    description = request.form.get('description')
    
    if title:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, description) VALUES (?, ?)',
                     (title, description))
        conn.commit()
        conn.close()
        flash('Task added successfully!', 'success')
    else:
        flash('Title is required!', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed"""
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    """Display statistics about tasks"""
    conn = get_db_connection()
    total_tasks = conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
    completed_tasks = conn.execute('SELECT COUNT(*) FROM tasks WHERE completed = 1').fetchone()[0]
    pending_tasks = total_tasks - completed_tasks
    conn.close()

    return render_template('stats.html',
                         total=total_tasks,
                         completed=completed_tasks,
                         pending=pending_tasks)

# Initialize database when module is imported (for gunicorn)
init_db()

if __name__ == '__main__':
    # Run the application locally
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
