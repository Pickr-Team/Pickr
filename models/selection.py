from .db_instance import db


class Selection(db.Model):
    __tablename__ = 'selections'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student = db.relationship('Student', foreign_keys=[student_id])
    submit_time = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    first_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    second_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    third_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    final_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    first_topic = db.relationship('Topic', foreign_keys=[first_topic_id])
    second_topic = db.relationship('Topic', foreign_keys=[second_topic_id])
    third_topic = db.relationship('Topic', foreign_keys=[third_topic_id])
    final_topic = db.relationship('Topic', foreign_keys=[final_topic_id])

    def __init__(self, student_id):
        self.student_id = student_id
        self.status = 0

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self, student_id, submit_time, status, first_topic_id, second_topic_id, third_topic_id, final_topic_id):
        self.student_id = student_id
        self.submit_time = submit_time
        self.status = status
        self.first_topic_id = first_topic_id
        self.second_topic_id = second_topic_id
        self.third_topic_id = third_topic_id
        self.final_topic_id = final_topic_id
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @property
    def first_topic_name(self):
        return self.first_topic.name

    @property
    def first_topic_supervisor_name(self):
        return self.first_topic.supervisor.first_name + ' ' + self.first_topic.supervisor.last_name

    @property
    def final_topic_supervisor_name(self):
        return self.final_topic.supervisor.first_name + ' ' + self.final_topic.supervisor.last_name

    @property
    def final_topic_supervisor_email(self):
        return self.final_topic.supervisor.email

    @property
    def final_topic_student_english_name(self):
        return self.student.english_name

    @property
    def final_topic_student_chinese_name(self):
        return self.student.chinese_name

    @property
    def english_name(self):
        return self.student.english_name

    @property
    def chinese_name(self):
        return self.student.chinese_name

    @property
    def class_number(self):
        return self.student.class_number

    # if is custom selection, return true
    @property
    def if_custom(self):
        if not self.first_topic:
            return False
        return self.first_topic.is_custom

    @property
    def custom_supervisor_id(self):
        return self.first_topic.supervisor_id

    @property
    def custom_supervisor_name(self):
        return self.first_topic.supervisor.first_name + ' ' + self.first_topic.supervisor.last_name

    @property
    def custom_type_id(self):
        return self.first_topic.type_id

    @property
    def custom_type_name(self):
        return self.first_topic.type.name

    @property
    def final_type_name(self):
        return self.final_topic.type.name

    @property
    def custom_description(self):
        return self.first_topic.description

    @property
    def second_topic_name(self):
        return self.second_topic.name

    @property
    def third_topic_name(self):
        return self.third_topic.name

    @property
    def final_topic_name(self):
        return self.final_topic.name

    @classmethod
    def get_by_student_id(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first()

    @classmethod
    def get_all_custom_selections(cls):
        return cls.query.filter(cls.status.in_([2, 3])).all()

    @classmethod
    def get_by_id(cls, selection_id):
        return cls.query.filter_by(id=selection_id).first()

    # get student name
    @classmethod
    def get_student_name(cls, student_id):
        return cls.query.filter_by(student_id=student_id).first().student.english_name

    # get number of status equal to 0
    @classmethod
    def get_num_of_status_0(cls):
        return cls.query.filter_by(status=0).count()

    # get number of status equal to 1
    @classmethod
    def get_num_of_status_1(cls):
        return cls.query.filter_by(status=1).count()

    # get number of status equal to 2
    @classmethod
    def get_num_of_status_2(cls):
        return cls.query.filter_by(status=2).count()

    # get number of status equal to 3
    @classmethod
    def get_num_of_status_3(cls):
        return cls.query.filter_by(status=3).count()

    # get number of status equal to 4
    @classmethod
    def get_num_of_status_4(cls):
        return cls.query.filter_by(status=4).count()

    # get number of status equal to 3 or 4 (success)
    @classmethod
    def get_num_of_status_3or4(cls):
        return cls.query.filter(cls.status.in_([3, 4])).count()

    # get number of status equal to 5 (fail)
    @classmethod
    def get_num_of_status_5(cls):
        return cls.query.filter_by(status=5).count()

    @classmethod
    def get_all_status_5(cls):
        return cls.query.filter_by(status=5).all()

    def update_status(self, status):
        self.status = status
        db.session.commit()

    def update_submit_time(self, submit_time):
        self.submit_time = submit_time
        db.session.commit()

    def update_first_topic_supervisor_id(self, supervisor_id):
        self.first_topic.supervisor_id = supervisor_id
        db.session.commit()

    def update_first_topic_type_id(self, type_id):
        self.first_topic.type_id = type_id
        db.session.commit()

    def update_first_topic_description(self, description):
        self.first_topic.description = description
        db.session.commit()

    def update_first_topic_name(self, name):
        self.first_topic.name = name
        db.session.commit()

    def update_topic_id(self, topic_priority, topic_id):
        self.__setattr__(self, f'{topic_priority}_topic_id', topic_id)

    # ===================================================================================================
    # DEPRECATE
    def update_first_topic_id(self, topic_id):
        self.first_topic_id = topic_id
        db.session.commit()

    def update_second_topic_id(self, topic_id):
        self.second_topic_id = topic_id
        db.session.commit()

    def update_third_topic_id(self, topic_id):
        self.third_topic_id = topic_id
        db.session.commit()

    def update_final_topic_id(self, topic_id):
        self.final_topic_id = topic_id
        db.session.commit()

    # ===================================================================================================
    @classmethod
    def get_supervisor_selection_not_custom(cls, supervisor_id):
        from .topic import Topic
        selections = cls.query.join(Topic, cls.final_topic_id == Topic.id).filter(
            Topic.supervisor_id == supervisor_id,
            Topic.is_custom == 0,
            cls.final_topic_id.isnot(None)
        ).all()
        return selections

    @classmethod
    def get_supervisor_selection_custom(cls, supervisor_id):
        from .topic import Topic
        selections = cls.query.join(Topic, cls.final_topic_id == Topic.id).filter(
            Topic.supervisor_id == supervisor_id,
            Topic.is_custom == 1,
            cls.final_topic_id.isnot(None)
        ).all()
        return selections

    @classmethod
    def get_all_order_by_submit_time(cls):
        return cls.query.filter_by(status=1).order_by(cls.submit_time).all()

    def topic_is_full(self, topic_priority):
        topic = getattr(self, f'{topic_priority}_topic')
        return topic.get_selected_num_final() >= topic.quota

    def __repr__(self):
        return f'<Selection {self.id}>'
