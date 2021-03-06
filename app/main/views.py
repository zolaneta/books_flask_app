import os
from flask import render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename

from app import app
from app.models import Book, User, db
from forms import RegistrationForm, LoginForm, SubmitField, ImageForm
from flask.ext.login import current_user, logout_user, login_user




def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/image-upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return render_template('image_upload.html')





@app.route('/')
def list_all():
    return render_template(
        'list.html',
        books=Book.query.all(),
        categories=Book.query.distinct(Book.category).group_by(Book.category)
    )


@app.route('/category/')
@app.route('/category/<category>')
def category(category=None):
    return render_template(
        'category.html',
        category=category, # goes into {{category}}
        books=Book.query.all(),
        # Query for list of categories (BROWSE BY CATEGORIES)
        categories=Book.query.distinct(Book.category).group_by(Book.category),
        # Query for list of books in specific categories
        category_list=Book.query.filter_by(category=category).all()  # grabs <category>
    )


@app.route('/title/<id>', methods=['GET', 'POST'])
def book(id):
    book = Book.query.get_or_404(id)
    related = Book.query.filter(Book.query.filter_by(id=id).first() != id, Book.category == book.category)
    category_books = Book.query.filter_by(category=(Book.query.filter_by(id=id).first()).category !=id)

##TODO work on querry where specific book is not included

    return render_template(
        'title.html',
        id=id,
        book=book,
        related=related,


        books=Book.query.all(),
        # Query for list of categories (BROWSE BY CATEGORIES)
        categories=Book.query.distinct(Book.category).group_by(Book.category),
        # Query for specific book id
        specific_book=Book.query.filter_by(id=id).first(),
        # Query for displaying books in the same category as the specific book (OTHER BOOKS IN THIS CATEGORY)
        category_books=category_books
                                                        # {{specific_book.category}}
        ### category_books=Book.query.filter_by(category=(Book.query.filter_by(id=id).first()).category).limit(9)

    )






'''
@app.route('/title')
@app.route('/title/<id>', methods=['GET', 'POST'])
def book(id=None):
    return render_template(
        'title.html',
        id=id,
        books=Book.query.all(),
        # Query for list of categories (BROWSE BY CATEGORIES)
        categories=Book.query.distinct(Book.category).group_by(Book.category),
        # Query for specific book id
        specific_book=Book.query.filter_by(id=id).first(),
        # Query for displaying books in the same category as the specific book (OTHER BOOKS IN THIS CATEGORY)
        category_books=Book.query.filter_by(category=(Book.query.filter_by(id=id).first()).category).limit(9)
                                                        # {{specific_book.category}}





        ### category_books=Book.query.filter_by(category=(Book.query.filter_by(id=id).first()).category).limit(9)
    )
'''



@app.route('/new-book', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        # picture loader
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        book = Book(title=request.form['title'], author=request.form['author'], category=request.form['category'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('list_all'))
    else:
        return render_template(
            'new-book.html',
            page='new-book.html',
            books=Book.query.all()
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
     #   return redirect(url_for('login'))
        return redirect(url_for('list_all'))
       # return render_template('list.html')   #renders the template but the url has /register in the end
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print '1'
    if request.method == 'POST':
        print '2'
        if form.validate_on_submit():
            print '3'
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password_hash.data):
                login_user(user)
                print (user)
                return redirect(url_for('list_all'))

            flash('Invalid username or password.')
        else:
            flash('Failed validation')


    return render_template('login.html', form=form)



