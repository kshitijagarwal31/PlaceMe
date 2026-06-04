class Config():
    DEBUG = False 
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    
    
class LocalDevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin123@localhost/placement_portal" 
    DEBUG = True
    
    SECRET_KEY = "secret-key-here"
    SECURITY_PASSWORD_HASH = "argon2"
    SECURITY_PASSWORD_SALT = "password-salt-here"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
    CACHE_TYPE            = "RedisCache"
    CACHE_REDIS_URL       = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX      = ""