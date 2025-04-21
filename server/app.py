#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
import os

from models import db, Movie

app = Flask(__name__, static_folder='../client/build', static_url_path='/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/movies', methods=['GET'])
def movies():
    if request.method == 'GET':
        movies = Movie.query.all()

        return make_response(
            jsonify([movie.to_dict() for movie in movies]),
            200,
        )

    return make_response(
        jsonify({"text": "Method Not Allowed"}),
        405,
    )

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=5555)
