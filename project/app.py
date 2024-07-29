from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Function to connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="172.17.0.2",
            user="root",
            password="rootpassword",
            database="tasks"
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

# Function to create a table for tasks
def create_table():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                task_id INT AUTO_INCREMENT PRIMARY KEY,
                                task_name VARCHAR(255) NOT NULL,
                                description TEXT,
                                due_date DATE,
                                status ENUM('Pending', 'In Progress', 'Completed') NOT NULL)''')
            conn.commit()
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            conn.close()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to view tasks
@app.route('/tasks')
def tasks():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return render_template('tasks.html', tasks=rows)
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            conn.close()
    return "Error connecting to database"

# Route to add a new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tasks (task_name, description, due_date, status) VALUES (%s, %s, %s, %s)", 
                               (task_name, description, due_date, status))
                conn.commit()
                return redirect(url_for('tasks'))
            except mysql.connector.Error as err:
                print(f"An error occurred: {err}")
            finally:
                conn.close()
    return render_template('add_task.html')

# Route to update a task
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            if request.method == 'POST':
                field = request.form['field']
                new_value = request.form['new_value']
                query = f"UPDATE tasks SET {field} = %s WHERE task_id = %s"
                cursor.execute(query, (new_value, task_id))
                conn.commit()
                return redirect(url_for('tasks'))
            else:
                cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
                task = cursor.fetchone()
                return render_template('update_task.html', task=task)
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            conn.close()
    return "Error connecting to database"

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
            conn.commit()
            return redirect(url_for('tasks'))
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
        finally:
            conn.close()
    return "Error connecting to database"

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
