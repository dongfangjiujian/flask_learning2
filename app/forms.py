from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,Length

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



#首先建立修改用户信息的表单
class EditProfileForm(FlaskForm):
    username =StringField('用户名',validators=[DataRequired()])
    about_me = TextAreaField('自我介绍',validators=[Length(min=0,max=200)])
    submit =SubmitField('提交')

    def __init__(self,original_name,*args,**kwargs):
        # super(EditProfileForm,self)是重新加载一次泪，是累能接受original_name这个参数
        super(EditProfileForm,self).__init__(*args,**kwargs)
        self.original_name = original_name

    def validate_username(self,username):
        if username.data != self.original_name:
            user = User.query.filter_by(username = username.data).first()
            if user is not None:
                raise ValueError('该用户名已被注册！')