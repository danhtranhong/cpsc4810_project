from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configure the path to save the uploaded images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to connect to the PostgreSQL database
def connect_to_db():
    connection = psycopg2.connect(
        host='database-test.chqug9auzx3l.us-east-1.rds.amazonaws.com',
        port=5432,
        database='database_test',
        user='postgres',
        password=''
    )
    return connection

# Function to check the database status
def check_database_status():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Execute a sample query to check the status
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        return f"Database status: Connected, Result: {result[0]}"

    except Exception as e:
        return f"Database status: Error - {str(e)}"

    finally:
        if connection:
            connection.close()

def update_database(filename):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
#        insert_query = sql.SQL("INSERT INTO record (filename) VALUES ({})").format(sql.Literal(file.filename))
#        cursor.execute(insert_query)

        insert_query = sql.SQL('INSERT INTO images.result ("filename") VALUES ({})').format(
            sql.Literal(filename)
        )
        cursor.execute(insert_query)

        # Commit the changes to the database
        connection.commit()

    except Exception as e:
        # Handle the exception (e.g., log the error)
        print(f"Error updating database: {str(e)}")

    finally:
        if connection:
            connection.close()
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return redirect(request.url)

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        # Save the file to the server
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Update the database with file information
        update_database(filename)

        # Redirect to the home page or any other appropriate page
        return redirect(url_for('index'))
@app.route('/check_database_status', methods=['GET'])
def check_status():
    status_result = check_database_status()
    return render_template('home.html', status_result=status_result)

if __name__ == '__main__':
    app.run(debug=True)
