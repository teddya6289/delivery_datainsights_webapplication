from application import db,mail
from db_model_mapping import User
from app_forms import changepasswordform, forgotpasswordform,verifyageform
from flask import (render_template,redirect,request,Blueprint,flash,abort,url_for,session,current_app)
from flask_login import current_user
from flask_mail import Message
from datetime import datetime, timezone,timedelta
from app_extentions import verify_token, limiter,limiter_user


forgotpassword_bp = Blueprint("rp",__name__)


@forgotpassword_bp.route("/forgotpassword", methods=["GET","POST"])
@limiter.limit("10 per hour", key_func= lambda:request.form.get("email"))
def forgotpassword():
    from app_extentions import generate_verification_token
    forgot_p_form = forgotpasswordform()
    if forgot_p_form.validate_on_submit():
                now = datetime.now(timezone.utc)
                Email = forgot_p_form.email.data
                stranded_user = User.query.filter_by(email = Email).first()
                if not stranded_user:
                    flash("E-address not valid!!!","danger")
                    return redirect(url_for("rp.forgotpassword"))
                if stranded_user.locked_until and stranded_user.locked_until > now:
                    abort(404,description = f":Account locked!!!.Too many failed attempts.Access unlocks in:\
                          {round((stranded_user.locked_until-now).total_seconds() // 60)} minutes")
                try:
                        token = generate_verification_token(stranded_user.email)
                        verification_url = url_for('rp.resetpassword', token=token, _external=True)

                        subject = "Password reset"
                        body = f"""
                                    <p> Password reset have been initiated To proceed click 
                                    <a href = "{verification_url}">
                                    here </a><br>
                                    If you did not initiated this request, Please ignore the message.Thank you</p>
                                    """
                        msg = Message(subject=subject,sender='no-reply@enterprisedelivery.com',recipients=[Email], html=body)
                        mail.send(msg)
                        return redirect(url_for("insights.success",code = 200,
                        message = "An email with a link have been sent to your registered email.Please follow the instruction"))
                    
                except Exception as e:
                        abort(401,
                        description=f":Failed to send send reset password link.{e}")
                    
                else:    
                    abort(404,description="E-address not valid")    
                       
                    

    return render_template("forgotpassword.html", form = forgot_p_form)
        




@forgotpassword_bp.route("/resetpassword/<token>", methods = ["GET","POST"])
@limiter.limit("25 per hour")
def resetpassword(token):
    from app_extentions import mask_dob
    
    email = verify_token(token)
    if not email:
        abort(403,description="Invalid email provided")
    now = datetime.now(timezone.utc)
    user = User.query.filter_by(email=email).first()
    
    if not user:
         abort(404, description="Unauthorized user!")
    
    Expired_token_timer = current_app.config["TOKEN_EXPIRED"]
    token_time_left = Expired_token_timer-(round((now - user.token_sent_at).total_seconds()))
    
    if token_time_left <= 0:
            session.pop("dob_verified", None)
            session.pop("password_reset_count", None)
            session.modified = True
            user.token_hashed = None
            user.token_sent_at = None
            db.session.commit()
            abort(401,description=":Reset password request session expired. Please close the page and create a new request.")
    
    if user.locked_until and user.locked_until > now:
        abort(403,description = f":Account locked!!!.Too many failed attempts.Access unlocks in:{round((user.locked_until-now).total_seconds() // 60)} minutes") 
     
    try:
        mask_date = mask_dob(user.dateofbirth) 
        if "password_reset_count" not in session:
            session["password_reset_count"] = 0
        vetdob_form = verifyageform()
        
        if vetdob_form.validate_on_submit():
                    
                        if user.dateofbirth == vetdob_form.dateofbirth.data:
                            session.pop("password_reset_count",None)
                            session["dob_verified"] =  True
                            session.modified = True
                            flash ("User authenticated for password reset","success")
                            return redirect(url_for("rp.changepassword",token=token))
                        
                        
                        session["password_reset_count"] += 1
                        session.modified = True
                        if session.get("password_reset_count") >= 3:
                            user.locked_until = now + timedelta(minutes= 10)
                            session["user_block_at"] = datetime.now(timezone.utc)
                            db.session.commit()
                            
                            abort(401,description = f":Account locked for {timedelta(minutes= 10).seconds//60}!!! Too many failed attempts.")
                            
                            
                        else:
                            flash(f"Invalid credentials.Attempt {session['password_reset_count']} of {3}.", "warning")
                                
    except Exception as e:
        abort(401,description = f"{e}")
        
        

    return render_template("resetpassword.html",Mask_d = mask_date, form = vetdob_form,token=token,
                            token_time_left=token_time_left)




@forgotpassword_bp.route("/changepassword/<token>", methods = ["GET","POST"])
def changepassword(token):
    email = verify_token(token)
    
    if not email:
          abort(403,description=":Unauthorized!.User missing session requirement.")

    if not session.get("dob_verified"):
         abort(403,description=":Unauthorized!.User missing session requirement.")
    
    now = datetime.now(timezone.utc)
    user = User.query.filter_by(email = email).first()
    Expired_token_timer = current_app.config["TOKEN_EXPIRED"]
    token_time_left = Expired_token_timer-(round((now - user.token_sent_at).total_seconds()))
    
    
    if user:
            cp_form = changepasswordform()
            if cp_form.validate_on_submit():
                    try:

                        user.set_password(cp_form.new_password.data)
                        user.locked_until = None
                        session.pop("dob_verified", None)
                        session.pop("password_reset_count", None)
                        session.modified = True
                        user.token_hashed = None
                        user.token_sent_at = None
                        db.session.commit()
                        return redirect(url_for("insights.success", code = 203,
                                                message ="Password have been changed successfully",))
                    except Exception as error:
                         abort(403,description =":Password reset failed")
    else:                    
        abort(404,description="User not found")                     
            
                        
    return render_template("changepassword.html",form = cp_form, token = token, token_time_left=token_time_left)

               