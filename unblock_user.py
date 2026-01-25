from functools import wraps
from flask_login import current_user
from flask import session,abort,request,current_app,flash,redirect,url_for
from application import db
from db_model_mapping import User
from datetime import datetime,timedelta, timezone
from app_extentions import verify_token


 
def unblock_if_expired_l(f):
    @wraps(f)
    def unblock_user_login(*args, **kwargs):
        email = request.form.get("identifier")
        user = User.query.filter_by(email=email).first()
        if user:        

            now = datetime.now(timezone.utc)
            if user.locked_until and user.locked_until > now:
                remaining = int((user.locked_until - now).total_seconds() // 60)
                abort(403, f"Account locked. Try again in {remaining} minutes.")

            
            user.locked_until = None
            db.session.commit()
        return f(*args, **kwargs)

    return unblock_user_login