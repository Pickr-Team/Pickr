from datetime import datetime
from unittest import TestCase
from flask import Flask
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
from config import *
from exts import db
from models.report import Report


class TestReport(TestCase):
    student_id = None  # Store IDs instead of objects
    week_id = None
    app = None
    db = None
    semester_id = None
    topic_id = None
    supervisor_id = None

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config.from_object(TestConfig)
        cls.db = db
        cls.db.init_app(cls.app)
        with cls.app.app_context():
            cls.db.create_all()

            # Create and commit student
            student = Student(
                chinese_name='张三',
                english_name='zhangsan',
                email='zhangsan@example.com',
                password='password123',
                user_name='zhangsan',
                class_number='CS101',
                graduation_year=2025
            )
            cls.db.session.add(student)
            cls.db.session.commit()
            cls.student_id = student.id  # Store just the ID

            # Create and commit semester
            semester = Semester(2025, '', '')
            cls.db.session.add(semester)
            cls.db.session.commit()
            cls.semester_id = semester.id

            # Create and commit week
            week = Week(1, '', 1, '', cls.semester_id, 1)
            cls.db.session.add(week)
            cls.db.session.commit()
            cls.week_id = week.id

            supervisor = Supervisor('Supervisor', 'One', False, 10, 'supervisor1', '123456', None, None)
            cls.db.session.add(supervisor)
            cls.db.session.commit()
            cls.supervisor_id = supervisor.id

            topic = Topic(quota=999, is_custom=False, required_skills=None, reference=None,
                          name='topic 1', supervisor_id=cls.supervisor_id, description=None, type_id=None)
            cls.db.session.add(topic)
            cls.db.session.commit()
            cls.topic_id = topic.id

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.drop_all()

    # clear data after each test
    def tearDown(self):
        with self.app.app_context():
            self.db.session.query(Report).delete()
            self.db.session.commit()

    def test_add(self):
        with self.app.app_context():
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_report = Report(
                student_id=self.student_id,  # Use stored ID
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id  # Use stored ID
            )
            new_report.add()

            # Verify the report was added
            report = Report.query.filter_by(student_id=self.student_id).first()
            self.assertIsNotNone(report)
            self.assertEqual(report.week_id, self.week_id)

    def test_get_all_by_student_id(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()

            # Test the method
            reports = Report.get_all_by_student_id(self.student_id)
            self.assertEqual(len(reports), 1)  # Expected :2  Actual   :1
            self.assertEqual(reports[0].student_id, self.student_id)

    def test_get_by_week_id(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()

            # Test the method
            found_report = Report.get_by_week_id(self.week_id)
            self.assertIsNotNone(found_report)
            self.assertEqual(found_report.week_id, self.week_id)

    def test_mark_as_read(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id,
                is_read=0  # Initially unread
            )
            report.add()

            # Test the method
            report.mark_as_read()
            updated_report = Report.query.get(report.id)
            self.assertEqual(updated_report.is_read, 1)

    def test_semester_property(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()

            # Test the property
            self.assertEqual(report.semester.id, self.semester_id)

    def test_get_all_by_supervisor_id(self):
        with self.app.app_context():
            # Create a selection linking student to supervisor
            selection = Selection(
                student_id=self.student_id,
            )
            selection.add()
            selection.update_status(4)
            selection.update_final_topic_id(self.topic_id)

            # Add a report for the student
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()

            # Test the method
            reports = Report.get_all_by_supervisor_id(self.supervisor_id)
            self.assertEqual(len(reports), 1)
            self.assertEqual(reports[0].student_id, self.student_id)

    def test_update(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id,
                current_plan="Initial plan",
                is_read=0
            )
            report.add()

            # Test updating multiple fields
            new_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report.update(
                update_time=new_time,
                current_plan="Updated plan",
                is_read=1
            )

            # Verify the updates
            updated_report = Report.query.get(report.id)
            self.assertEqual(updated_report.update_time, new_time)
            self.assertEqual(updated_report.current_plan, "Updated plan")
            self.assertEqual(updated_report.is_read, 1)

    def test_delete(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()
            report_id = report.id

            # Verify it exists
            self.assertIsNotNone(Report.query.get(report_id))

            # Test deletion
            report.delete()

            # Verify it's deleted
            self.assertIsNone(Report.query.get(report_id))

    def test_get_by_id(self):
        with self.app.app_context():
            # First add a report
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            report = Report(
                student_id=self.student_id,
                submit_time=current_time,
                update_time=current_time,
                week_id=self.week_id
            )
            report.add()

            # Test the method
            found_report = Report.get_by_id(report.id)
            self.assertIsNotNone(found_report)
            self.assertEqual(found_report.id, report.id)
            self.assertEqual(found_report.student_id, self.student_id)

    def test_get_all(self):
        with self.app.app_context():
            # Clear any existing reports
            self.db.session.query(Report).delete()
            self.db.session.commit()

            # Add multiple reports
            for i in range(3):
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = Report(
                    student_id=self.student_id,
                    submit_time=current_time,
                    update_time=current_time,
                    week_id=self.week_id,
                    current_plan=f"Plan {i}"
                )
                report.add()

            # Test the method
            all_reports = Report.get_all()
            self.assertEqual(len(all_reports), 3)

            # Verify they're ordered by ID descending
            self.assertGreater(all_reports[0].id, all_reports[1].id)
            self.assertGreater(all_reports[1].id, all_reports[2].id)

    def test_get_num(self):
        with self.app.app_context():
            # Clear any existing reports
            self.db.session.query(Report).delete()
            self.db.session.commit()

            # Add some reports
            for i in range(4):
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                report = Report(
                    student_id=self.student_id,
                    submit_time=current_time,
                    update_time=current_time,
                    week_id=self.week_id
                )
                report.add()

            # Test the method
            self.assertEqual(Report.get_num(), 4)