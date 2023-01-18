from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length
from wtforms import ValidationError
from sayhello.models import Message


class HelloForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(1,20)])
    body = TextAreaField("Message",validators=[DataRequired(),Length(1,200)])
    submit = SubmitField()


    def validate_name(self, field):
        return
        if Message.query.filter_by(name=field.data).first():
            raise ValidationError("名字已经被别人占用了，换一个吧")