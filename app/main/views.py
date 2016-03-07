from flask import render_template, url_for, redirect, request

from app import app
from app.models import Book, User, db




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
            books=Book.query.all()
        )