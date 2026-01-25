from application import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timezone




class BookTable(db.Model):
    __tablename__   = "book_store"
    ups             = db.Column(db.String(100), primary_key=True)
    title           = db.Column(db.String(4000))
    genre           = db.Column(db.String(100))
    price           = db.Column(db.Numeric(10, 2))



class User(db.Model,UserMixin):
    __bind_key__    = "db_2"
    __tablename__   = "users"
    
    userid              = db.Column(db.String(100),primary_key=True)
    firstname           = db.Column(db.String(50))
    lastname            = db.Column(db.String(50))
    dateofbirth         = db.Column(db.Date)
    email               = db.Column(db.String(100))
    hashpassword        = db.Column(db.String(100))
    jobtitle            = db.Column(db.String(100))
    email_verified      = db.Column(db.Boolean, default=False, nullable=False)
    failed_attempts     = db.Column(db.Integer, default=0)
    locked_until        = db.Column(db.DateTime(timezone=True), nullable=True)
    last_active         = db.Column(db.DateTime(timezone=True))
    token_hashed        = db.Column(db.String(250),nullable=True)
    token_sent_at       = db.Column(db.DateTime(timezone=True))

    def get_id(self):
        return str(self.userid)

    def set_password(self, password):
        self.hashpassword = generate_password_hash(password)

    def set_hashedtoken(self, token):
        self.token_hashed= generate_password_hash(token)

    def check_token(self, token):
        return check_password_hash(self.token_hashed, token)
    

    def check_password(self, password):
        return check_password_hash(self.hashpassword, password)

    @property
    def password(self):
        raise AttributeError("Invalid access")

    @password.setter
    def password(self, password):
        self.set_password(password)