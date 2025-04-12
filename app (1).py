from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'mysecretkey'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

users = {
    "drjohn": {"password": "doc123", "role": "doctor"},
    "alice": {"password": "pat456", "role": "patient"}
}

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = users.get(username)
    if user and user['password'] == password:
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('landing'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('landing'))

    role = session.get('role')
    if role == 'doctor':
        return render_template('doctor_dashboard.html', username=session['username'])
    elif role == 'patient':
        return render_template('patient_dashboard.html', username=session['username'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return redirect(url_for('landing'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('dashboard'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    flash('File uploaded successfully!')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
