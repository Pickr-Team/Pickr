from datetime import timedelta, datetime

from flask import Flask, render_template
from exts import db
# import data model
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.topic import Topic
from models.type import Type
from models.deadline import Deadline
from models.semester import Semester
from models.report import Report
# import data migration tool
from flask_migrate import Migrate
# import blueprints
from blueprints.base import bp as base_bp
from blueprints.manager import bp as manager_bp
from blueprints.student import bp as student_bp
from blueprints.supervisor import bp as supervisor_bp
from config import *
from flask_scss import Scss
import secrets
import os
import logging
import traceback
import sys

'''Set up database'''
# Read flask environment variable to determine which database to use
if os.environ.get('FLASK_ENV') == 'production':
    app = Flask(__name__, static_url_path='/studentprojectmanager/static')
    config = ProdConfig
elif os.environ.get('FLASK_ENV') == 'test':
    app = Flask(__name__)
    config = TestConfig
else:
    app = Flask(__name__)
    config = DevConfig

app.config.from_object(config)
Scss(app, static_dir='static/css', asset_dir='assets')
app.secret_key = secrets.token_hex(16)
db.init_app(app)

# flask db init
# flask db migrate
# flask db upgrade
migrate = Migrate(app, db)

app.register_blueprint(base_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(student_bp)
app.register_blueprint(supervisor_bp)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app.jinja_env.globals['timedelta'] = timedelta
app.jinja_env.globals['datetime'] = datetime


# Catch 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base/error.html', message='404 NOT FOUND'), 404


@app.errorhandler(Exception)
def handle_generic_error(error):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.error(f"Error Name: {error.__class__.__name__}")
    logger.error(f"Error Message: {str(error)}")

    for line in stack_trace:
        logger.error(line.strip())

    return render_template('base/error.html', message='Internal server error'), 500


if __name__ == '__main__':
    app.run()
