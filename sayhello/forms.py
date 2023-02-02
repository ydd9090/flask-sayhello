from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo
from wtforms import ValidationError
from sayhello.models import Message,User


class HelloForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(1,60)])
    body = TextAreaField("Message",validators=[DataRequired(),Length(1,200)])
    submit = SubmitField()


    def validate_name(self, field):
        return
        if Message.query.filter_by(name=field.data).first():
            raise ValidationError("名字已经被别人占用了，换一个吧")


class LoginForm(FlaskForm):
    username = StringField("用户名",validators=[DataRequired(),Length(1,60)])
    password = PasswordField("密码",validators=[DataRequired()])
    remember = BooleanField("记住我",default=False)
    submit = SubmitField("登录")


class RegisterForm(FlaskForm):
    username = StringField("用户名",validators=[DataRequired(),Length(1,60)])
    password = PasswordField("密码",validators=[DataRequired()])
    password2 = PasswordField("确认密码",validators=[DataRequired(),EqualTo("password",message="两次密码输入不一致")])
    description = TextAreaField("个人介绍",validators=[Length(1,1000)])
    submit = SubmitField("注册")


    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("该用户名已被占用")