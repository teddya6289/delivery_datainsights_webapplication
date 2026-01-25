from flask import request,render_template,redirect,url_for, flash,Blueprint,current_app,abort
from application import db
from db_model_mapping import User
from flask_login import current_user,login_user,logout_user,login_required
from app_forms import enrolform,loginform
from app_extentions import get_safe_redirect, generate_userid,limiter
from flask_limiter.util import get_remote_address




useraccess_bp = Blueprint('user',__name__)



@useraccess_bp.route('/enroluser', methods=['GET','POST'])
def enroluser():
    form = enrolform()
    if  form.validate_on_submit():
        if request.method == "POST":
            
            Email       =   form.email.data
            checkemail  =   User.query.filter_by(email= Email).first()
            
            if checkemail:
                flash(f"Email:{Email} already exist. please enter a different email to enrol or log in","danger")
                return redirect(url_for('insights.home'))

            f_name      = form.firstname.data
            l_name      = form.lastname.data
            dob         = form.dateofbirth.data
            Password    = form.password.data
            Jobtitle    = form.jobtitle.data
            Userid      = generate_userid(f_name,l_name)
            
            new_user = User(
                            userid      = Userid,
                            firstname   = f_name,
                            lastname    = l_name,
                            dateofbirth = dob,
                            email       = Email,
                            jobtitle    = Jobtitle)
            
            
            new_user.set_password(Password)
            db.session.add(new_user)
            db.session.commit()
            flash(f"You have been enrolled to data insights successfully.please log in to proceed","success")
            return redirect(url_for('insights.home'))
        
    return render_template('enrol.html', form = form)



@useraccess_bp.route('/login',methods=['GET','POST'])
@limiter.limit("48 per hour",key_func=lambda:request.form.get("identifier" or request.remote_addr))
def login():
    from datetime import (datetime, timezone)
    MAX_ATTEMPTS    = current_app.config["MAX_ATTEMPTS"]
    LOCK_DURATION   = current_app.config["LOCK_DURATION"]

    l_form = loginform()
    if request.method == "POST":
        if l_form.validate_on_submit():
            now = datetime.now(timezone.utc)
            try:
                    Email       =    l_form.identifier.data
                    Password    =    l_form.password.data 
                    user = User.query.filter_by(email = Email).first()
                    if user:
                    
                        if user.locked_until and user.locked_until > now:
                            abort(403,description=f"Account locked.Try again after {round((user.locked_until-now).total_seconds() // 60)} minutes")
                            
                            
                        
                        if user and user.check_password(Password):
                            user.failed_attempts = 0
                            user.locked_until = None
                            db.session.commit()
                            login_user(user)
                            user.last_active = datetime.now(timezone.utc)
                            db.session.commit()
                            next_page = request.args.get('next')
                            return get_safe_redirect(next_page, 'insights.home')
                        
                        else:
                            user.failed_attempts += 1
                            db.session.commit()
                            if user.failed_attempts >= MAX_ATTEMPTS:
                                user.locked_until = now + LOCK_DURATION
                                db.session.commit()
                                abort(429,
                                      description=f"Account locked for {LOCK_DURATION.seconds//60} minutes due to too many failed attempts.")
                                
                            else:
                                flash(f"DANGER!!! Invalid credentials. Attempt {user.failed_attempts} of {MAX_ATTEMPTS}.", "warning")
                                return redirect(url_for("user.login")) 
                    else:
                         flash("Invalid credentials,please check and retry","warning")
                         return redirect(url_for("user.login"))
            except Exception as e:
                    flash(f"{e}", "danger")
    return render_template('login.html', form = l_form)


@useraccess_bp.route('/signout')
@login_required
def signout():
    current_user.email_verified = False
    db.session.commit()
    logout_user()
    return redirect(url_for('insights.home'))