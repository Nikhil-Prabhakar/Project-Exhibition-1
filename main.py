from flask import Flask, render_template, redirect, url_for, session, request
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "1234567890"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "nikHIL@2112"
app.config["MYSQL_DB"] = "login"

db = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('loginsuccess', None)
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM logininfo WHERE email=%s AND password=%s",(username,password))
            info = cursor.fetchone()
            if info is not None:
                if info['email'] == username and info['password'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
    return render_template("Index.html")


@app.route('/new' , methods=['GET', 'POST'])
def new_user():
    if request.method == "POST":
        if "one" in request.form and "two" in request.form and "three" in request.form:
            username = request.form['one']
            email = request.form['two']
            password = request.form['three']
            cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("INSERT INTO logininfo(name, password, email)VALUES(%s, %s, %s)",(username, password, email))
            db.connection.commit()
            return redirect(url_for('index'))
    return render_template("register.html")

@app.route('/new/profile')
def profile():
    if session['loginsuccess'] == True:
        return render_template ('pro.html')

@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)