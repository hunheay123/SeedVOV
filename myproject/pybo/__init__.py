from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    #블루프린트
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app

# @app.route('/')
   # def hello_pybo():
   #     return 'Hello, P1asdaf3111' # Hello Pybo! 를 출력

    #if __name__ == '__main__':
      #  app.run(debug=True)

# $env:FLASK_APP = "pybo.py" 하고 flask run 해야 됨
# 그냥 위에 재생 눌러도 됨