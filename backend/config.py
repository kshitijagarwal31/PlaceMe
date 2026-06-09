from dotenv import load_dotenv
import os

load_dotenv()  

class Config():
    DEBUG = False 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = True
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
    CACHE_TYPE            = "RedisCache"
    CACHE_REDIS_URL       = os.getenv("REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX      = ""