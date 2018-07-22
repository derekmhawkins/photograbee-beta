import os, random, time, json, boto3, botocore
from app import app, db, mail
from flask import session, redirect, render_template, url_for, flash, send_from_directory, request
from app.models import User, Post, Category, Comment, Tag, Photo, Genre
from app.forms import LoginForm, RegistrationForm, BlogForm, CategoryForm, CommentForm, PortfolioForm, ContactForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from flask_mail import Message
from app.email import send_contact_form_email

s3 = boto3.client(
  "s3",
  aws_access_key_id=os.getenv('S3_KEY'),
  aws_secret_access_key=os.getenv('S3_SECRET')
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      bucket_name,
      file.filename,
      ExtraArgs= {
        "ACL": acl,
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    # This is a catch all exception, edit this part to fit your needs.
    print("Something Happened: ", e)
    return e
  return f"{app.config['S3_LOCATION']}{file.filename}"

def category_count(num):
  return Category.query.get(num).posts.count()

def comments_count(num):
  return Post.query.get(num).comments.count()

@app.route('/')
def index():
  context = {
    "title": "Photograbee",
    "photos": Photo.query.order_by(Photo.timestamp.desc()).limit(9).all(),
    "form": ContactForm(),
  }
  return render_template('index.html', **context)


@app.route('/about')
def about():
  return render_template('about.html', title='About')


@app.route('/portfolio')
def portfolio():
  context = {
    "title": "Portfolio",
    "weddings": Genre.query.filter_by(name='Wedding').first().photos.all(),
    "studios": Genre.query.filter_by(name='Studio').first().photos.all(),
    "natures": Genre.query.filter_by(name='Nature').first().photos.all(),
    "travels": Genre.query.filter_by(name='Travel').first().photos.all(),
    "events": Genre.query.filter_by(name='Events').first().photos.all(),
  }
  return render_template('portfolio-grid_1.html', **context)


@app.route('/pricing')
def pricing():
  return render_template('pricing.html', title='Pricing')


@app.route('/blog/<int:id>', methods=['GET', 'POST'])
def blog_single(id):
  context = {
    "post": Post.query.get(id),
    "posts": Post.query.order_by(Post.created_on.desc()).all(),
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "comments": Post.query.get(id).comments.all(),
    "comments_count": Post.query.get(id).comments.count(),
    "form": CommentForm(),
    "tags": Tag.query.order_by('name').all()
  }
  if context['form'].validate_on_submit():
    db.session.add(Comment(name=context['form'].name.data, body=context['form'].body.data, post_id=id))
    db.session.commit()
    flash("Comment posted successfully.")
    return redirect(url_for('blog_single', id=id, _anchor='section-comments'))
  return render_template('blog/blog-single.html', **context)


@app.route('/blog')
def blog():
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.created_on.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('blog', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('blog', page=posts.prev_num) if posts.has_prev else None
  context = {
    "title": "Blog",
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "comments_count": comments_count,
    "tags": Tag.query.order_by('name').all()
  }
  return render_template('blog/blog.html', **context, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/blog/category/<cat_id>')
def blog_category(cat_id):
  page = request.args.get('page', 1, type=int)
  posts = Post.query.filter_by(category_id=cat_id).paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('blog', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('blog', page=posts.prev_num) if posts.has_prev else None
  context = {
    "title": "Blog",
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "comments_count": comments_count,
    "tags": Tag.query.order_by('name').all()
  }
  return render_template('blog/blog.html', **context, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/blog/tag/<tag_id>')
def tag_category(tag_id):
  page = request.args.get('page', 1, type=int)
  posts = Tag.query.get(tag_id).posts.paginate(page, app.config['POSTS_PER_PAGE'], False)
  next_url = url_for('blog', page=posts.next_num) if posts.has_next else None
  prev_url = url_for('blog', page=posts.prev_num) if posts.has_prev else None
  context = {
    "title": "Blog",
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "comments_count": comments_count,
    "tags": Tag.query.order_by('name').all()
  }
  return render_template('blog/blog.html', **context, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/contact')
def contact():
  context = {
    "title": "Contact",
    "form": ContactForm(),
  }
  return render_template('contact.html', **context)


@app.route('/contact-send', methods=['POST'])
def contact_send():
  form = ContactForm()
  if form.validate_on_submit():
    # msg = Message('[Photograbee] {} has an inquiry'.format(form.name.data), sender=form.email.data, recipients=[app.config['ADMINS'][0]])
    # msg.body = form.body.data
    # msg.html = '<p>{}</p>'.format(form.body.data)
    # mail.send(msg)
    send_contact_form_email()
    flash("Your inquiry has been submitted.")
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  context = {
    'title': 'Sign In',
    'form': LoginForm(),
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "tags": Tag.query.order_by('name').all()
  }
  if context['form'].validate_on_submit():
    user = User.query.filter_by(email=context['form'].email.data).first()
    if user is None or not user.check_password(context['form'].password.data):
      flash('Invalid email or password')
      return redirect(url_for('login'))
    login_user(user, remember=context['form'].remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    flash('You are currently logged in.')
    if user.is_admin:
      return redirect(url_for('admin_blog'))
    return redirect(url_for('admin_blog'))
  return render_template('authentication/login.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
  context = {
    'form': RegistrationForm(),
    'title': 'Register',
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "tags": Tag.query.order_by('name').all()
  }
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  if context['form'].validate_on_submit():
    print('it works!')
    user = User(name=context['form'].name.data, email=context['form'].email.data)
    user.set_password(context['form'].password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('index'))
  return render_template('authentication/register.html', **context)

@app.route('/logout')
def logout():
  logout_user()
  flash('You are logged out.')
  return redirect(url_for('login'))


@app.route('/admin/portfolio', methods=['GET', 'POST'])
@login_required
def admin_portfolio():
  context = {
    "portfolioForm": PortfolioForm(),
    "genre_choices": [(i.id, i.name) for i in Genre.query.all()],
  }
  context['portfolioForm'].genre.choices = context['genre_choices']
  if context['portfolioForm'].validate_on_submit():
    # if not os.path.exists(app.config['PORTFOLIO_FOLDER']):
    #   os.makedirs(app.config['PORTFOLIO_FOLDER'])
    # filename = str(int(time.time())) + '.png'
    # context['portfolioForm'].image.data.save(os.path.join(app.config['PORTFOLIO_FOLDER'], filename))
    file = request.files["image"]
    file.filename = str(int(time.time())) + '.png'
    db.session.add(Photo(model_name=context['portfolioForm'].model_name.data, image=upload_file_to_s3(file, os.getenv('S3_BUCKET')), event=context['portfolioForm'].event.data, synopsis=context['portfolioForm'].synopsis.data, camera=context['portfolioForm'].camera.data, lens=context['portfolioForm'].lens.data, focus=context['portfolioForm'].focus.data, shutter=context['portfolioForm'].shutter.data, iso=context['portfolioForm'].iso.data, genre_id=context['portfolioForm'].genre.data))
    db.session.commit()
    flash("Photo saved successfully")
    return redirect(url_for('admin_portfolio'))
  return render_template('admin/portfolio.html', **context)


@app.route('/admin/blog', methods=['GET', 'POST'])
@login_required
def admin_blog():
  context = {
    "title": "Admin",
    "form": BlogForm(),
    "categoryForm": CategoryForm(),
    "categories": [(c.id, c.name) for c in Category.query.order_by('name').all()],
    "category": Category.query.order_by('name').all(),
    "category_count": category_count,
    "new_posts": Post.query.order_by('created_on').limit(5).all(),
    "tags": Tag.query.order_by('name').all(),
    "tag_choices": [(i.id, i.name) for i in Tag.query.order_by('name').all()],
  }
  context['form'].category.choices = context['categories']
  context['form'].tags.choices = context['tag_choices']
  
  if context['form'].validate_on_submit():
    # Blog form
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #   os.makedirs(app.config['UPLOAD_FOLDER'])
    # filename = str(int(time.time())) + '.png'
    # context['form'].image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file = request.files["image"]
    file.filename = str(int(time.time())) + '.png'
    post = Post(title=context['form'].title.data, image=upload_file_to_s3(file, os.getenv('S3_BUCKET')), body=context['form'].body.data, author=current_user, category_id=context['form'].category.data)
    tags = [i.strip() for i in context['form'].tags.data.split(',')]
    names = [i.name for i in Tag.query.all()]

    # Add tags to posts
    for i in tags:
      if i not in names:
        new_tag = Tag(name=i)
        post.tags.append(new_tag)
      else:
        existing_tag = Tag.query.filter_by(name=i).first()
        post.tags.append(existing_tag)
    db.session.add(post)
    db.session.commit()
    flash("Your post has submitted successfully")
    return redirect(url_for('admin_blog'))
  return render_template("admin/blog.html", **context)


@app.route('/add-category', methods=['POST'])
def add_category():
  categoryForm = CategoryForm()
  if categoryForm.validate_on_submit():
    category = Category.query.filter_by(name=categoryForm.name.data).first()
    if category is not None:
      flash('Category already exists. Try another.')
    else:
      db.session.add(Category(name=categoryForm.name.data))
      db.session.commit()
      flash('Category added.')
    return redirect(url_for('admin'))


# @app.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#   context = {
#     "categoryForm": CategoryForm(),
#     "blogForm": BlogForm(),
#     "portfolioForm": PortfolioForm(),
#     "category_choices": [(c.id, c.name) for c in Category.query.order_by('name').all()],
#     "tag_choices": [(i.id, i.name) for i in Tag.query.order_by('name').all()],
#     "genre_choices": [(i.id, i.name) for i in Genre.query.all()],
#     "title": "Admin Panel",
#   }
#   context['blogForm'].category.choices = context['category_choices']
#   context['blogForm'].tags.choices = context['tag_choices']
#   context['portfolioForm'].genre.choices = context['genre_choices']
#   return render_template('admin/index.html', **context)


@app.route('/img/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/img/portfolio/uploads/<filename>')
def portfolio_file(filename):
  return send_from_directory(app.config['PORTFOLIO_FOLDER'], filename)
