import pytest
from flask import Flask, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
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
from blueprints.base import bp as base_bp
from blueprints.manager import bp as manager_bp
from blueprints.student import bp as student_bp
from blueprints.supervisor import bp as supervisor_bp


# pip install pytest-mock

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy()
    db.init_app(app)

    app.register_blueprint(base_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(supervisor_bp)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_student():
    return {'id': 1, 'user_name': 'test_student', 'user_type': 'student'}


@pytest.fixture
def test_week():
    return {'id': 1, 'week_num': 1, 'requires_report': True}


def test_handle_report_create_new(client, test_student, test_week, mocker):
    # Mock the session and database operations
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = test_student['id']
            sess['user_name'] = test_student['user_name']
            sess['user_type'] = test_student['user_type']

        # Mock the Report.query.filter_by().first() to return None (no existing report)
        mocker.patch.object(Report, 'query')
        mocker.patch.object(Report.query, 'filter_by')
        mocker.patch.object(Report.query.filter_by(), 'first', return_value=None)

        # Mock the add method
        mock_add = mocker.patch.object(Report, 'add')

        # Prepare form data
        form_data = ImmutableMultiDict([
            ('week_id', str(test_week['id'])),
            ('action', 'create'),
            ('current_plan', 'Test current plan'),
            ('next_plan', 'Test next plan'),
            ('issues', 'Test issues'),
            ('feedback', 'Test feedback')
        ])

        # Mock datetime.now() to return a fixed time
        fixed_time = datetime(2023, 1, 1, 12, 0, 0)
        mocker.patch('datetime.datetime', return_value=fixed_time)
        mocker.patch('datetime.datetime.now', return_value=fixed_time)

        # Mock url_for to return a fixed URL
        mock_url_for = mocker.patch('flask.url_for')
        mock_url_for.return_value = '/student/home'

        # Call the endpoint
        response = client.post('/student/handle_report', data=form_data)

        # Assertions
        assert response.status_code == 302

        # Verify the redirect location matches expected
        assert response.location == '/student/home'

        # Verify the Report was created with correct data
        assert Report.query.filter_by().first.call_count == 1
        assert mock_add.call_count == 1

        # Verify url_for was called with correct endpoint
        # mock_url_for.assert_called_once_with('student.index')


def test_handle_report_create_existing(client, test_student, test_week, mocker):
    # Mock the session and database operations
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = test_student['id']
            sess['user_name'] = test_student['user_name']
            sess['user_type'] = test_student['user_type']

        # Mock an existing report
        mock_report = mocker.MagicMock()
        mocker.patch.object(Report, 'query')
        mocker.patch.object(Report.query, 'filter_by')
        mocker.patch.object(Report.query.filter_by(), 'first', return_value=mock_report)

        # Prepare form data
        form_data = ImmutableMultiDict([
            ('week_id', str(test_week['id'])),
            ('action', 'create'),
            ('current_plan', 'Test current plan'),
            ('next_plan', 'Test next plan'),
            ('issues', 'Test issues'),
            ('feedback', 'Test feedback')
        ])

        # Call the endpoint
        response = client.post('/student/handle_report', data=form_data)

        # Assertions
        assert response.status_code == 400
        assert b"Report already exists. Use update instead." in response.data


def test_handle_report_update_success(client, test_student, test_week, mocker):
    # Mock the session and database operations
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = test_student['id']
            sess['user_name'] = test_student['user_name']
            sess['user_type'] = test_student['user_type']

        # Mock an existing report
        mock_report = mocker.MagicMock()
        mocker.patch.object(Report, 'query')
        mocker.patch.object(Report.query, 'filter_by')
        mocker.patch.object(Report.query.filter_by(), 'first', return_value=mock_report)

        # Mock the update method
        mock_update = mocker.patch.object(mock_report, 'update')

        # Prepare form data
        form_data = ImmutableMultiDict([
            ('week_id', str(test_week['id'])),
            ('action', 'update'),
            ('current_plan', 'Updated current plan'),
            ('next_plan', 'Updated next plan'),
            ('issues', 'Updated issues'),
            ('feedback', 'Updated feedback')
        ])

        # Mock datetime.now() to return a fixed time
        fixed_time = datetime.now()

        datetime_mock = mocker.patch('datetime.datetime')
        datetime_mock.now.return_value = fixed_time

        # Mock redirect
        mock_redirect = mocker.patch('flask.redirect')

        # Call the endpoint
        response = client.post('/student/handle_report', data=form_data)

        # Assertions
        assert response.status_code == 302

        # Verify the report was updated with correct data
        mock_update.assert_called_once_with(
            current_plan='Updated current plan',
            next_plan='Updated next plan',
            issues='Updated issues',
            feedback='Updated feedback',
            update_time=fixed_time.strftime('%Y-%m-%d %H:%M:%S')
        )


def test_handle_report_update_not_found(client, test_student, test_week, mocker):
    # Mock the session and database operations
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = test_student['id']
            sess['user_name'] = test_student['user_name']
            sess['user_type'] = test_student['user_type']

        # Mock no existing report
        mocker.patch.object(Report, 'query')
        mocker.patch.object(Report.query, 'filter_by')
        mocker.patch.object(Report.query.filter_by(), 'first', return_value=None)

        # Prepare form data
        form_data = ImmutableMultiDict([
            ('week_id', str(test_week['id'])),
            ('action', 'update'),
            ('current_plan', 'Updated current plan'),
            ('next_plan', 'Updated next plan'),
            ('issues', 'Updated issues'),
            ('feedback', 'Updated feedback')
        ])

        # Call the endpoint
        response = client.post('/student/handle_report', data=form_data)

        # Assertions
        assert response.status_code == 404
        assert b"Report not found. Create it first." in response.data


@pytest.fixture
def test_supervisor():
    return {'id': 1, 'user_name': 'test_supervisor', 'user_type': 'supervisor'}


@pytest.fixture
def test_topic(test_supervisor):
    return {
        'id': 1,
        'name': 'Test Topic',
        'supervisor_id': test_supervisor['id'],
        'quota': 1,
        'is_custom': False
    }


@pytest.fixture
def test_selection(test_student, test_topic):
    return {
        'id': 1,
        'student_id': test_student['id'],
        'final_topic_id': test_topic['id'],
        'status': 4  # success(Supervisor's Topic)
    }


@pytest.fixture
def test_report(test_student, test_week):
    return {
        'id': 1,
        'student_id': test_student['id'],
        'week_id': test_week['id'],
        'submit_time': '2023-01-01 12:00:00',
        'update_time': '2023-01-01 12:00:00',
        'is_read': 0,
        'current_plan': 'Test plan',
        'next_plan': 'Test next plan',
        'issues': 'Test issues',
        'feedback': 'Test feedback'
    }


def test_supervisor_comment_on_report(client, test_supervisor, test_student,
                                      test_topic, test_selection, test_report, mocker):
    # Mock the session (supervisor logged in)
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = test_supervisor['id']
            sess['user_name'] = test_supervisor['user_name']
            sess['user_type'] = test_supervisor['user_type']

        # Mock database operations
        # 1. Mock the report exists
        mock_report = mocker.MagicMock()
        mocker.patch.object(Report, 'get_by_id', return_value=mock_report)

        # 2. Mock the update method
        mock_update = mocker.patch.object(mock_report, 'update')

        # Prepare JSON data
        comment_data = {
            'report_id': test_report['id'],
            'comments': 'This is a test comment from supervisor'
        }

        # Call the endpoint
        response = client.post(
            '/supervisor/report/comments',
            json=comment_data,
            content_type='application/json'
        )

        # Assertions
        assert response.status_code == 200
        assert b"Provide feedback successfully" in response.data

        # Verify the report was updated with correct comment
        mock_update.assert_called_once_with(comments=comment_data['comments'])

        # Verify the report was retrieved with correct ID
        Report.get_by_id.assert_called_once_with(test_report['id'])