# from functools import wraps
# from flask_login import current_user
# from flask import session,abort,request
# from application import db
# from db_model_mapping import User
# from datetime import datetime,timedelta, timezone
# from app_extentions import verify_token

# def unblock_if_expired(f):
#     @wraps(f)
#     def unblock_user_pr_abuse(*args, **kwargs):
#         token = kwargs.get("token")
#         if not token:
#             abort(400,description = "ERROR")

#         email = verify_token(token)
#         if not email:
#             abort(401,description = "Invalid email address")

#         user = User.query.filter_by(email=email).first()
#         if not user:
#             abort(404,"Unauthorised User")

#         now = datetime.now(timezone.utc)
#         if user.locked_until and user.locked_until > now:
#             remaining = int((user.locked_until - now).total_seconds() // 60)
#             abort(403, f"Account locked. Try again in {remaining} minutes.")

#         if user.locked_until and user.locked_until <= now:
#             user.locked_until = None
#             session.pop("user_block_at", None)
#             db.session.commit()
        
        

#         return f(*args, **kwargs)

#     return unblock_user_pr_abuse
 


# def unblock_if_expired_l(f):
#     @wraps(f)
#     def unblock_user_login(*args, **kwargs):
#         email = request.form.get("identifier")
#         user = User.query.filter_by(email=email).first()
#         if not user:
#             abort(404,"Unauthorised User")

#         now = datetime.now(timezone.utc)
#         if user.locked_until and user.locked_until > now:
#             remaining = int((user.locked_until - now).total_seconds() // 60)
#             abort(403, f"Account locked. Try again in {remaining} minutes.")

#         if user.locked_until and user.locked_until <= now:
#             user.locked_until = None
#             session.pop("user_block_at", None)
#             db.session.commit()
        
        

#         return f(*args, **kwargs)

#     return unblock_user_login