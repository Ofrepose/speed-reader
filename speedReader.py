#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np

import os
import sqlalchemy
import random
import string
import oauth2client
import httplib2
from flask import Flask, render_template, request, redirect, url_for, \
    flash, send_from_directory
from datetime import datetime
import sys

import json
import requests
import codecs

from flask import Flask, render_template, request, redirect, url_for, \
    flash, send_from_directory, jsonify, make_response
from datetime import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, asc, desc
from flask import session as sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_user, \
    logout_user, login_required
from random import randint
from flask import Flask, render_template, request, redirect, url_for, \
    flash

from flask import make_response
import requests
from werkzeug.utils import secure_filename

from flask_login import LoginManager
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required

from datetime import datetime
from datetime import date
from sqlalchemy.orm import scoped_session
from flask_mail import Mail, Message
from flask_login import LoginManager, current_user, login_user, \
    logout_user, login_required
app = Flask(__name__)
app.secret_key = 'super_secret_key'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from flask_login import LoginManager, current_user, login_user, \
    logout_user, login_required
import PyPDF2
import re

from create_dbPort import Base, User, Project, Room, Product, \
    UserMixin, Images, Notes, cust_Product, Words, Book, UserBL, UserB, \
    SiteSurvey

engine = create_engine('sqlite:///ac_db_be.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

login = LoginManager(app)
login.login_view = 'wordsHome'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'wordsHome'

skipped = True

reader = codecs.getreader('utf-8')

UPLOAD_FOLDER = os.path.dirname('static/im/usrs/')

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
ALLOWED_EXTENSIONS_BOOKS = set(['pdf', 'epub', 'txt', 'epdf'])
ALLOWED_EXTENSIONS_VIDEOS = set(['mpg', 'mpeg', 'mp4', 'mov'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(  # EMAIL SETTINGS
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    )

mail = Mail(app)


@login_manager.user_loader
def load_user(id):
    user = session.query(UserB).filter_by(id=id).one()
    return user


@app.route('/wordsHome', methods=['GET', 'POST'])
def wordsHome():
    all_users = session.query(UserB).all()
    keywords = ['manchester city']
    today = datetime.today().strftime('%Y-%m-%d')
    print(today)

    if request.method == 'POST':
        for a in all_users:
            print(a)
            if a.email.lower() == request.form['email'].lower() \
                and a.p_word == request.form['p']:

            # if 'haroldfranklinpayne@gmail.com' == request.form['email'].lower() and 'bright661' == request.form['p']:

                login_user(a, remember=True)
                return redirect(url_for('wordsProfile'))
        return render_template('wordsHome.html')

    if current_user.is_authenticated:
        return redirect(url_for('wordsProfile'))

    return render_template('wordsHome.html')


@app.route('/wordsSearch/', methods=['GET', 'POST'])
def wordsSearch():

    all_books = session.query(Book).all()
    all_books_keywords = ''
    hit_count = []
    b_hit = []

    for a in all_books:
        all_books_keywords = all_books_keywords + ' ' + a.name
        hit_count.append(a.id)

    all_books_keywords_final = all_books_keywords.split()
    print(all_books_keywords_final[1])
    print(all_books_keywords_final)

    if request.method == 'POST':

        u_words = request.form['word']
        u_words_all = u_words.split()
        for a in all_books:
            print(a.name + ' is a.name')
            print(request.form['word'] + ' is word in form')
            if request.form['word'].lower() in a.name.lower():

                b_hit.append(a)
                print('here')

        for b in b_hit:
            print(b.name)

        return render_template('wordsSearch.html', all_books=all_books,
                               hit_count=hit_count, b_hit=b_hit)

    return redirect(url_for('wordsHome'))


@app.route('/wordsProfile')
@login_required
def wordsProfile():
    print(allowed_file('test.pdf'))
    this_user = session.query(UserB).filter_by(id=1).one()
    this_books = \
        session.query(Book).filter_by(owner_id=this_user.id).all()
    print('this user id is ' + str(this_user.id))
    return render_template('wordsProfile.html', this_user=this_user,
                           books=this_books)


@app.route('/api/words/<int:id>/', methods=['GET'])
def api_words(id):
    this_user = session.query(UserB).filter_by(id=1).one()
    all_con = session.query(Book).filter_by(id=id,
            owner_id=this_user.id).one()

    if request.method == 'POST':
        all_con = session.query(Book).filter_by(id=id,
                owner_id=current_user.id).one()
        all_con.save_loc = request.form['page']

        session.add(all_con)
        session.commit()
        print('all_con save loc is ' + str(all_con.save_loc))

        return redirect(url_for('wordsProfile'))

    if all_con.filename[-3:] == 'txt':
        print('all_con filename last 3 is ' + all_con.filename[-3:])
        book_txt = open('static/im/usrs/' + str(this_user.id) + '/'
                        + all_con.filename, 'r')
        decoded_string = book_txt.read()
        decoded_string = decoded_string.replace('\r', '')
        decoded_string = decoded_string.replace('\n', '')
        all_con.content = bytes(decoded_string, 'utf-8'
                                ).decode('unicode_escape')

        # print(all_con.content)

        session.add(all_con)
        session.commit()

        w_lst = all_con.content.split()

        return render_template('words.html', user=this_user,
                               w_lst=w_lst, content=all_con.content,
                               all_con=all_con)

    # pdfFileObj = open('static/nutshell2.pdf', 'rb')

    pdfFileObj = open('static/im/usrs/' + str(this_user.id) + '/'
                      + all_con.filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    content_here = ''
    number_of_pages = pdfReader.getNumPages()

    print('number of pages {}'.format(number_of_pages))

    for page_number in range(number_of_pages):  # use xrange in Py2

        page = pdfReader.getPage(page_number)
        try:

            # print("Trying to extract text from page: {}".format(page_number))

            page_content = page.extractText()
        except IndexError:

            print('ERROR, keyerror /content')
            all_con.compat = 2
            session.add(all_con)
            session.commit()
            return redirect(url_for('wordsProfile'))

            # print(page_content)
            # print(page_content)

        content_here = content_here + page_content

    content_here = content_here.replace('\r', ' ')
    content_here = content_here.replace('\n', ' ')

    decoded_string = bytes(content_here, 'utf-8'
                           ).decode('unicode_escape')

    all_con.content = decoded_string

    session.add(all_con)
    session.commit()

    w_lst = all_con.content.split()

    w_lst2 = str(w_lst).replace(all_con.name, '')

    w_lst = w_lst2.split()

    try:
        gotdata = w_lst[1]
    except IndexError:
        gotdata = 'null'
        print('ERROR, book is not indexed correctly')
        all_con.compat = 2
        session.add(all_con)
        session.commit()
        return redirect(url_for('wordsProfile'))

    # return render_template ('words.html', user = this_user, w_lst = w_lst, content = all_con.content, all_con = all_con )

    return jsonify({'user': this_user.id, 'save_loc': all_con.save_loc,
                   'content': all_con.content})


@app.route('/words/<int:id>/', methods=['GET', 'POST'])
def words(id):

    this_user = session.query(UserB).filter_by(id=1).one()
    all_con = session.query(Book).filter_by(id=id,
            owner_id=this_user.id).one()

    return render_template('words.html', book_id=all_con.id)


@app.route('/words/upload/', methods=['GET', 'POST'])
@login_required
def uploadBook():

    userinfo = session.query(UserB).filter_by(id=1).one()

    if request.method == 'POST':
        print('inside request method is equal to post inside upload profile picture'
              )
        all_books = session.query(Book).all()

        # check if the post request has the file part

        if 'file' not in request.files:
            print('file not in requeest files')

            # return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            print('file.filename is equal to blank ')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            path = 'static/im/usrs/' + str(userinfo.id)
            print(path)
            UPLOAD_FOLDER = os.path.dirname('static/im/usrs/'
                    + str(userinfo.id) + '/')
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            # for a in all_photos:
            #     if a.photo_name == filename:
                    # filename = filename + str("1")

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                      filename))

            # thisUser = session.query(User).filter_by(id = user_id).one()
            # thisUser.profile_picture = filename

            newBook = Book(filename=filename, compat=1,
                           owner_id=userinfo.id,
                           name=request.form['name'],
                           author=request.form['author'])

            session.add(newBook)
            session.commit()
            return redirect(url_for('wordsProfile'))

    print('nothing found here')
    return redirect(url_for('wordsProfile'))


@login_manager.user_loader
def load_user(id):
    user = session.query(UserB).filter_by(id=id).one()
    return user


@app.teardown_request
def remove_session(ex=None):
    session.remove()


@app.route('/logout')
def logout():
    print('logged out')
    logout_user()

    return redirect(url_for('Portfolio'))

today = datetime.now().date()
visitCount = 0


@app.teardown_request
def remove_session(ex=None):
    session.remove()


def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower())
    print(filename.rsplit('.', 1)[1].lower()
          in ALLOWED_EXTENSIONS_BOOKS)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS_BOOKS


if __name__ == '__main__':

    app.debug = False
    app.run(host='0.0.0.0')

    # connect_args=={'check_same_thread': False}
