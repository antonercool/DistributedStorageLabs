from flask import Flask, g, request
from flask.helpers import *
import sqlite3
import base64
import string
import random
import os

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
    file_data = payload.get('contents_b64')
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

@app.route('/files', methods=['GET'])
def list_files():
    # Query the database for all files
    db = get_db()
    cursor = db.execute("SELECT * FROM `file`")
    if not cursor:
        return make_response({"message": "Error connecting to the database"}, 500)
    files = cursor.fetchall()
    # Convert files from sqlite3.Row object (which is not JSON-encodable) to
    # a standard Python dictionary simply by casting
    files = [dict(f) for f in files]
    return make_response({"files": files})


from flask import Flask, make_response, g, request, send_file
...
@app.route('/files/<int:file_id>', methods=['GET'])
def download_file(file_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM `file` WHERE `id`=?", [file_id])
    if not cursor:
        return make_response({"message": "Error connecting to the database"}, 500)
    f = cursor.fetchone()
    # Convert to a Python dictionary
    f = dict(f)
    print("File requested: {}".format(f))
    # Return the binary file contents with the proper Content-Type header.
    return send_file(f"Storage/{f['blob_name']}", mimetype=f['content_type'])


@app.route('/files/meta/<int:file_id>', methods=['GET'])
def meta_data(file_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM `file` WHERE `id`=?", [file_id])
    if not cursor:
        return make_response({"message": "Error connecting to the database"}, 500)
    f = cursor.fetchone()
    # Convert to a Python dictionary
    f = dict(f)
    print( f['size'] )
    return make_response({"size": f"{f['size']}" })    


def remove_file(filename):
    os.remove(f"Storage/{filename}")
    return "File deleted"
 
 
@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM file WHERE id=?", [file_id])
    if not cursor:
       return make_response({"message": "Error connecting to the database"}, 500)
 
    f = cursor.fetchone()
    # Convert to a Python dictionary 
    data_dictionary = dict(f)
    print(f"File delete: {data_dictionary}")
 
    cursor = db.execute("DELETE FROM file WHERE id=?", [file_id])
    db.commit()
    # Return the binary file contents with the proper Content-Type header.
    return remove_file(f"{data_dictionary['blob_name']}")  

app.run(host="localhost", port=9000)