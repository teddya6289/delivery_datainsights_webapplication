from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, DateField, \
                    SubmitField, BooleanField,MultipleFileField, \
                    RadioField,SelectField,SearchField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


class enrolform(FlaskForm):
    firstname           =   StringField("First Name:", validators=[DataRequired()])
    lastname            =   StringField("Last Name:", validators=[DataRequired()])
    dateofbirth         =   DateField("DOB:",validators=[DataRequired()])
    email               =   StringField("Email:", validators=[DataRequired(), Email()])
    password            =   PasswordField("Password:", validators=[DataRequired(),Length(min=9)])
    confirm_password    =   PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo("password")])
    jobtitle            =   RadioField("Job Title:", validators=[DataRequired()],
                                       choices=[("Sales director","Sales Director"),\
                                                ("Procurement director","Procurement Director")])
    submit              =   SubmitField("Enrol Now")



class loginform(FlaskForm):
    identifier      =       StringField("Email:", validators=[DataRequired()],render_kw={"Placeholder":"*"})
    password        =       PasswordField("Password:", validators=[DataRequired()],\
                                          render_kw={"Placeholder":"*"})

    login           =       SubmitField("Login")


    

class forgotpasswordform(FlaskForm):
    email               =   StringField("Email:", validators=[DataRequired(), Email()])
    submit              =   SubmitField("Proceed")



class changepasswordform(FlaskForm):
    new_password        = PasswordField("New Password:", validators=[DataRequired(),Length(min=9)],
                                         render_kw={"Placeholder":"*"})
    confirm_password    = PasswordField("Confirm Password:",validators=[DataRequired(),EqualTo("new_password")],
                                        render_kw={"Placeholder":"*"})
    submit              = SubmitField("Change Password")



class verifyageform(FlaskForm):
    dateofbirth         =   DateField("DOB:",validators=[DataRequired()])
    submit              =   SubmitField("Proceed")




