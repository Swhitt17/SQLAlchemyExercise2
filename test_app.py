from unittest import TestCase

from app import app
from models import db, User,Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

context = app.app_context()
context.push()

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        Post.query.delete()
         
        user = User(first_name='Tyson', last_name='Mays', image_url= 'https://www.freepik.com/icon/profile_3135715#fromView=keyword&term=User&page=1&position=4&uuid=b54ae4ab-f32f-4a13-bd70-d8219a2fa9b7')
        db.session.add(user)
        db.session.commit()


        post = Post(title='First Post', content="This is my first post!",user_id=user.id)
        db.session.add(post)
        db.session.commit
        
        self.user_id = user.id
        self.post_id= post.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        #######################################################################################################################
        #User tests

    def test_list_users(self):
       with app.test_client() as client:
          res = client.get('/users')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>All Users</h1>',html)

    def test_show_user(self):
        with app.test_client() as client:
          res = client.get(f'users/{self.user_id}')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Tyson Mays Details</h1>',html)

    def test_create_user(self):
        with app.test_client() as client:
          res = client.get('/users/new')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Create a user</h1>',html)

    def test_edit_user(self):
        with app.test_client() as client:
          res = client.get('/users/<int:user_id>/edit')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Edit a User</h1>',html)

    ###################################################################################################
          # Post tests 
  
    def test_new_post(self):
       with app.test_client() as client:
          res = client.get('/users/<int:user_id>/posts/new')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Create Post for Tyson Mays</h1>',html)

    def test_show_post(self):
       with app.test_client() as client:
          res = client.get('/posts/<int:post_id>')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>First Post</h1>',html)

    def test_edit_post(self):
       with app.test_client() as client:
          res = client.get('/posts/<int:post_id>/edit')
          html = res.get_data(as_text=True)

          self.assertEqual(res.status_code, 200)
          self.assertIn('<h1>Edit Post </h1>',html)


