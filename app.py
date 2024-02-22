from flask import Flask,request,render_template,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User,Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'rainbowfish12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
context = app.app_context()
context.push()

db.create_all()


@app.route('/')
def root():
    """Hompage rediercts to list of users"""
    return redirect('/users')
######################################################################################
#User routes

@app.route('/users')
def list_users():
    """Shows list of users in db"""
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('list.html',users=users)

@app.route('/users/new',methods=["GET"])
def create_user():
   """Shows form to create new user"""
   return render_template('create.html')

@app.route('/users/new',methods=["POST"])
def new_users():
    new_user = User(
    first_name = request.form['first'],
    last_name = request.form['last'],
    image_url = request.form['image'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
   """Show details about a single user"""
   user = User.query.get_or_404(user_id)
   return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user(user_id):
   """Edit page for user"""
   user = User.query.get_or_404(user_id)
   return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
   """Updating changed info """
   user = User.query.get_or_404(user_id)
   user.first_name = request.form['first']
   user.last_name = request.form['last']
   user.image_url = request.form['image'] 

   db.session.add(user)
   db.session.commit()

   return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
   """Deleting an existing user"""
   user = User.query.get_or_404(user_id)
   
   db.session.delete(user)
   db.session.commit()

   return redirect('/users')
#################################################################################
#Post routes

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_posts_form(user_id):
   """Shows a form to create a new post"""
   user = User.query.get_or_404(user_id)
   return render_template('new_post.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_posts(user_id):
   """Handles form for creating a new post"""
   user = User.query.get_or_404(user_id)

   new_post= Post(
   title = request.form['title'],
   content = request.form['content'],
   user=user)

   db.session.add(new_post)
   db.session.commit()

   return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
   """Shows details about a single post"""
   post = Post.query.get_or_404(post_id)
   return render_template('details_post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
   """Shows a form to update a post"""
   post = Post.query.get_or_404(post_id)
   return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
   """Updating an existing post"""
   post = Post.query.get_or_404(post_id)

   post.title = request.form["title"]
   post.content = request.form["content"]

   db.session.add(post)
   db.session.commit()


   return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
   """Deleting an existing post"""
   post = Post.query.get_or_404(post_id)
   
   db.session.delete(post)
   db.session.commit()

   return redirect(f'/users/{post.user_id}')