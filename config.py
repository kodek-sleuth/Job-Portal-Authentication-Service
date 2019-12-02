import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

class Development(Config):
    debug = True
    MONGODB_SETTINGS = {'db': os.getenv("DATABASE"), 'host': os.getenv("HOST"), 'port': int(os.getenv("PORT"))}

class Testing(Config):
    MONGODB_SETTINGS = {'db': os.getenv("DATABASE_TEST"), 'host': os.getenv("HOST"), 'port': int(os.getenv("PORT"))}

class Production(Config):
    MONGODB_SETTINGS = {'db': os.getenv("DATABASE_PROD"), 'host': os.getenv("HOST"), 'port': int(os.getenv("PORT"))}


app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production
}

