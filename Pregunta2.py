import pyotp
import sqlite3
import hashlib
import uuid
from flask import Flask, request
app = Flask(__name__)
db_name = 'devnet.db'
@app.route('/')
def index():
    return 'Testing CCNA DEVNET'
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASHES
           (USERNAME  TEXT    PRIMARY KEY NOT NULL,
            LASTNAME  TEXT    NOT NULL,
            HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASHES (USERNAME, LASTNAME, HASH) "
                  "VALUES ('{0}', '{1}', '{2}')".format(request.form['username'], request.form['lastname'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "username has been registered."
    print('username: ', request.form['username'], 'lastname: ', request.form['lastname'], 'password: ', request.form['password'], 'hash: ', hash_value)
    return "signup success"
def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASHES WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'login success'
        else:
            error = 'Invalid username/password'
    else:
        error = 'Invalid Method'
    return error
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=7890, ssl_context='adhoc')