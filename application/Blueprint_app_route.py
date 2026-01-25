from flask import request,render_template,redirect,url_for, flash,Blueprint,session,current_app,abort
from application import db
from flask_login import login_required,current_user,logout_user
from .route_security import email_verification
from app_extentions import limiter,limiter_user
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import calendar


app_routes_bp = Blueprint('insights',__name__)




@app_routes_bp.before_request
def email_verified_timeout():
     from datetime import datetime, timezone,timedelta
     exempted_endpoints = {"insights.home"}

     if request.endpoint in exempted_endpoints:
          return
     if current_user.is_authenticated:
          now = datetime.now(timezone.utc)
          if current_user.locked_until and current_user.locked_until > now:
               abort(403,description = f":Account locked for {timedelta(minutes= 10).seconds//60}\
                    minutes.Too many failed attempts.Time left:{(current_user.locked_until-now).total_seconds() // 60} minutes") 
          verified_at = session.get("email_verified_at")
          if verified_at:
               check_expired_email_verification = current_app.config['VERIFIED_EMAIL_TIMEOUT'] - (round((now - verified_at).total_seconds()))
               if check_expired_email_verification <= 0:
                    current_user.email_verified = False
                    db.session.commit()
                    session.pop("email_verified_at",None)
                    session.modified = True
                    abort(401,description="Session for verified email expired.Please reverify email address to proceed")
                    
                    


# ROUTE 1  View Book Inventory
    
@app_routes_bp.route("/book_catalogue",methods=["GET"])
@login_required
@email_verification
@limiter.limit("10 per hour",key_func=limiter_user)
def book_catalogue():
          from app_extentions import metricfunc
          from db_model_mapping import BookTable
          import pandas as pd     


          current_month = calendar.month_name[datetime.now(ZoneInfo("America/Edmonton")).month]
          query = db.session.query(
                                    BookTable.genre,
                                    BookTable.price
                                    )
          df = pd.DataFrame(query.all(), columns=["genre", "price"])
            
          if df.empty:
                flash('Oops! Could not retrieve record. Please consult admin', 'warning')
                return redirect(url_for('insights.home'))
          username = (current_user.firstname).upper()
          jobtitle = current_user.jobtitle

           
          try:
                    
                    
                    
                    
                    graph_top5sellers,graph_bottom5worstsellers,totalbooksold,totalsales = metricfunc(df)
                    
                    return render_template('viewbookcatalogue.html',
                                        top5sellers=graph_top5sellers,
                                        bottom5worstsellers=graph_bottom5worstsellers,
                                        totalbooksold=totalbooksold,
                                        totalsales=totalsales,username=username,jobtitle=jobtitle,
                                        current_month = current_month)
                                    
          except Exception as e:
               abort(403,description=f"Error displaying catalogue{e}")
                                
                        

    
    
# ROUTE 2 Home page
  
@app_routes_bp.route("/")
def home():
        # return "PRINT. TESTING IF APP CAN DETECT ROUTES"
        return render_template("home.html")

@app_routes_bp.route("/success/<int:code>/<string:message>")
def success(code,message):
     s_code = code
     s_message = message
     return render_template("success.html",s_code=s_code,s_message=s_message)