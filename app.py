from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# মডেল
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()

# নতুন ভিডিও যোগ করার API
@app.route('/add', methods=['POST'])
def add_video():
    data = request.get_json()
    title = data.get('title')
    url = data.get('url')

    if not title or not url:
        return jsonify({'error': 'title and url required'}), 400

    video = Video(title=title, url=url)
    db.session.add(video)
    db.session.commit()
    return jsonify({'message': 'Video added successfully!'})

# সব ভিডিও দেখার API
@app.route('/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([{'title': v.title, 'url': v.url} for v in videos])

# Fly.io-compatible run
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
