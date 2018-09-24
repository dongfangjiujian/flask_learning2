from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Email,EqualTo
from app.models import db,User

class LoginForm(FlaskForm):

    username = StringField('用户名',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    # email = StringField('电子邮箱',validators=[DataRequired(),Email()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    email = StringField('电子邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    # EqualTo()参数需要传入的是变量名 即password
    password2 = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')

    #自定义数据验证的格式是  validate_<field_name>   错误用raise ValueError('error')以显示给用户
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValueError('该邮箱已被注册！')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValueError('该用户名已被注册！')
