import os
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = '/Users/Szymon/Desktop/UNI/Mag/1 semestr/PythonSQL/project/flaskProject_281219_2201_hb/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '58hqfiqlfb1476478hijgdbkygik67899'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userform = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    visualisations = db.relation('Visualisation', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Visualisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Visualisation('{self.title}','{self.date_created}')"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect((url_for('home')))
    return render_template("register.html", title='Register', form=form)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if 'file' in session:
        return redirect(url_for('table'))
    else:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            sep = request.form.get('Sep')
            enc = request.form.get('Enc')
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session['file'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                session['sep'] = sep
                session['enc'] = enc
                session['filename'] = session['file'][session['file'].rfind('/'):]
                return redirect(url_for('table'))
            elif file and not allowed_file(file.filename):
                flash('Not supported format')
                return redirect(request.url)
        return render_template("upload.html")


@app.route("/upload_back", methods=['GET', 'POST'])
def upload_back():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        sep = request.form.get('Sep')
        enc = request.form.get('Enc')
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            session['file'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            session['sep'] = sep
            session['enc'] = enc
            session['filename'] = filename
            return redirect(url_for('table'))
        elif file and not allowed_file(file.filename):
            flash('Not supported format')
            return redirect(request.url)
    return render_template("upload.html")


@app.route("/saved")
def saved_viz():
    return render_template("saved_viz.html")


@app.route('/table')
def table():
    if 'file' in session:
        df = pd.read_csv(session['file'], sep=session['sep'], encoding=session['enc'])
        return render_template('table.html', data=df.to_html(table_id="table"))
    else:
        flash('No selected file')
        return render_template("upload.html")


if __name__ == '__main__':
    app.run()
