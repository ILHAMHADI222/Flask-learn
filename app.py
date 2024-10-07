from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app)

# Konfigurasi SQLAlchemy untuk MySQL
username = 'root'
password = ''
hostname = 'localhost'
database_name = 'students'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{username}:{password}@{hostname}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Students('{self.name}', '{self.email}')"

# Create database tables
with app.app_context():
    db.create_all()

# Route untuk menambahkan data user baru
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()  # Mengambil data JSON dari request body
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    if not name or not age or not email:
        return jsonify({'error': 'All fields are required'}), 400

    # Membuat instance student baru
    new_user = Students(name=name, age=age, email=email)
    db.session.add(new_user)
    db.session.commit()  # Menyimpan perubahan ke database

    return jsonify({'message': 'User added successfully', 'user': {'name': name, 'age': age, 'email': email}}), 201

# Route untuk mengambil semua data user
@app.route('/users', methods=['GET'])
def get_users():
    users = Students.query.all()
    users_list = [{'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age} for user in users]
    return jsonify(users_list)

# Route untuk mengambil data user berdasarkan ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Students.query.get_or_404(id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age})

# Route untuk memperbarui data user berdasarkan ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = Students.query.get_or_404(id)
    data = request.get_json()  # Mengambil data JSON dari request body

    user.name = data.get('name', user.name)  # Update name jika ada
    user.age = data.get('age', user.age)  # Update age jika ada
    user.email = data.get('email', user.email)  # Update email jika ada

    db.session.commit()  # Menyimpan perubahan ke database

    return jsonify({'message': 'User updated successfully', 'user': {'id': user.id, 'name': user.name, 'age': user.age, 'email': user.email}})

# Route untuk menghapus data user berdasarkan ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Students.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()  # Menyimpan perubahan ke database
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
