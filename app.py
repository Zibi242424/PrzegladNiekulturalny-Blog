from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
import os
from functools import wraps
from datetime import datetime
from pytz import timezone
import re
#from credentials import user_log, user_pass

app = Flask(__name__)
app.secret_key = "my precious"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
#config
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

from models import *

poland = timezone('Europe/Warsaw')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/', methods=['GET'])
def index():
    css = url_for('static', filename='clean-blog.min.css')
    font = url_for('static', filename='font-awesome.min.css')
    bootstrap = url_for('static', filename='bootstrap.min.css')
   # jumbotron = url_for('static',filename='jumbotron.css')
    #css = url_for('static', filename='bootstrap.min.css')
    #date = str(datetime.now(poland))[:-22]    
    posts = db.session.query(BlogPost).order_by("id")[::-1][:3]
    return render_template('index.html', posts=posts, css=css, font=font, bootstrap=bootstrap)
    #return render_template('index.html', posts=posts css=css, jumbotron=jumbotron, date=date)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #user = db.session.query(User).filter_by(id=1).first()
        if username != 'admin' or password != "admin":
            error = 'Invalid credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

@app.route('/dev_menu')
@login_required
def home():    
    return render_template("dev_menu.html")

@app.route('/edit_post_menu')
@login_required
def edit_post_menu():
    """
        Prints all the posts in the database in a table
        and gives a possibility to edit them or delete.
        
        Function returns to the template a table of Post objects.
    """
    posts = db.session.query(BlogPost).order_by("id desc")
    return render_template('edit_post_menu.html', posts=posts)

@app.route('/edit_post/', methods=['GET','POST'])
@login_required
def edit_post():
    if request.method == 'GET':
        global id
        id = int(request.args.get('id', None))
        global post
        post = db.session.query(BlogPost).filter_by(id=id).first()
        return render_template('edit_post.html', post=post)
    if request.method == 'POST':
        title = request.form['title']
        header = f"""{request.form['header']}"""
        text = f"""{request.form['text']}"""
        category = request.form['category'] 
        if title == '' or text == '':
            return "You didn't fill all the obligatory fields (title, text)." 
        post = db.session.query(BlogPost).filter_by(id=id).first()                
        post.title = title
        post.header = header
        post.text = text
        post.category = category
        post.date = str(datetime.now(poland))[:-13]
        db.session.commit()
        return f"Post with title '{ post.title }' was updated"


@app.route('/delete_post', methods=['GET','POST'])
@login_required
def deleting_post():
    """
        Function firstly asks user if he is sure to delete
        a post and if user answers yes it removes a post
        from the database.
    """
    if request.method == 'GET':
        id = int(request.args.get('id', None))
        post = db.session.query(BlogPost).filter_by(id=id).first()
        return render_template('ask_delete_post.html', post=post)
    if request.method == 'POST':
        id = int(request.args.get('id', None))
        title = db.session.query(BlogPost).filter_by(id=id).first().title
        db.session.query(BlogPost).filter_by(id=id).delete()
        db.session.commit()
        flash(f"Post with id {id} and title '{title}' has been deleted.")
        return redirect(url_for('edit_post_menu'))


@app.route('/add_post', methods=['GET','POST'])
@login_required
def adding_post():    
    """
       # This function allows to add new posts. Posts that exists in db
       # cant be added for the second time. Everything is secured with a password
    """    
    if request.method == 'GET':
        return render_template('add_post.html')
    if request.method == 'POST':        
        title = request.form['title']
        header = f"""{request.form['header']}"""
        text = f"""{request.form['text']}"""
        image = f"""{request.form['image']}"""
        category = request.form['category']        
        if title == '' or text == '':
            return "You didn't fill all the obligatory fields (title, text)."
        if BlogPost.query.filter_by(title=title).first() is not None:
            return "Post probably is already in the database."            
        date = str(datetime.now(poland))[:-13]       
        db.session.add(BlogPost(title, header, text, date, category, image))
        db.session.commit()
        db.session.close()
        msg = "Added succesfully"                      
        return f"'{title}' post was added... {msg}"
    return "No authorization to perform this action."

@app.route('/post')
def post():
    post_link = request.args.get('post', None)
    post = db.session.query(BlogPost).filter_by(post_link=post_link).first()
    return render_template('post.html', post=post)

@app.route('/search-by-category')
def search_by_category():
    category = request.args.get('category',None)
    if category == "Gry-Wideo":
        category = "Gry Wideo"
    posts = db.session.query(BlogPost).filter_by(category=category).order_by("id")[::-1]    
    return render_template('search_by_category.html', posts=posts, category=category)

@app.route('/choose-category')
def choose_category():
    return render_template('choose_category.html')

@app.route('/all_posts')
def all_posts():
    posts = posts = db.session.query(BlogPost).order_by("id")[::-1]
    return render_template('all_posts.html', posts=posts)

if __name__ == '__main__':
    app.run()

