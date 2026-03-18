import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI        = os.getenv('DATABASE_URL', 'sqlite:///enrollments.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG                          = os.getenv('DEBUG', 'False') == 'True'
    STUDENT_SERVICE_URL            = os.getenv('STUDENT_SERVICE_URL', 'http://localhost:8001')
    COURSE_SERVICE_URL             = os.getenv('COURSE_SERVICE_URL',  'http://localhost:8002')
    TIMEOUT_SECONDS                = int(os.getenv('TIMEOUT_SECONDS', '3'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
