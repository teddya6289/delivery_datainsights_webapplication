from flask import Flask, render_template,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_login import LoginManager,logout_user,current_user
from application.app_config import Config





db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()
login_manager = LoginManager()


def analytic_report_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app_extentions import limiter
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)


    from db_model_mapping import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get((user_id))
    
#   Register logout inactive user
    
    from .route_security import logout_inactive_user
    logout_inactive_user(app)
    

# Registry Blueprint for modular route structuring
    
    from .Blueprint_app_route import app_routes_bp
    from .Blueprint_user import useraccess_bp
    from emailverification import send_verify_email_bp
    from .forgotpassword import forgotpassword_bp
    app.register_blueprint(app_routes_bp)
    app.register_blueprint(useraccess_bp)
    app.register_blueprint(send_verify_email_bp)
    app.register_blueprint(forgotpassword_bp)

    from flask_limiter.errors import RateLimitExceeded
    @app.errorhandler(RateLimitExceeded)
    def handle_errorslimiter(error):
        if request.endpoint == "insights.book_catalogue":
            current_user.email_verified = False
            db.session.commit()
            session.pop("email_verfied_at",None)
            session.modified = True
        logout_user()
        return render_template(
            "error.html",
            code=error.code,
            message=error.description or "An unexpected error occurred."
        ), error.code
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(429)
    def handle_errors(error):
        return render_template(
            "error.html",
            code=error.code,
            message=error.description or "An unexpected error occurred."
        ), error.code
    print(app.url_map)
    return app