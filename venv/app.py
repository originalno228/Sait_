import math
import sqlite3
import os

import tkinter as tk
from tkinter import filedialog

from flask import Flask, render_template, url_for, request, redirect, flash, session, make_response
# from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # для хеширования паролей

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ski.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "455e7d29d0e896fdf85dfd93619a44a1aa8c5243"
db = SQLAlchemy(app)

picFolder = os.path.join('static', 'pictures')
app.config['UPLOAD_FOLDER'] = picFolder

DATABASE = 'ski.db'
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'ski.db')))

root = tk.Tk()
root.withdraw()

# if request.method == "POST":
# session['name'] = request.form['name']
# return redirect(url_for('login'))
# global remarks

redacting = False  # рисуются ли кнопки Удалить редактировать

text = ""
@app.route('/login', methods=["POST", "GET"])
def login():
    global redacting
    global text

    if request.method == "POST" and request.form['name'] == "Admin" and request.form['psw'] == "12345" and redacting == False:
        flash("Вы успешно зарегестрированы", "success")
        redacting = True
        text = "Вы вышли"
        return render_template("login.html", Admin=True)

    if request.method == "POST" and redacting == True:
        flash("Вы вышли", "error")
        text = ""
        redacting = False
        return render_template("login.html", Admin=False)
    else:
        if text == "":
            pass
        else:
            flash(text, "error")
            redacting = False
        return render_template("login.html", Admin = False)


@app.route('/posts/<int:id>')
def post_detail(id):  # функция перехода на подробный просмотр статьи
    article = Article.query.get(id)
    if redacting == True:

        return render_template("post_detail.html", Admin=True, article=article)

    else:
        return render_template("post_detail.html", article=article)



def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


# функция для создания бд
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


@app.route('/')
def index():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'on.jpg')#картинка!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'itcube.jpg')  # картинка!!!!!!!!!!!!!!!!!!!!!!!!!!!

    if redacting:#выход
        return render_template("index.html", user_image=pic1, user_image2=pic2, Admin = True)
    else:#вход
        return render_template("index.html", user_image=pic1, user_image2=pic2, Admin = False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    public = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Articel %r' % self.id  # объект + айди


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    if redacting:#выход
        return render_template("posts.html", articles=articles, Admin = True)
    else:#вход
        return render_template("posts.html", articles=articles, Admin = False)



@app.route('/posts/<int:id>/del')
def post_delete(id):  # функция удаления статьи
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Ошибка при удалении статьи"


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):  # функция редактирования статьи
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')  # перейти на
        except:
            return "Ошибка при редактировании статьи"
    else:

        return render_template("post_update.html", article=article, Admin=True,)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():# функция создание статьи (на сайте)
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']


        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')  # перейти на
        except:
            return "Ошибка при добавлении статьи"
    else:
        if redacting:  # выход
            return render_template("create-article.html", Admin=True)
        else:  # вход
            return render_template("create-article.html", Admin=False)


@app.route('/predlog-article', methods=['POST', 'GET'])
def predlog_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')  # перейти на
        except:
            return "Ошибка при добавлении статьи"
    else:
        if redacting:  # выход
            return render_template("predlog-article.html", Admin=True)
        else:  # вход
            return render_template("predlog-article.html", Admin=False)



@app.route('/Admin', methods=['POST', 'GET'])
def Admin():
    return render_template("Admin.html", Admin=True)


@app.route('/Guest', methods=['POST', 'GET'])
def Guest():
    return render_template("Guest.html")





if __name__ == '__main__':
    app.run(debug=True)
