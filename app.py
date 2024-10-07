from flask import Flask, render_template
from flask_cors import CORS
import pymysql
from Models.model import db  # Import the db object from model.py
import Controller.usercontroller as ctrl 
 # Import controller functions

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

# Initialize SQLAlchemy
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Register API routes
app.add_url_rule('/users', view_func=ctrl.add_user, methods=['POST'])
app.add_url_rule('/users', view_func=ctrl.get_users, methods=['GET'])
app.add_url_rule('/users/<int:id>', view_func=ctrl.get_user, methods=['GET'])
app.add_url_rule('/users/<int:id>', view_func=ctrl.update_user, methods=['PUT'])
app.add_url_rule('/users/<int:id>', view_func=ctrl.delete_user, methods=['DELETE'])

# Serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
