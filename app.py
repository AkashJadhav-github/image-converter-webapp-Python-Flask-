import os
from flask import Flask, render_template, request, session, redirect, url_for, escape, send_from_directory
from PIL import Image
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'xyzqwert'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('upload.html', msg = ''' Logged in as ''' + username)
    return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] and request.form['password']:
            
            con = sql.connect("app1.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from users where name = ? and password = ?", (request.form['username'], request.form['password']))
            data = cur.fetchall(); 
            
            if len(data) > 0:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            return render_template('login.html', error = "Username/password incorrect")
            
        return render_template('login.html', error = "Username and password cannot be empty")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/enternew')
def new_user():
    return render_template('user.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['addr']
            city = request.form['city']
            password = request.form['password']

            with sql.connect("app1.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (name,addr,city,password) VALUES (?,?,?,?)",(name,addr,city,password) )

                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = "error in insert operation" + str(e)
      
        finally:
            return render_template("complete.html",msg = msg)
            con.close()

@app.route('/list')
def list():
    if 'username' in session:
        con = sql.connect("app1.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from users")

        rows = cur.fetchall(); 
        return render_template("list.html",rows = rows)
    return render_template('login.html', error = "Login to view the list of users")
    
@app.route('/uploader', methods = ['GET', 'POST'])
def uploadfile():
    if 'username' in session:
        if request.method == 'POST':
            target = os.path.join(APP_ROOT, 'images/')
            if not os.path.isdir(target):
                os.mkdir(target)
            else:
                print "could not create directory"
            f = request.files['file']
            filename = f.filename
            destination = "/".join([target, filename])
            f.save(destination)
            img = Image.open(destination).convert('LA')
            img.save(destination)
            return render_template("result.html", image_name=filename)
    return render_template('login.html', error = "Please login to perform this operation")

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


if __name__ == '__main__':
    app.run(debug = True)
