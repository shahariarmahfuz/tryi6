from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# মডেল: User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

# ডাটাবেজ তৈরি করা হচ্ছে
with app.app_context():
    db.create_all()

# ফ্রন্টএন্ড HTML পেজ
@app.route('/')
def index():
    return render_template('index.html')

# ইউজার যোগ করা (POST)
@app.route('/add', methods=['POST'])
def add_user():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    
    if not name or not email or not age:
        return jsonify({'error': 'All fields (name, email, age) are required!'}), 400

    new_user = User(name=name, email=email, age=age)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'})

# ইউজারের সার্চ করা
@app.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('query', '')
    users = User.query.filter(User.name.contains(query)).all()
    return jsonify([{'name': u.name, 'email': u.email, 'age': u.age} for u in users])

# সব ইউজার দেখানো (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'name': u.name, 'email': u.email, 'age': u.age} for u in users])

# Glitch needs this port setup
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
