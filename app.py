from datetime import timedelta, datetime
from flask import Flask, render_template, request, session
from exts import db
# Import data models
from models.student import Student
from models.supervisor import Supervisor
from models.selection import Selection
from models.topic import Topic
from models.type import Type
from models.deadline import Deadline
from models.note import Note
from models.semester import Semester
from models.report import Report
from models.week import Week
# Import data migration tool
from flask_migrate import Migrate
# Import blueprints
from blueprints.base import bp as base_bp
from blueprints.manager import bp as manager_bp
from blueprints.student import bp as student_bp
from blueprints.supervisor import bp as supervisor_bp
from config import *
from flask_scss import Scss
import secrets
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback
import sys
import glob
import time

'''Database Setup'''
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

# Database migration commands:
# flask db init
# flask db migrate
# flask db upgrade
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(base_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(student_bp)
app.register_blueprint(supervisor_bp)

# Set up log directory
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def cleanup_old_logs():
    """Delete log files older than one week based on filename date"""
    try:
        now = datetime.now()
        one_week_ago = now - timedelta(days=7)

        print(f"\n=== Log Cleanup Debug ===")
        print(f"Current time: {now}")
        print(f"Cutoff date: {one_week_ago} (files older than this will be deleted)")

        log_files = glob.glob(os.path.join(log_dir, '*.log'))
        print(f"Found {len(log_files)} log files:")

        deleted_count = 0
        kept_count = 0
        error_count = 0

        for log_file in log_files:
            try:
                filename = os.path.basename(log_file)
                # YYYY-MM-DD_HH-MM-SS.log
                date_str = filename.split('.')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

                if file_date < one_week_ago:
                    try:
                        os.remove(log_file)
                        print(f"- {filename} => DELETED (created on {file_date})")
                        deleted_count += 1
                    except Exception as e:
                        print(f"- {filename} => DELETE FAILED: {str(e)}")
                        error_count += 1
                else:
                    print(f"- {filename} => KEPT (created on {file_date})")
                    kept_count += 1

            except ValueError:
                print(f"- {filename} => IGNORED (invalid date format)")
                error_count += 1
            except Exception as e:
                print(f"- {filename} => ERROR: {str(e)}")
                error_count += 1

        print(f"\nCleanup summary:")
        print(f"- Deleted: {deleted_count}")
        print(f"- Kept: {kept_count}")
        print(f"- Errors: {error_count}")
        print("=== End Log Cleanup Debug ===\n")

    except Exception as e:
        print(f"CRITICAL ERROR in log cleanup: {str(e)}")


def setup_logging():
    """Configure application logging system"""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'{timestamp}.log'
    log_path = os.path.join(log_dir, log_filename)

    cleanup_old_logs()

    # Custom formatter for request-related logs
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            # For non-request related logs (system messages)
            if not hasattr(record, 'url'):
                return f"{record.asctime} - {record.levelname} - {record.message}"

            # For request-related logs
            return super().format(record)

    # Main log format
    main_formatter = RequestFormatter(
        '%(asctime)s - %(levelname)s - %(user_info)s - %(method)s %(url)s - %(message)s'
    )

    log_level = logging.INFO
    if app.config.get('DEBUG'):
        log_level = logging.DEBUG

    # Main log handler (file)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=1024 * 1024 * 10,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(main_formatter)

    # Console log handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(message)s'))

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove all existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add new handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Disable werkzeug default logging
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.handlers = []
    werkzeug_logger.propagate = False

    return log_path


# Initialize logging configuration
log_file_path = setup_logging()

# Get application logger
logger = logging.getLogger(__name__)


def get_user_info():
    """Get detailed user information including role and username"""
    # If user is logged in (user_id in session)
    if 'user_id' in session:
        user_id = session['user_id']

        # Check user type if available in session
        if 'user_type' in session:
            user_type = session['user_type']

            if user_type == 'student':
                student = Student.query.get(user_id)
                if student:
                    return f"student:{user_id}:{student.user_name}"

            elif user_type == 'supervisor':
                supervisor = Supervisor.query.get(user_id)
                if supervisor:
                    return f"supervisor:{user_id}:{supervisor.user_name}"

            elif user_type == 'manager':
                supervisor = Supervisor.query.get(user_id)
                if supervisor:
                    return f"admin:{user_id}:{supervisor.user_name}"

        # If no user_type in session but user_id exists
        # Try to determine user type by querying database
        student = Student.query.get(user_id)
        if student:
            return f"student:{user_id}:{student.user_name}"

        supervisor = Supervisor.query.get(user_id)
        if supervisor:
            role = "admin" if supervisor.is_admin else "supervisor"
            return f"{role}:{user_id}:{supervisor.user_name}"

        # If neither student nor supervisor but user_id exists
        return f"user:{user_id}"

    # Anonymous user
    return "anonymous"


@app.before_request
def log_request_info():
    """Log request start information"""
    try:
        # Skip static file requests
        if request.path.startswith('/static/'):
            return

        # Get user information
        user_info = get_user_info()

        # Special handling for login attempts
        if request.path == '/login' and request.method == 'POST':
            login_username = request.form.get('username', 'unknown')
            user_info = f"login_attempt:{login_username}"

        logger.info(
            "Request started",
            extra={
                'user_info': user_info,
                'method': request.method,
                'url': request.path
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log request: {str(e)}")


@app.after_request
def log_response_info(response):
    """Log request completion information"""
    try:
        # Skip static file requests
        if request.path.startswith('/static/'):
            return response

        # Special handling for successful login
        if request.path == '/login' and request.method == 'POST' and response.status_code == 200:
            if 'user_id' in session:
                user_info = get_user_info()
                logger.info(
                    f"Login successful - {user_info}",
                    extra={
                        'user_info': user_info,
                        'method': request.method,
                        'url': request.path
                    }
                )
            return response

        logger.info(
            f"Request completed - Status: {response.status_code}",
            extra={
                'user_info': get_user_info(),
                'method': request.method,
                'url': request.path
            }
        )
    except Exception as e:
        logger.warning(f"Failed to log response: {str(e)}")
    return response


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(
        f"404 Not Found: {request.path}",
        extra={
            'user_info': get_user_info(),
            'method': request.method,
            'url': request.path
        }
    )
    return render_template('base/error.html', message='404 NOT FOUND'), 404


@app.errorhandler(Exception)
def handle_generic_error(error):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

    # Log error summary
    logger.error(
        f"Error: {error.__class__.__name__} - {str(error)}",
        extra={
            'user_info': get_user_info(),
            'method': request.method if request else '-',
            'url': request.path if request else '-'
        }
    )

    # Log detailed stack trace
    logger.debug("Stack trace:\n" + ''.join(stack_trace))

    return render_template('base/error.html', message=f'{error.__class__.__name__}, {error}'), 500


# Startup logs
logger.info(f'Application logging configured successfully. Log file: {log_file_path}', extra={
    'user_info': 'system',
    'method': '-',
    'url': '-'
})

if __name__ == '__main__':
    logger.info('Starting application...', extra={
        'user_info': 'system',
        'method': '-',
        'url': '-'
    })
    app.run(debug=True, use_reloader=False)
