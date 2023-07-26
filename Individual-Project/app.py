from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBfp3Ppzd3e_R2Lm10uRnuzGt2YLEna9r4",
  "authDomain": "individual-pro.firebaseapp.com",
  "projectId": "individual-pro",
  "storageBucket": "individual-pro.appspot.com",
  "messagingSenderId": "13013348316",
  "appId": "1:13013348316:web:8730cfb2048110bd622919",
  "measurementId": "G-0RQHF75YWH",
  "databaseURL" : "https://individual-pro-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/',methods=['GET', 'POST'])
def index_page():
    return render_template("index.html")

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template("home.html")

@app.route('/aboutus', methods=['GET', 'POST'])
def about():
    return render_template("aboutus.html")

@app.route('/snacks',methods=['GET', 'POST'])
def snacks():
    return render_template("snacks.html")

@app.route('/shop_all',methods=['GET', 'POST'])
def shop():
    return render_template("shop_all.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/sign_in',methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("sign_in.html")
    else:
        return render_template("sign_in.html")


@app.route('/sign_up',methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": "Fouad", "email": "f@h.com"}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("sign_up.html")
    else:
        return render_template("sign_up.html")


@app.route('/your_bag',methods=['GET', 'POST'])
def yourbag():
    # return render_template("your_bag.html")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user']=auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("your_bag.html")
    else:
        return render_template("your_bag.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))





if __name__ == '__main__':
    app.run(debug=True)