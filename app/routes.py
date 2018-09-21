from app import app
from flask import render_template,redirect,flash,url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',username = '左旭')

@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if  form.validate_on_submit():
        flash('登录用户名{},记住我 {}'.format(form.username.data,form.remember_me.data))
        return redirect(
            url_for('login')
        )
    return render_template('login.html',form = form)

