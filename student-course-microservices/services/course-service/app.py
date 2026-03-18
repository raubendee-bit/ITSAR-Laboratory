from flask import Flask
from flask_cors import CORS
from config import DevelopmentConfig
from models import db
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    CORS(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8002)
