from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import json

app = Flask(__name__, template_folder="templates")
BASE_DIR = 'ema-surveys'

# Get users and EMA status
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in os.listdir(BASE_DIR):
        user_path = os.path.join(BASE_DIR, user)
        ema_path = os.path.join(user_path, 'ema.json')
        if os.path.isdir(user_path):
            with open(ema_path, 'r') as f:
                try:
                    data = json.load(f)
                    is_active = bool(data)  # Active if JSON is non-empty
                except json.JSONDecodeError:
                    is_active = False  # Inactive if JSON is invalid
            users.append({'name': user, 'status': 'active' if is_active else 'inactive'})
    return jsonify(users)

# Replace EMA
@app.route('/replace-ema', methods=['POST'])
def replace_ema():
    user = request.form['user']
    file = request.files['file']
    user_path = os.path.join(BASE_DIR, user)
    if os.path.exists(user_path):
        file.save(os.path.join(user_path, 'ema.json'))
        return jsonify({'message': 'EMA file replaced successfully!'})
    return jsonify({'error': 'User does not exist'}), 404

# Add new user
@app.route('/add-user', methods=['POST'])
def add_user():
    user = request.form['user']
    file = request.files['file']
    user_path = os.path.join(BASE_DIR, user)
    if not os.path.exists(user_path):
        os.makedirs(user_path)
        file.save(os.path.join(user_path, 'ema.json'))
        return jsonify({'message': 'User added successfully!'})
    return jsonify({'error': 'User already exists'}), 400

# Download EMA
@app.route('/download/<user>', methods=['GET'])
def download_ema(user):
    user_path = os.path.join(BASE_DIR, user)
    if os.path.exists(user_path):
        return send_from_directory(user_path, 'ema.json', as_attachment=True)
    return jsonify({'error': 'User does not exist'}), 404

# Render Frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(BASE_DIR, exist_ok=True)
    app.run(debug=True)
