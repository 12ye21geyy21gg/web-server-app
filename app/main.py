from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DecimalField
import wtforms
from wtforms.validators import DataRequired
from flask import Flask, render_template,url_for,redirect
import json,random,sqlite3,hashlib
from flask import Flask
import app.gen as g

conn = sqlite3.connect('../data/users.db')
gen = g.Gen()

class LoginForm(FlaskForm):
    login = StringField('Логин',validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Ваше имя',validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class UltimateForm(FlaskForm):
    pixelnoise = BooleanField('Режим 1: Шумно-пиксельный')
    trianglenoise = BooleanField('Режим 2: Шумно-треугольный')
    mirrored = BooleanField('Режим 3: Зеркально-пиксельный')
    mirroredgithub = BooleanField('Режим 4: Зеркально-гитхабный')
    captcha = BooleanField('Режим 5: Генератор капчи')
    size = DecimalField('Ширина:', validators=[DataRequired()])
    num = DecimalField('Количество блоков:')
    inp = StringField('Строка для рандомизации:')
    submit = SubmitField('Сгенерировать')

def get_hash(passw):
    return hashlib.sha256(passw.encode('utf8')).hexdigest()

def get_logins():
    return list(map(lambda x: x[0],conn.execute('SELECT login FROM users').fetchall()))

def get_data(login):
    return list(conn.execute(f'SELECT * FROM users WHERE login="{login}"').fetchall()[0])

def insert_user(name,login,pasw):
    conn.execute(conn.execute(f"INSERT INTO USERS (name,login,password) VALUES ('{name}','{login}','{get_hash(pasw)}')"))
    conn.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
auth = False
name = ''
id = ''
temp = None


@app.route('/<temp>')
def main(temp):
    form = UltimateForm()
    render_template('index.html',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data in get_logins():
            data = get_data(form.email.data)
            if get_hash(form.password.data) == data[3]:
                global auth,id,name
                auth = True
                id = data[0]
                name = data[1]
                return redirect('/')
            else:
                render_template('login.html',
                                message="Неправильный логин или пароль",
                                form=form)
        else:
            render_template('login.html',
                            message="Неправильный логин или пароль",
                            form=form)
    return render_template('login.html', title='Авторизация', form=form)
@app.route('/logout',methods=['GET','POST'])
def logout():
    global auth,name,id
    auth = False
    name = ''
    id = ''
    return redirect('/')

@app.route('/view',methods=['GET','POST']):
def view():
    pass

@app.route('/result',methods=['GET','POST']):
def show():
    global gen



if __name__ == '__main__':
    app.run(port=80, host='127.0.0.1')
    conn.close()