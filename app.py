import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

# Function to connect to the MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="testuser ",
            password="testpassword",
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
def create_table(conn):
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

# Function to insert a new task
def insert_task(conn, task_name, description, due_date, status):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task_name, description, due_date, status) VALUES (%s, %s, %s, %s)", 
                       (task_name, description, due_date, status))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

# Function to read all tasks
def read_tasks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

# Function to update a specific field of a task
def update_task_field(conn, task_id, field, new_value):
    try:
        cursor = conn.cursor()
        query = f"UPDATE tasks SET {field} = %s WHERE task_id = %s"
        cursor.execute(query, (new_value, task_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No task found with task_id {task_id}")
        else:
            print(f"Task with task_id {task_id} successfully updated")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

# Function to delete a task
def delete_task(conn, task_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print(f"No task found with task_id {task_id}")
        else:
            print(f"Task with task_id {task_id} successfully deleted")
    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

# Main function to handle user input and perform CRUD operations
def main():
    conn = connect_db()
    if conn is None:
        return

    create_table(conn)

    while True:
        print("\nChoose an operation:")
        print("1. Create a new task")
        print("2. Read all tasks")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Exit")
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            task_name = input("Enter task name: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            status = input("Enter task status (Pending, In Progress, Completed): ")
            insert_task(conn, task_name, description, due_date, status)
        elif choice == '2':
            read_tasks(conn)
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            print("Choose a field to update:")
            print("1. Task Name")
            print("2. Description")
            print("3. Due Date")
            print("4. Status")
            field_choice = input("Enter choice (1-4): ")
            if field_choice == '1':
                field = "task_name"
                new_value = input("Enter new task name: ")
            elif field_choice == '2':
                field = "description"
                new_value = input("Enter new description: ")
            elif field_choice == '3':
                field = "due_date"
                new_value = input("Enter new due date (YYYY-MM-DD): ")
            elif field_choice == '4':
                field = "status"
                new_value = input("Enter new status (Pending, In Progress, Completed): ")
            else:
                print("Invalid choice. Please choose a valid field.")
                continue
            update_task_field(conn, task_id, field, new_value)
        elif choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(conn, task_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose a valid operation.")
    
    conn.close()

if __name__ == "__main__":
    main()
