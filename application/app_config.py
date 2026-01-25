import os,socket,secrets
from datetime import timedelta
    
    
    
hostname    = socket.gethostname()
password    = os.environ.get("ora_password")
server      = os.environ.get("ora_server")
user        = os.environ.get("ora_user")
port        = os.environ.get("ora_port")
driver      = os.environ.get("driver_mssql")
database    = os.environ.get("database_mssql")


class Config(object):

    SECRET_KEY = secrets.token_hex(16)

    SQLALCHEMY_DATABASE_URI = (f'oracle+oracledb://{user}:{password}@{hostname}:{port}/?service_name={server}')

    SQLALCHEMY_BINDS = {"db_2": 'mssql+pyodbc://@TEDDYPC/Mydb?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'}

    MAIL_SERVER = f'{hostname}'
    MAIL_PORT =     1025
    MAIL_USE_TLS =  False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'no-reply@enterprisedelivery.com'

    VERIFIED_EMAIL_TIMEOUT = 300
    INACTIVE_SESSION_TIME = 600
    TOKEN_EXPIRED = 150

    MAX_ATTEMPTS = 3
    LOCK_DURATION = timedelta(minutes=15) 