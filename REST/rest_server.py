from flask import Flask, g, request
from flask.helpers import *
import sqlite3
import base64
import string
import random

def get_db():
    # Connect to the sqlite DB at 'files.db' and store the connection in 'g.db'
    # Re-use the connection if it already exists
    if 'db' not in g:
        g.db = sqlite3.connect(
                    'files.db',
                    detect_types=sqlite3.PARSE_DECLTYPES)
    # Enable casting Row objects to Python dictionaries
    g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    # Close the DB connection and remove it from the 'g' object
    db = g.pop('db', None)
    if db is not None:
        db.close()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def write_file(encoded_file):
    base64bytes = base64.b64decode(encoded_file)
    blop_id = id_generator()
    f = open(f"Storage/{blop_id}", "wb")
    f.write(base64bytes)
    f.close() 
    return blop_id


app = Flask(__name__)
# Close the DB connection after serving a request
app.teardown_appcontext(close_db)


@app.route('/')
def hello():
    return make_response({'message': 'Hello World!'})


@app.route('/files', methods=['POST'])
def add_files():
     # Parse the request body as JSON and convert to a Python dictionary
    payload = request.get_json()
    filename = payload.get('filename')
    content_type = payload.get('content_type')
    # Decode the file contents and calculate its original size
    file_data = base64.b64decode(payload.get('contents_b64'))
    size = len(file_data)
    # Store the file locally with a random generated name
    blob_name = write_file(file_data)
    # Insert the File record in the DB
    db = get_db()
    cursor = db.execute(
        "INSERT INTO 'file'('filename', 'size', 'content_type', 'blob_name') VALUES (?,?,?,?)",
        (filename, size, content_type, blob_name)
    )

    
    db.commit()
    # Return the ID of the new file record with HTTP 201 (Created) status code
    return make_response({"id": cursor.lastrowid }, 201)

app.run(host="localhost", port=9000)