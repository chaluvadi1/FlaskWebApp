from datetime import datetime
from flask import Flask, render_template, url_for, redirect, flash
from forms import flask_sqlalchemy, SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AnyRandomStringOFcHaracters'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///site.db'
db = SQLAlchemy(app)

class User(db.model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True,nullable=False)
	email = db.Column(db.String(120), unique=True,nullable=False)
	image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
	password = db.Column(db.String(60),nullable=False)
	posts = db.relationship('Post',backref='author',lazy=True)
	
	def __repr__(self):
		return f"User('{self.username}','{self.email},'{self.image_file}')"

class User(db.model):
	id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)	
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	content = db.Column(db.Text,nullable=False)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
	
	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted})"	
			
posts = [ 
		{
			'author' : 'Manoj Chaluvadi',
			'title'  : 'First Web App',
			'content': 'I like Flask',
			'date_posted' : 'March 16 2019' 
			},
		{
			'author' : 'Chandrika Neelisetti',
			'title'  : 'My Web App',
			'content': 'I like Manoj',
			'date_posted' : 'March 16 2019'
			}
		]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts,title='Home')

@app.route("/about")
def about():
	return render_template('about.html',title='About')

@app.route("/register",methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account Created for user { form.username.data } !','success')
		return redirect(url_for('home'))
	return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password': 
			flash( 'Hazzah You are logged in!','success' )
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful, Please Check Username and Password','danger')
	return render_template('login.html',title='Login',form=form)

if __name__ == '__main__':
	app.run(debug=True)
