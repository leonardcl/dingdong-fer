from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

                                                                               
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)          
    role = db.Column(db.String(120), unique=False, nullable=False)
    data_joined = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return f"Users {self.username}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_userame(self, new_username):
        self.username = new_username

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDict(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email
        cls_dict['role'] = self.role

        return cls_dict

    def toJSON(self):
        return self.toDict()


class Emotions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    schedule_id = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime(), default=datetime.now)
    face_detection = db.Column(db.Integer, nullable=True)
    angry = db.Column(db.Float, nullable=False)
    disgust = db.Column(db.Float, nullable=False)
    fear = db.Column(db.Float, nullable=False)
    happy = db.Column(db.Float, nullable=False)
    neutral = db.Column(db.Float, nullable=False)
    sad = db.Column(db.Float, nullable=False)
    surprise = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Emotions {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_user_class_schedule(cls, id, classId, scheduleId):
        return cls.query.filter_by(user_id=id, 
                class_id=classId, 
                schedule_id=scheduleId).all()

    @classmethod
    def toJSONSimple(cls, results):
        user_id, class_id, schedule_id = "", "", ""
        for result in results:
            print(result.id)
            print(result.user_id)
            print(result.class_id)
            user_id = result.user_id
            class_id = result.class_id
            schedule_id = result.schedule_id
        dformat = '%Y-%m-%dT%H:%M:%S.%f'
        ts_ms = "milliseconds"
        list_results = []
        time_dummy, duration = None, None
        summary = {"positive": None,"negative": None,"neutral": None}
        for result in results:
            cls_dict = {}
            dummy_emotion_data = {}
            dummy_emotion_data['angry'] = result.angry
            dummy_emotion_data['disgust'] = result.disgust
            dummy_emotion_data['fear'] = result.fear
            dummy_emotion_data['happy'] = result.happy
            dummy_emotion_data['surprise'] = result.surprise
            dummy_emotion_data['neutral'] = result.neutral
            dummy_emotion_data['sad'] = result.sad
            time = datetime.strptime(
                result.date_time.isoformat(timespec='milliseconds'), dformat)
            if time_dummy == None:
                time_dummy = time
            else:
                duration = time - time_dummy
                time_dummy = time
            cls_dict["x"] = time.strftime(dformat)
            if result.face_detection == 0:
                cls_dict["y"] = None
                time_dummy = None
                duration = None
            else:
                cls_dict["y"] = max(dummy_emotion_data, 
                                    key=lambda x: dummy_emotion_data[x]).title()
                emo = cls_dict["y"]
            if duration != None:
                if emo=='Angry' or emo=='Disgust' or emo=='Fear' or emo=='Sad':
                    if summary['negative']:
                        summary['negative'] += duration.total_seconds()
                    else:
                        summary['negative'] = duration.total_seconds()
                elif emo == 'Surprise' or emo == 'Happy' or emo == 'Angry':
                    if summary['positive']:
                        summary['positive'] += duration.total_seconds()
                    else:
                        summary['positive'] = duration.total_seconds()
                else:
                    if summary['neutral']:
                        summary['neutral'] += duration.total_seconds()
                    else:
                        summary['neutral'] = duration.total_seconds()
            list_results.append(cls_dict)
        dic_results = {
            "user_id": user_id,"class_id": class_id,"schedule_id": schedule_id,
            "emotion_data": list_results,
            "summary": summary,
            "total_time": (datetime.strptime(
                results[-1].date_time.isoformat(
                    timespec=ts_ms), dformat) - datetime.strptime(
                results[0].date_time.isoformat(
                    timespec=ts_ms), dformat)).total_seconds(),
            "start_time": datetime.strptime(
                results[0].date_time.isoformat(
                    timespec=ts_ms), dformat).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.strptime(
                results[-1].date_time.isoformat(
                    timespec=ts_ms), dformat).strftime('%Y-%m-%d %H:%M:%S')
        }
        return dic_results

    def toDict(self):
        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['user_id'] = self.user_id
        cls_dict['class_id'] = self.class_id
        cls_dict['schedule_id'] = self.schedule_id
        cls_dict['date_time'] = self.date_time
        cls_dict['face_detection'] = self.face_detection
        emotion_dic = {}
        emotion_dic['angry'] = self.angry
        emotion_dic['disgust'] = self.disgust
        emotion_dic['fear'] = self.fear
        emotion_dic['happy'] = self.happy
        emotion_dic['neutral'] = self.neutral
        emotion_dic['sad'] = self.sad
        emotion_dic['surprise'] = self.surprise
        cls_dict['emotion'] = emotion_dic

        return cls_dict

    def toJSON(self):
        return self.toDict()


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Class {self.id}"

    def save(self):
        print("Savingg...")
        print(self.id, self.user_id, self.class_name)
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_teacher_id(cls, id):
        return cls.query.filter_by(user_id=id).all()

    @classmethod
    def get_by_class_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_class_name(cls, class_name):
        return cls.query.filter_by(class_name=class_name).first()

    @classmethod
    def get_by_teacher_id_class_name(cls, id, class_name):
        return cls.query.filter_by(user_id=id, class_name=class_name).first()

    @classmethod
    def delete_class_by_class_id(cls, id):
        classById = cls.query.filter_by(id=id).first()
        db.session.delete(classById)
        db.session.commit()

    @classmethod
    def toJSONAll(cls, results):
        print(results)
        for result in results:
            print(result.id)
            print(result.user_id)
            print(result.class_name)
        list_results = []
        for result in results:
            cls_dict = {}
            cls_dict['_id'] = result.id
            cls_dict['teacher_id'] = result.user_id
            cls_dict['class_name'] = result.class_name
            list_results.append(cls_dict)

        return list_results

    def toDict(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['teacher_id'] = self.user_id
        cls_dict['class_name'] = self.class_name

        return cls_dict

    def toJSON(self):
        return self.toDict()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Students {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_student_id(cls, id):
        return cls.query.filter_by(id=id).all()

    @classmethod
    def get_by_class_id(cls, class_id):
        return cls.query.filter_by(class_id=class_id).all()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def delete_student_by_student_id(cls, id):
        classById = cls.query.filter_by(id=id).first()
        db.session.delete(classById)
        db.session.commit()

    @classmethod
    def check_student_by_student_id_class(cls, student_id, class_id):
        return cls.query.filter_by(user_id=student_id).filter_by(class_id=class_id).first()

    @classmethod
    def toJSONAll(cls, results):
        print(results)
        for result in results:
            print(result.id)
            print(result.class_id)
            print(result.user_id)
        list_results = []
        for result in results:
            cls_dict = {}
            cls_dict['_id'] = result.id
            cls_dict['class_id'] = result.class_id
            cls_dict['user_id'] = result.user_id
            list_results.append(cls_dict)

        return list_results

    def toDict(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['class_id'] = self.class_id
        cls_dict['user_id'] = self.user_id

        return cls_dict

    def toJSON(self):
        return self.toDict()


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Schedule {self.id}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_class_id(cls, class_id):
        return cls.query.filter_by(class_id=class_id).all()

    @classmethod
    def get_by_schedule_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def delete_schedule_by_schedule_id(cls, id):
        scheduleById = cls.query.filter_by(id=id).first()
        db.session.delete(scheduleById)
        db.session.commit()

    @classmethod
    def toJSONAll(cls, results):
        print(results)
        for result in results:
            print(result.id)
            print(result.class_id)
            print(result.start_time)
            print(result.end_time)
        list_results = []
        for result in results:
            cls_dict = {}
            cls_dict['_id'] = result.id
            cls_dict['class_id'] = result.class_id
            cls_dict['start_time'] = result.start_time
            cls_dict['end_time'] = result.end_time
            list_results.append(cls_dict)

        return list_results

    def toDict(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['class_id'] = self.class_id
        cls_dict['start_time'] = self.start_time
        cls_dict['end_time'] = self.end_time

        return cls_dict

    def toJSON(self):
        return self.toDict()
