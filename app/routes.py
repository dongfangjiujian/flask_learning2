from app import app
from flask import render_template,redirect,flash,url_for,request
from app.forms import LoginForm,RegistrationForm,EditProfileForm,PostForm
from werkzeug.urls import url_parse
from datetime import datetime
# 登录视图中需要验证用户 所以需要import User模型
from app.models import User,db,Post
# 用户登录 登出 需要用到Flask_login的login_user 和 logout_user函数 和current_user属性来储存当前用户
from flask_login import login_user,logout_user,current_user,login_required

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
# flask-login 访问权限判定 需要用到@login_required装饰器  放到其他装饰器下面，因为装饰器是从下向上的
@login_required
def index():
    form = PostForm()
    posts = Post.query.all()
    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data,author =current_user)
        db.session.add(post)
        db.session.commit()
        flash('文章一发不!')
        return redirect(url_for('index'))
    return render_template('index.html',form = form,posts = posts,username = '左旭')

@app.route('/login',methods=['POST','GET'])
def login():
    # 先判断当前用户是否是已授权用户
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or form.password.data != user.password:
            flash('用户名不存在或密码错误')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        # 先判定是否从其他页面跳转到的login页面 ，以便登录后调回原来页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        # flash('登录用户名{},记住我 {}'.format(form.username.data,form.remember_me.data))
        return redirect(
            url_for('index')
        )
    return render_template('login.html',form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['post','get'])
def register():
    form = RegistrationForm()
    #  form.validate_on_submit 提交过后 其实validate_username 和 validate_email都已经验证
    if form.validate_on_submit():
        #添加新用户到数据库  和shell中的操作一样
        new_user = User(username = form.username.data,password = form.password.data,email = form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！')
        return redirect(url_for('login'))
    return render_template('register.html',form = form,title= '注册页面')

# 用户信息显示页面
@app.route('/user/<username>')
@login_required
def user(username):
    #首先需要查询数据库，将用户对象找到
    user = User.query.filter_by(username = username).first()
    posts =user.posts
    return render_template('user.html',user = user,posts = posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

#自我介绍 以及名字修改 EditProfile
@app.route('/editProfile',methods=['post','get'])
def editProfile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('修改成功！')
        return redirect(url_for('editProfile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return  render_template('editProfile.html',form = form,title = 'EditProfile')

# @app.route('/post',methods=['POST'])
# def postArtical():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title = form.title.data,content = form.content.data)
#         db.session.add(post)
#         db.session.commit()
#         flash('文章一发不!')
#         return redirect(url_for('index'))
#     return render_template('index.html',form = form)