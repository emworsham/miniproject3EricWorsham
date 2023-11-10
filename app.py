from flask import Flask, request, render_template, redirect, url_for, session
import db  # Importing your database functions from db.py

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production


# Global variable to check if database is initialized
db_initialized = False

@app.route('/')
def index():
    global db_initialized
    if not db_initialized:
        db.init_db()
        db_initialized = True

    if 'user_id' in session:
        weight_entries = db.get_weight_entries(session['user_id'])
        return render_template('dashboard.html', entries=weight_entries)
    else:
        return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You should add password hashing and validation here
        db.create_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic here
        user = db.get_user(username)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/log_weight', methods=['POST'])
def log_weight():
    if 'user_id' in session:
        weight = request.form['weight']
        db.log_weight(session['user_id'], weight)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
