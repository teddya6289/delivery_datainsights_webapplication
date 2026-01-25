from functools import wraps
from flask_login import current_user,logout_user
from flask import session,redirect,render_template,request,flash,url_for,current_app,abort
from datetime import datetime, timezone
from application import db
from app_extentions import get_safe_redirect


def email_verification(f):
    @wraps(f)
    def check_email_verification(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to log in first!", "danger")
            return redirect(url_for("home"))
        
        if not current_user.email_verified:
            if "post_verify_redirect" not in session:
                session["post_verify_redirect"] = request.full_path

            return redirect(url_for("ev.SendEmail"))

        return f(*args, **kwargs)
    return check_email_verification

def logout_inactive_user(app):
    @app.before_request
    def session_timeout():

        if request.blueprint in {"user", "rp"}:
            return

        if request.endpoint in (None, "static","insights.success"):
            return

        if not current_user.is_authenticated:
            return

        now = datetime.now(timezone.utc)
        last_active = current_user.last_active

        if not last_active:
            current_user.last_active = now
            db.session.commit()
            return

        inactive = current_app.config["INACTIVE_SESSION_TIME"]-(round((now - last_active).total_seconds()))

        if inactive <= 0:
            logout_user()
            abort(401, description = "Session timed out due to inactivity.Please re-authenticate.")
            

        current_user.last_active = now
        db.session.commit()


                 

        

     