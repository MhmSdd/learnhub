# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE= 'Lax'
    SESSION_COOKIE_SECURE= False 
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    LANGUAGES = {
        'en': 'English',
        'ar': 'Arabic'
    }

    BABEL_DEFAULT_LOCALE = 'en'
