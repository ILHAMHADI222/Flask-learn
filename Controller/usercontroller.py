from flask import request, jsonify
from Models.model import db, Students  # Impor db dan Students

# Fungsi untuk menambahkan pengguna baru
def add_user():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')

    # Membuat instance Students
    new_user = Students(name=name, age=age, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully!"}), 201

# Fungsi untuk mendapatkan semua pengguna
def get_users():
    users = Students.query.all()
    user_list = [{"id": user.id, "name": user.name, "age": user.age, "email": user.email} for user in users]
    return jsonify(user_list), 200

# Fungsi untuk mendapatkan pengguna berdasarkan ID
def get_user(id):
    user = Students.query.get_or_404(id)
    return jsonify({"id": user.id, "name": user.name, "age": user.age, "email": user.email}), 200

# Fungsi untuk memperbarui pengguna berdasarkan ID
def update_user(id):
    user = Students.query.get_or_404(id)
    data = request.get_json()

    # Memperbarui atribut pengguna
    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.email = data.get('email', user.email)
    
    db.session.commit()

    return jsonify({"message": "User updated successfully!"}), 200

# Fungsi untuk menghapus pengguna berdasarkan ID
def delete_user(id):
    user = Students.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200
