from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configure the path to save the uploaded images
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Redirect to the index page or do something else
        return 'OK - Image uploaded successfully!'

    # If the file does not have an allowed extension, you can handle it accordingly
    return 'Not OK - Invalid file type!'

if __name__ == '__main__':
    app.run(debug=True)
