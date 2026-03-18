import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI        = os.getenv('DATABASE_URL', 'sqlite:///students.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG                          = os.getenv('DEBUG', 'False') == 'True'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
