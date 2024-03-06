from sqlalchemy import text

from models.student import Student
from models.db_instance import db


def clear_db():
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
    # truncate all tables
    tables = ['deadlines', 'notes', 'selections', 'students', 'supervisors', 'topics', 'types']
    for table in tables:
        db.session.execute(text(f'TRUNCATE TABLE {table};'))
    db.session.commit()

def login():
    print("running topic_filter.py")
    clear_db()

    new_student = Student(
        chinese_name="赵程鑫",
        english_name="Chengxin Zhao",
        class_number="2020180",
        email="2020180@zy",
        password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
        user_name="2020180"
    )
    db.session.add(new_student)
    db.session.commit()

    students = Student.query.all()
    for student in students:
        print(student.chinese_name, student.english_name, student.class_number, student.email, student.password,
              student.user_name)

