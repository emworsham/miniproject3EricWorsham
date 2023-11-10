#INF601 - Advanced Programming in Python
#Eric Worsham
#Mini Project 3


from flask import Flask, request, render_template, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key for production

@app.route('/')
def index():
    # Redirect to dashboard if user is logged in
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = db.get_user_by_id(user_id)  # Retrieve user details
        weight_entries = db.get_weight_entries(user_id)
        return render_template('dashboard.html', username=user['username'], entries=weight_entries)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username)  # Verify user credentials
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']  # Store username in session
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db.create_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)  # Clear the username from session
    return redirect(url_for('index'))

@app.route('/log_weight', methods=['POST'])
def log_weight():
    if 'user_id' in session:
        weight = request.form['weight']
        db.log_weight(session['user_id'], weight)
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.init_db()  # Initialize the database only once when the application starts
    app.run(debug=True)
