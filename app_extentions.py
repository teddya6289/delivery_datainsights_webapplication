
from flask import request, redirect, render_template, url_for,flash,session, current_app,abort
from functools import wraps
from flask_login import current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timezone, timedelta
from app_forms import forgotpasswordform




def is_safe_url(target):
    from urllib.parse import urlparse,urljoin
    ref_url = urlparse(request.host_url)  # app's base URL
    test_url = urlparse(urljoin(request.host_url, target))  # full url
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_safe_redirect(target, default):
    if target and is_safe_url(target):
        return redirect(target)
    return redirect(url_for(default))


def metricfunc(df):
    import io
    import base64
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if df.empty:
         return "Empty dataframe passed!"  
    try:
             
            total_booksold     = int(len(df))
            totalsales         = df["price"].sum()

            top5book_by_genre_df = (df.groupby("genre").size().reset_index(name="no_booksold")
                                    .sort_values("no_booksold",ascending = False).head(5))
             
            bottom5book_by_genre_df = (df.groupby("genre").size().reset_index(name="no_booksold")
                                        .sort_values("no_booksold",ascending = True).head(5))
             

            fig, ax = plt.subplots(figsize = (4,4))
            ax.bar(top5book_by_genre_df["genre"], top5book_by_genre_df["no_booksold"])
            ax.set_title("Top 5 Best Sellers")
            ax.tick_params(axis='x', labelrotation=45)
            fig.tight_layout()
                
            img = io.BytesIO()
            plt.savefig(img, format="png", bbox_inches="tight")
            plt.close(fig)
            img.seek(0)

            fig2, ax2 = plt.subplots(figsize = (4,4))
            ax2.bar(bottom5book_by_genre_df["genre"], bottom5book_by_genre_df["no_booksold"])
            ax2.set_title("Bottom 5 worst Sellers")
            ax2.tick_params(axis='x', labelrotation=45)
            fig2.tight_layout()

            img2 = io.BytesIO()
            plt.savefig(img2, format="png", bbox_inches="tight")
            plt.close(fig2)
            img2.seek(0)


            return base64.b64encode(img.getvalue()).decode("utf-8"), \
                    base64.b64encode(img2.getvalue()).decode("utf-8"), \
                    total_booksold,totalsales

             
    except Exception as error:
            return f"encountered error accessing dataset{error}"

             
    







def getserializer():
    from itsdangerous import URLSafeTimedSerializer
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def generate_verification_token(Email):
        from db_model_mapping import User
        from application import db
        serializer = getserializer()
        user = User.query.filter_by(email=Email).first()
        if not user:
            abort(404,description="User not found")
        token = serializer.dumps(Email, salt='email-verification')
        user.set_hashedtoken(token)
        user.token_sent_at = datetime.now(timezone.utc)
        db.session.commit()
        return token


def verify_token(token, expiration=6000):
            from db_model_mapping import User
            serializer = getserializer()
            try:
                email = serializer.loads(token, salt='email-verification', max_age=expiration)
                user = User.query.filter_by(email=email).first()
                if not user or not user.token_hashed:
                    abort(404,description="Token not found")
                if not user.check_token(token):
                     abort(404,description="Broken Token")
                return user.email
            except:
                return None
                



def generate_userid(firstname, lastname):
    import secrets
    first = str(firstname).strip() 
    last  = str(lastname).strip()
    
    initials = (first[0] if first else "X") + (last[0] if last else "Y")
    random_hex = secrets.token_hex(9).upper()

    return initials + random_hex




def mask_dob(dob):
    from datetime import date, datetime
    if dob is None:
        return None

    if not isinstance(dob, date):
        raise TypeError("dob must be a date")

    return f"**--{dob.month:02d}--**"




limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"])



def limiter_user():
     if current_user.is_authenticated:
          return f"user:{str(current_user.email).lower()}|ip:{get_remote_address()}"
     return f"ip:{get_remote_address()}"



     