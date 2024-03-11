from sqlalchemy import text
import random
from datetime import timedelta, datetime

from models.selection import Selection
from models.student import Student
from models.db_instance import db
from models.supervisor import Supervisor
from models.topic import Topic
from models.type import Type


def clear_db():
    db.session.execute(text('SET FOREIGN_KEY_CHECKS = 0;'))
    tables = ['notes', 'selections', 'students', 'supervisors', 'topics', 'types']
    for table in tables:
        db.session.execute(text(f'TRUNCATE TABLE {table};'))
    db.session.commit()


def creat_one_student():
    new_student = Student(
        chinese_name="赵程鑫",
        english_name="Chengxin Zhao",
        class_number="2020180",
        email="2020180@zy",
        password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
        user_name="202018020317"
    )
    new_student.add()


def create_one_supervisor():
    new_supervisor = Supervisor(
        first_name="Li",
        last_name="Clivia",
        is_admin=0,
        position=4,
        user_name="clivia",
        password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        email="clivia@zy.cdut.edu.cn"
    )
    new_supervisor.add()


def create_one_manager():
    new_supervisor = Supervisor(
        first_name="Walker",
        last_name="Joojo",
        is_admin=1,
        position=0,
        user_name="Joojo",
        password="8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92",
        email="clivia@zy.cdut.edu.cn"
    )
    new_supervisor.add()


def random_int_20():
    import random
    return random.randint(1, 20)


def random_int_5():
    import random
    return random.randint(1, 5)


def random_int_10():
    import random
    return random.randint(1, 10)


def random_int_10_exclude_1():
    result = random.randint(1, 9)
    if result >= 1:
        result += 1
    return result


def create_types():
    for i in range(11):
        new_type = Type(name=f'type{i}')
        new_type.add()


def create_topics():
    for i in range(51):
        new_topic = Topic(
            name=f'topic{i}',
            supervisor_id=random_int_10(),
            quota=random_int_5(),
            is_custom=0,
            type_id=random_int_10(),
            description='description',
            required_skills='required_skills',
            reference='reference'
        )
        new_topic.add()


def create_supervisors():
    for i in range(11):
        new_supervisor = Supervisor(
            first_name=f'first_name{i}',
            last_name=f'last_name{i}',
            is_admin=0,
            position=random_int_5(),
            user_name=f'user_name{i}',
            password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
            email=f'email{i}',
        )
        new_supervisor.add()


def create_students():
    for i in range(151):
        new_student = Student(
            chinese_name=f'Student{i}',
            english_name=f'name{i}',
            class_number=f'2020180{i}',
            email=f'2020180@zy{i}',
            password='8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
            user_name=f'202018020317{i}'
        )
        new_student.add()


def initSelections():
    base_time = datetime.strptime('2021-06-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    for i in range(130):
        new_selection = Selection(
            student_id=i,
        )
        new_selection.add()
        new_selection.first_topic_id = random_int_20()
        new_selection.second_topic_id = random_int_20()
        new_selection.third_topic_id = random_int_20()
        new_selection.status = 1

        random_seconds = random.randint(0, 10)
        random_time = base_time + timedelta(seconds=random_seconds)
        new_selection.submit_time = random_time.strftime('%Y-%m-%d %H:%M:%S')
        new_selection.add()

    # Create some custom topics and selections, starting from 130
    for i in range(130, 150):
        new_topic = Topic(
            name=f'topic{i - 130} (custom)',
            supervisor_id=random_int_10_exclude_1(),
            quota=random_int_5(),
            is_custom=1,
            type_id=random_int_10(),
            description='custom description',
            required_skills='custom required_skills',
            reference='custom reference'
        )
        new_topic.add()

        new_selection = Selection(
            student_id=i,
        )
        new_selection.status = 2
        # Assuming new topics are sequentially added and their IDs match the iteration index
        new_selection.first_topic_id = i - 78
        new_selection.add()


def initTopics():
    create_types()
    create_supervisors()
    create_topics()


def login():
    clear_db()
    creat_one_student()
    create_one_supervisor()
    create_one_manager()


def change_password():
    clear_db()
    creat_one_student()
    create_one_supervisor()
    create_one_manager()


def view_topics():
    clear_db()
    create_one_manager()
    initTopics()


def supervisor_create_topics():
    clear_db()
    create_types()
    create_one_supervisor()


def student_select_topics():
    clear_db()
    initTopics()
    creat_one_student()


def student_selection():
    clear_db()
    create_students()
    create_one_manager()
    initTopics()
    initSelections()


if __name__ == '__main__':
    view_topics()
