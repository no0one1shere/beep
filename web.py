import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_user_data(username):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', '')
    return f"<h1>Hello, {name}</h1>"

@app.route('/read_file', methods=['GET'])
def read_file():
    filename = request.args.get('filename', '')
    with open(f'/var/www/html/{filename}', 'r') as file:
        return file.read()

def hash_password(password):
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('/uploads', filename))
    return 'File uploaded successfully'

@app.route('/xxe', methods=['POST'])
def xxe():
    xml = request.data
    import xml.etree.ElementTree as ET
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    return f"XML parsed: {root.tag}"

if __name__ == '__main__':
    app.run(debug=True)
