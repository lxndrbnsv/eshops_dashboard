from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class EditCategoryForm(FlaskForm):
    cat_name = StringField("Категория:")
    cat_link = StringField()
    submit = SubmitField("Подтвердить")
