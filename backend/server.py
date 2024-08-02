from flask import Flask, request, jsonify, g
import mysql.connector
import os
from mysql.connector import Error

app = Flask(__name__)

print("valdooo")
# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12Athmikha@',
    'database': 'v2k'
}

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**DB_CONFIG)
            print(g.db,"success\n\n\n\n")
        except Error as e:
            print(f"Error: {e}")
            g.db = None
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()

# Initialize the database schema
@app.cli.command('initdb')

def initdb_command():
    db = get_db()
    if db is not None:
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
        ''')
        db.commit()
        cursor.close()
        print('Initialized the database.')

# Create an item
@app.route('/signin', methods=['POST'])
def create_item():
    print("innn")
    
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    cursor = db.cursor()
    cursor.execute('INSERT INTO user (email,password) VALUES (%s, %s)',
                   (data['email'], data['password']))
    db.commit()
    item_id = cursor.lastrowid
    cursor.close()
    return jsonify({'id': item_id}), 201

# Read all items
@app.route('/items', methods=['GET'])
def get_items():
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    return jsonify(items)

# Read a single item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)


# Update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    data = request.get_json()
    cursor = db.cursor()
    cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s',
                   (data['name'], data.get('description', ''), item_id))
    if cursor.rowcount == 0:
        cursor.close()
        return jsonify({'error': 'Item not found'}), 404
    db.commit()
    cursor.close()
    return jsonify({'id': item_id})

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    cursor = db.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    if cursor.rowcount == 0:
        cursor.close()
        return jsonify({'error': 'Item not found'}), 404
    db.commit()
    cursor.close()
    return jsonify({'result': True})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)