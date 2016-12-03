from flask import *
from functools import wraps
import sqlite3
import sys

DATABASE = 'C:\\Users\\AKASH GUPTA\\PycharmProjects\\Aspire_shashank\\userDB.db'
con = sqlite3.connect('C:\\Users\\AKASH GUPTA\\PycharmProjects\\Aspire_shashank\\userDB.db')
cur1 = con.cursor()

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'thirty'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('my_home.html')
    return render_template('home.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/google_direct')
def google_direct():
    return render_template('google_direct.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first')
            return redirect(url_for('log'))
    return wrap

@app.route('/my_account',methods=['GET','POST'])
@login_required
def my_account():
    if 'logged_in' in session:
        c_user = session['username']
        tData = cur1.execute("select data from users WHERE users.user_name='%s'" % (c_user))
        tData = tData.fetchall()
        userData = tData[0]
        tData = userData[0]
        print ('new data:')
        print (tData)
        # print ('My name is %s' % session['username'])
        return render_template('my_account.html',user=c_user,tData=tData)
    else:
        return render_template('log.html')

@app.route('/save',methods=['GET','POST'])
def save():
    if request.method == 'POST':
        td = request.form['text_data']
        c_user = session['username']
        print (td)
        cur  = None
        cur = cur1.execute("UPDATE users SET data = '%s' WHERE users.user_name='%s';" % (td,c_user))
        if cur:
            print('Text saved')
        tData = cur1.execute("select data from users WHERE users.user_name='%s'" % (c_user))
        tData = tData.fetchall()
        userData = tData[0]
        tData = userData[0]
        print (tData)
    return render_template('my_account.html',tData=tData,user=c_user)


@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('you were logged out')
    return redirect(url_for('log'))

@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if 'logged_in' in session:
        c_user = session['username']
        tData = cur1.execute("select data from users WHERE users.user_name='%s'" % (c_user))
        tData = tData.fetchall()
        userData = tData[0]
        tData = userData[0]
        print ('new data:')
        print (tData)
        # print ('My name is %s' % session['username'])
        return render_template('my_account.html',tData=tData,user=c_user)
    if request.method == 'POST':
        un = request.form['username']
        pswd=request.form['password']
        cur = cur1.execute("SELECT * FROM users where user_name = '%s' and password = '%s'" % (un,pswd))
        user = [dict(name=row[0],password=row[0],email=row[0],data=row[0]) for row in cur.fetchall()]
        if len(user) > 0 :
            session['logged_in'] = True
            current_user = user[0]
            session['username'] = current_user['name']
            c_user=session['username']
            tData = cur1.execute("select data from users WHERE users.user_name='%s'" % (c_user))
            tData = tData.fetchall()
            userData = tData[0]
            tData = userData[0]
            return render_template(('my_account.html'),tData=tData,user = user)
        else:
            error = "Error logging in"
    return render_template('log.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cur = cur1.execute('INSERT INTO users VALUES (?,?,?,?)',(request.form['username'],request.form['password'],request.form['email'],'Enter the text here'))
        cur2 = cur1.execute('select * from users')
        data2 = [dict(name=row[0], password=row[1], email=row[2]) for row in cur2.fetchall()]
        return redirect(url_for('log'))
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run()
