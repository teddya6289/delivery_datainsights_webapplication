
from application import mail,db
from flask import request,render_template,redirect,url_for, flash,Blueprint,session,current_app,abort
from db_model_mapping import  User
from sqlalchemy import or_
from app_extentions import verify_token, generate_verification_token, get_safe_redirect
from flask_login import login_required,current_user,logout_user
from flask_mail import Message
from datetime import datetime, timezone


send_verify_email_bp = Blueprint('ev',__name__)

@send_verify_email_bp.route('/SendEmail', methods=['GET','POST'])
@login_required
def SendEmail():
    if current_user.is_authenticated:
                email =     current_user.email
                if not email:
                            logout_user()
                            abort(401, description="Invalid e-address.")
                
                if current_user.email_verified:
                    flash("Email already verified.", "info")
                    return redirect(url_for("insights.book_catalogue"))
                
                token = generate_verification_token(email)
                
                verification_url = url_for('ev.verifyEmail', token=token, _external=True)

                subject = "Verify Your Email"
                body = f"""
                        <p> An attempt was initiated to update a patient record.</p>
                        <p> To proceed click the link <a href = "{verification_url}"> Verify Email </a></p>
                        <p> If you did not initiated this request, Please ignore the message. Thank you</p>
                        """
                try:
                    msg = Message(subject=subject,sender='no-reply@example.com',recipients=[email], html=body)
                    mail.send(msg)
                    return redirect(url_for("insights.success",
                                    code = 200, 
                                    message ="Email Verification Required:link have been sent to the registered email address"))

                    
                    
                
                except Exception as e:
                    abort(401,description = "Failed to send verification email")
                   
                
                
            
    else:
        flash ("Ooops! Request encountered an error","danger")
        logout_user()
        return redirect(url_for('insights.home'))
    
        
       
@send_verify_email_bp.route('/verifyEmail/<token>', methods = ['GET', 'POST'])
def verifyEmail(token):
            email = verify_token(token)
            now = datetime.now(timezone.utc)
            if current_user.is_authenticated:
                Expired_token_timer = current_app.config["TOKEN_EXPIRED"]
                token_time_left = Expired_token_timer-(round((now - current_user.token_sent_at).total_seconds()))
                if token_time_left <= 0:
                    current_user.token_hashed = None
                    current_user.token_sent_at = None
                    db.session.commit()
                    abort(401,description = "Link expired!!!. Please request a new one.")
                    
                    
                
                if request.method == 'POST':
                        
                                        verified_user=User.query.filter_by(email=email).first()
                                        if verified_user:
                                            verified_user.email_verified = True
                                            session["email_verified_at"] = datetime.now(timezone.utc)
                                            db.session.commit()
                                            flash("Email verified successfully","success")
                                            next_page = session.pop("post_verify_redirect", None)
                                            if next_page and get_safe_redirect(next_page, "insights.catalogue"):
                                                return redirect(next_page)
                                        else:
                                            abort(404,description = "User Not Found")
                                            
                        
            return render_template('verifyemail.html', email = email)
                
                        
