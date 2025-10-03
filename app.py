from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Simple in-memory user storage (use a database in production)
users = {
    'admin': generate_password_hash('password123'),
    'user': generate_password_hash('mypassword')
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and check_password_hash(users[username], password):
        session['user'] = username
        return jsonify({'success': True, 'message': 'Login successful!'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)