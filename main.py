from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DecimalField,FileField
import wtforms
from wtforms.validators import DataRequired
from flask import Flask, render_template,url_for,redirect,abort,request
import json,random,sqlite3,hashlib,time,shutil,os
from flask import Flask
import app.gen as g
import app.gc as GC
from os import listdir
from os.path import isfile, join

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
    pixilise = BooleanField('Режим 6: Пиксилятор фото')
    monopixilise = BooleanField('Режим 7: Черно-белый пиксилятор фото')
    voronoise = BooleanField('Режим 8: Эффект Вороного')
    photo_voronoise = BooleanField('Режим 9: Фото с эффектом Вороного')
    size = DecimalField('Ширина:', validators=[DataRequired()])
    num = StringField('Количество блоков:')
    porog = StringField('Порог:')
    inp = StringField('Строка для рандомизации:')
    finp = FileField('Фотография для модицикаций:')
    submit = SubmitField('Сгенерировать')

def copy_file_function(list_of_files, directory1, directory2,rename=True):
    global usrs
    auth,name,id,temp = get_usrs(request.remote_addr)
    if id != 0:
        for i in list_of_files:
            address = directory1 + '/' + i
            shutil.copy(address, directory2)
            if rename:
                os.rename(directory2 + '/' + i, directory2 + '/' + str(id)+'_' + i)
    else:
        return

def get_usrs(ip):
    global usrs
    if ip not in usrs.keys():
        usrs[ip] = [False,'',0,list()]
        return False,'',0,list()
    else:
        return usrs[ip][0],usrs[ip][1],usrs[ip][2],usrs[ip][3]

def get_works(id):
    global gc
    onlyfiles = [f for f in listdir(join('..','data','usr')) if isfile(join('..','data','usr', f))]
    temp = list()
    copy_file_function(onlyfiles,'../data/usr','../static',rename=False)
    #gc.add_files(list(map(lambda x:x.split('_')[1],onlyfiles)),'../static')
    gc.add_files(onlyfiles,'../static')
    for i in onlyfiles:
        if str(id) == i.split('_')[0]:
            temp.append('/static/'+i)
    return temp

def get_hash(passw):
    return hashlib.sha256(passw.encode('utf8')).hexdigest()

def get_logins(conn):
    return list(map(lambda x: x[0],conn.execute('SELECT login FROM users').fetchall()))

def get_data(login,conn):
    return list(conn.execute(f'SELECT * FROM users WHERE login="{login}"').fetchall()[0])

def insert_user(name,login,pasw,conn):
    conn.execute(f'INSERT INTO USERS (name,login,password) VALUES (\'{name}\',\'{login}\',\'{get_hash(pasw)}\')')
    conn.commit()


app = Flask(__name__,static_url_path='/static')
app.debug =True
app.jinja_env.auto_reload = True

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
gc = GC.Gc(app.logger)

usrs = dict() # [auth,name,id,temp]

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')

@app.errorhandler(405)
def not_found(error):
    return render_template('error.html')

@app.route('/help')
def get_help():
    return render_template('help.html')

@app.route('/',methods=['GET','POST'])
def main():
    global usrs,gc
    auth,name,id,temp = get_usrs(request.remote_addr)
    form = UltimateForm()
    if form.validate_on_submit():
        if form.num.data == '':
            num = 0
        else:
            try:
                num = int(form.num.data)
            except Exception:
                num = 5
        if form.porog.data == '':
            porog = 127
        else:
            try:
                porog = int(form.porog.data)
            except Exception:
                porog = 127
        fname = ''
        if request.method == 'POST':
            f = request.files['file']
            fname = hashlib.sha256((str(time.time())+str(f.content_length)).encode('utf8')).hexdigest() + '.png'
            f.save('../static/'+fname)
            app.logger.debug(fname)
            gc.add_files([fname],'../static')
            f.close()
        usrs[request.remote_addr][3] = [form.pixelnoise.data,form.trianglenoise.data,form.mirrored.data,form.mirroredgithub.data,form.captcha.data,int(form.size.data),num,form.inp.data,form.pixilise.data,form.monopixilise.data,porog,'../static/'+fname,form.voronoise.data,form.photo_voronoise.data]
        return redirect('/result')
    return render_template('index.html',form=form,name=name,auth=auth)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global app,gc
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('../data/users.db')
        if form.login.data in get_logins(conn):
            data = get_data(form.login.data,conn)
            if get_hash(form.password.data) == data[3]:
                global usrs
                auth, name, id, temp = get_usrs(request.remote_addr)
                auth = True
                id = data[0]
                name = data[1]
                usrs[request.remote_addr] = [auth,name,id,temp]
                conn.close()
                gc.check()
                return redirect('/')
            else:
                conn.close()
                gc.check()
                return render_template('login.html',
                                message="Неправильный логин или пароль",
                                form=form)
        else:
            conn.close()
            gc.check()
            return render_template('login.html',
                            message="Неправильный логин или пароль",
                            form=form)
    gc.check()
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
    global usrs
    usrs[request.remote_addr] = [False,'',0,list()]
    return redirect('/')

@app.route('/view',methods=['GET','POST'])
def view():
    global temp,gc
    auth, name, id, temp = get_usrs(request.remote_addr)
    if id > 0:
        return render_template('view.html', temp=get_works(id))
    else:
        abort(404)

@app.route('/download',methods=['GET','POST'])
def download():
    auth, name, id, temp = get_usrs(request.remote_addr)
    if os.path.isfile(temp):
        pass
    else:
        return render_template('error.html',message='Слишком поздно, генерируйте заного')

@app.route('/result',methods=['GET','POST'])
def show():
    global gen,app,usrs,gc
    auth, name, id, temp = get_usrs(request.remote_addr)
    app.logger.debug(gc.stack)
    if temp:
        if type(temp[0]) is bool:
            try:
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
                if temp[8]:
                    gen.gen_pixilise(temp[5],temp[6],temp[11])
                if temp[9]:
                    gen.gen_monopixilise(temp[5],temp[6],temp[11],temp[10])
                if temp[12]:
                    gen.gen_voronoise(temp[5],temp[6],temp[7])
                if temp[13]:
                    gen.gen_photo_voronoise(temp[5],temp[6],temp[11])

            except Exception as e:
                app.logger.debug(e.__class__.__name__)
                gc.check()
                return abort(404)
            usrs[request.remote_addr][3] = gen.names
            copy_file_function(gen.get_fnames(),'../static','../data/usr')
            gc.add_files(gen.get_fnames(),'../static')

            gen.names = list()
            gc.check()
            return redirect('/result')
        else:
            gc.check()
            return render_template('result.html',temp=usrs[request.remote_addr][3])
        #return render_template('view.html')
    else:
        abort(404)

@app.route('/delete/<num>',methods=['GET','POST'])
def delete(num):
    try:
        os.remove('../data/usr/'+num)
    except Exception as e:
        app.logger.debug(e)
        abort(404)
    return redirect('/view')


if __name__ == '__main__':
    gc.clean()
    app.run(port=8080,host='0.0.0.0')