from flask import render_template, url_for, redirect, request, flash

from app import app
from app.models import Book, User, db
from forms import RegistrationForm



@app.route('/')
def list_all():
    return render_template(
        'list.html',
        books=Book.query.all()
    )


@app.route('/new-book', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        book = Book(title=request.form['title'], author=request.form['author'], category=request.form['category'])
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('list_all'))
    else:
        return render_template(
            'new-book.html',
            page='new-book.html',
            books=Book.query.all(),
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
     #   return redirect(url_for('login'))
        return redirect(url_for('list_all'))
       # return render_template('list.html')   #renders the template but the url has /register in the end
    return render_template('register.html', form=form)





