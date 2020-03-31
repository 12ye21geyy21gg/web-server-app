from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DecimalField,FileField
import wtforms
from wtforms.validators import DataRequired
from flask import Flask, render_template,url_for,redirect,abort
import json,random,sqlite3,hashlib
from flask import Flask
import app.gen as g

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
    finp = FileField('Фотография для модицикаций:')
    submit = SubmitField('Сгенерировать')

def copy_files(names):
    for i in names:


def get_hash(passw):
    return hashlib.sha256(passw.encode('utf8')).hexdigest()

def get_logins(conn):
    return list(map(lambda x: x[0],conn.execute('SELECT login FROM users').fetchall()))

def get_data(login,conn):
    return list(conn.execute(f'SELECT * FROM users WHERE login="{login}"').fetchall()[0])

def insert_user(name,login,pasw,conn):
    conn.execute(f'INSERT INTO USERS (name,login,password) VALUES (\'{name}\',\'{login}\',\'{get_hash(pasw)}\')')
    conn.commit()
def clean():
    pass

app = Flask(__name__,static_url_path='/static')
app.debug =True
app.jinja_env.auto_reload = True

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

auth = False
name = ''
id = ''
temp = None

@app.errorhandler(404)
def not_found(error):
    return "page is not found or bad request"

@app.errorhandler(405)
def not_found(error):
    return "page is not found or bad request"

@app.route('/',methods=['GET','POST'])
def main():
    global temp,app,name,auth
    app.logger.debug([name,auth])
    form = UltimateForm()
    if form.validate_on_submit():
        temp = [form.pixelnoise.data,form.trianglenoise.data,form.mirrored.data,form.mirroredgithub.data,form.captcha.data,int(form.size.data),int(form.num.data),form.inp.data]
        return redirect('/result')
    return render_template('index.html',form=form,name=name,auth=auth)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global app
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('../data/users.db')
        if form.login.data in get_logins(conn):
            data = get_data(form.login.data,conn)
            if get_hash(form.password.data) == data[3]:
                global auth,id,name
                auth = True
                id = data[0]
                name = data[1]
                conn.close()
                return redirect('/')
            else:
                conn.close()
                return render_template('login.html',
                                message="Неправильный логин или пароль",
                                form=form)
        else:
            conn.close()
            return render_template('login.html',
                            message="Неправильный логин или пароль",
                            form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('../data/users.db')
        if form.login.data not in get_logins(conn):
            if len(form.password.data) >= 8:
                insert_user(form.name.data,form.login.data,form.password.data,conn)
                conn.close()
                return redirect('/')
            else:
                conn.close()
                return render_template('register.html',
                                message="Пароль короткий",
                                form=form)
        else:
            conn.close()
            return render_template('register.html',
                            message="Введенный логин уже кем-то используется",
                            form=form)
    return render_template('register.html', form=form)

@app.route('/logout',methods=['GET','POST'])
def logout():
    global auth,name,id
    auth = False
    name = ''
    id = ''
    return redirect('/')

@app.route('/view',methods=['GET','POST'])
def view():
    pass

@app.route('/result',methods=['GET','POST'])
def show():
    global gen,temp,app
    if temp:
        #app.logger.debug(temp)
        if type(temp[0]) is bool:
            if temp[0]:
                gen.gen_random_pixel_noise(temp[5], temp[6], temp[7])
            if temp[1]:
                gen.gen_random_triangle_noise(temp[5], temp[6], temp[7])
            if temp[2]:
                gen.gen_mirrored(temp[5], temp[6], temp[7])
            if temp[3]:
                gen.gen_mirrored_github(temp[5], temp[6], temp[7])
            if temp[4]:
                gen.gen_captcha(temp[5], temp[7])
            temp = 'good'
            return redirect('/result')
        else:
            return render_template('result.html',temp=gen.names)
        #return render_template('view.html')
    else:
        abort(404)


if __name__ == '__main__':
    #clean()
    app.run(port=8080,host='0.0.0.0')
    conn.close()
    clean()