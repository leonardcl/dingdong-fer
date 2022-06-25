from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db_models import Users, Emotions, Students, Schedule, db
from db_models import Class as Classes
from flask_cors import CORS, cross_origin
import config
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['APPLICATION_ROOT'] = '/dingdong'
db.init_app(app)

cors = CORS(app, resources={r"*": {"origins": "http://localhost:port"}})

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return "render_template('index.html')"

# @app.shell_context_processor
# def make_shell_context():
#     return {
#             "db": db
#             }


@app.route('/try_api')
def try_pi():
    return json.dumps({'name': 'tyche', 'email': 'leonard@creator.dingdong'})

###############################################################################
# User
###############################################################################
                                                                               

@app.route('/api/user/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])  
def user_login():
    try:
        _user_data = json.loads(request.data)
        _email = _user_data['email']
        _password = _user_data['password']
        existing_user = Users.get_by_email(_email)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not existing_user:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400
    if existing_user.check_password(_password) == False:
        return {'success': 'failed',
                'msg': 'Wrong password.'}, 400

    return {'success': 'success',
            'msg': 'Login Success.',
            'user': existing_user.toJSON()}, 200


@app.route('/api/user/register', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def user_register():
    try:
        _user_data = json.loads(request.data)
        _username = _user_data['username']
        _email = _user_data['email']
        _password = _user_data['password']
        _role = _user_data['role']

        if Users.get_by_email(_email):
            return {'success': 'failed',
                    'msg': 'User existed.'}, 400

        new_user = Users(username=_username, email=_email, role=_role)
        new_user.set_password(_password)
    except:
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    try:
        new_user.save()
    except:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400
    # response = Flask.jsonify({{'success': 'success',
    #                            'msg': 'Login Success.',
    #                            'user': new_user.toJSON()}})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return {'success': 'success',
            'msg': 'Login Success.',
            'user': new_user.toJSON()}, 200


# @app.route('/api/user/check', methods=['POST'])
# @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
# def user_check():
    # print("hello")
    # users = Users.query.all()
    # for user in users:
    #     print(user.email)
    #     print("hello")
    try:
        _user_data = json.loads(request.data)
        _email = _user_data['email']
        _password = _user_data['password']
        existing_user = Users.get_by_email(_email)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not existing_user:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400
    if existing_user.check_password(_password) == False:
        return {'success': 'failed',
                'msg': 'Wrong password.'}, 400

    return {'success': 'success',
            'msg': 'Login Success.',
            'user': existing_user.toJSON()}, 200


@app.route('/api/user/id', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def user_get_detail():
    # print("hello")
    # users = Users.query.all()
    # for user in users:
    #     print(user.email)
    #     print("hello")
    try:
        _user_data = json.loads(request.data)
        _user_id = _user_data['student_id']
        existing_user = Users.get_by_id(_user_id)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not existing_user:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400

    return {'success': 'success',
            'msg': 'Login Success.',
            'data': existing_user.toJSON()}, 200

###############################################################################
# EMOTION
###############################################################################

@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/user/data/emotion/register', methods=['POST'])
def user_emotion_register():
    try:
        _user_data = json.loads(request.data)
        _user_id = _user_data['user_id']
        _class_id = _user_data['class_id']
        _schedule_id = _user_data['schedule_id']
        _face_detection = _user_data['face_detection']
        _angry = _user_data['emotion']['angry']
        _disgust = _user_data['emotion']['disgust']
        _fear = _user_data['emotion']['fear']
        _happy = _user_data['emotion']['happy']
        _neutral = _user_data['emotion']['neutral']
        _sad = _user_data['emotion']['sad']
        _surprise = _user_data['emotion']['surprise']

        _emotion = _user_data['emotion']

        emotion_data = Emotions(user_id=_user_id,
                                class_id=_class_id,
                                schedule_id=_schedule_id,
                                face_detection=_face_detection,                
                                angry=_angry,
                                disgust=_disgust,
                                fear=_fear,
                                happy=_happy,
                                neutral=_neutral,
                                sad=_sad,
                                surprise=_surprise)

    except:
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    try:
        emotion_data.save()
    except:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400

    return {'success': 'success',
            'msg': 'Login Success.',
            'user': emotion_data.toJSON()}, 200


@app.route('/api/user/data/emotion', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def user_emotion():
    try:
        _user_data = json.loads(request.data)
        _user_id = _user_data['user_id']
        _class_id = _user_data['class_id']
        _schedule_id = _user_data['schedule_id']

        emotion_data = Emotions.get_by_user_class_schedule(
            id=_user_id, classId=_class_id, scheduleId=_schedule_id)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

        # return {'success': 'success',
        #         'msg': 'Save Data Success.',
        #         'emotion': _emotion}, 200

    if not emotion_data:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400

    return {'success': 'success',
            'msg': 'Login Success.',
            'data': Emotions.toJSONSimple(emotion_data)}, 200


###############################################################################
# CLASSES
###############################################################################


@app.route('/api/user/teacher/class', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def teacher_class():
    try:
        _user_data = json.loads(request.data)
        _teacher_id = _user_data['teacher_id']
        print(_teacher_id)
        teacher_classes = Classes.get_by_teacher_id(_teacher_id)
        print(teacher_classes)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not teacher_classes:
        return {'success': 'failed',
                'msg': 'No Classes.'}, 400

    return {'success': 'success',
            'msg': 'Success.',
            'data': Classes.toJSONAll(teacher_classes)}, 200


@app.route('/api/user/teacher/class/id', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def class_id():
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        print(_class_id)
        classes_id = Classes.get_by_class_id(_class_id)
        print(classes_id)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not classes_id:
        return {'success': 'failed',
                'msg': 'No Classes.'}, 400

    return {'success': 'success',
            'msg': 'Success.',
            'data': classes_id.toJSON()}, 200


@app.route('/api/user/teacher/class/register', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def teacher_class_register():
    try:
        _user_data = json.loads(request.data)
        _teacher_id = _user_data['teacher_id']
        _class_name = _user_data['class_name']

        detect_double = Classes.get_by_teacher_id_class_name(
            id=_teacher_id, class_name=_class_name)

        new_class = Classes(user_id=_teacher_id, class_name=_class_name)
    except:
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if detect_double:
        return {'success': 'failed',
                'msg': 'Double Class.'}, 400

    try:
        new_class.save()
    except:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400
    # response = Flask.jsonify({{'success': 'success',
    #                            'msg': 'Login Success.',
    #                            'user': new_user.toJSON()}})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return {'success': 'success',
            'msg': 'Login Success.',
            'user': new_class.toJSON()}, 200


@app.route('/api/user/teacher/class/delete', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def teacher_class_delete():
    # print("hello")
    # users = Users.query.all()
    # for user in users:
    #     print(user.email)
    #     print("hello")
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        print(_class_id)
        class_data = Classes.get_by_class_id(_class_id)
        print(class_data)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.'}, 400

    if not class_data:
        return {'success': 'failed',
                'msg': 'Wrong credentials.'}, 400
    try:
        Classes.delete_class_by_class_id(_class_id)
        return {'success': 'success',
                'msg': 'Delete data success.'}, 200
    except Exception as e:
        return {'success': 'failed',
                'msg': 'Delete data failed.'}, 400

###############################################################################
# STUDENTS - CLASS
###############################################################################


@app.route('/api/user/teacher/class/student', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def student_view():
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        print(_class_id)
        students = Students.get_by_class_id(_class_id)
        print(students)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'Data': None}, 400

    if not students:
        return {'success': 'failed',
                'msg': 'No Students.',
                'Data': None}, 400

    students_data = Students.toJSONAll(students)
    new_data = []
    for student_data in students_data:
        temp_dic = {}
        temp_dic['_id'] = student_data['_id']
        temp_dic['class_id'] = student_data['class_id']
        temp_dic['user_id'] = student_data['user_id']
        existing_user = Users.get_by_id(student_data['user_id'])
        existing_user_data = existing_user.toJSON()
        temp_dic['username'] = existing_user_data['username']
        temp_dic['email'] = existing_user_data['email']
        temp_dic['role'] = existing_user_data['role']
        new_data.append(temp_dic)

    print(new_data)

    return {'success': 'success',
            'msg': 'Success.',
            'data': new_data}, 200


@app.route('/api/user/teacher/class/student/register', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def student_register():
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        _user_id = _user_data['student_id']

        existing_user = Users.get_by_id(_user_id)
        if existing_user.role != 'student':
            return {'success': 'failed',
                    'msg': 'Not a student.',
                    'data': None}, 400
        check_student = Students.check_student_by_student_id_class(
            student_id=_user_id, class_id=_class_id)
        new_student = Students(class_id=_class_id, user_id=_user_id)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'data': None}, 400

    if check_student:
        return {'success': 'failed',
                'msg': 'Student already registered.',
                'data': None}, 400

    try:
        new_student.save()
    except:
        return {'success': 'failed',
                'msg': 'Wrong credentials.',
                'data': None}, 400

    return {'success': 'success',
            'msg': 'Student registration success.',
            'data': new_student.toJSON()}, 400


@app.route('/api/user/teacher/class/student/delete', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def student_delete():
    try:
        _user_data = json.loads(request.data)
        _student_id = _user_data['student_id']
        print(_student_id)
        student_data = Students.get_by_student_id(_student_id)
        print(student_data)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'data': None}, 400

    if not student_data:
        return {'success': 'failed',
                'msg': 'Wrong credentials.',
                'data': None}, 400

    try:
        Students.delete_student_by_student_id(_student_id)
        return {'success': 'success',
                'msg': 'Delete data success.',
                'data': None}, 400
    except Exception as e:
        return {'success': 'failed',
                'msg': 'Delete data failed.',
                'data': None}, 400


@app.route('/api/user/student/class', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def student_get_class():
    try:
        _user_data = json.loads(request.data)
        _user_id = _user_data['user_id']
        print(_user_id)
        classes = Students.get_by_user_id(_user_id)
        print(classes)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'Data': None}, 400

    if not classes:
        return {'success': 'failed',
                'msg': 'No Students.',
                'Data': None}, 400

    classes_data = Students.toJSONAll(classes)
    new_data = []
    for class_data in classes_data:
        temp_dic = {}
        existing_class = Classes.get_by_class_id(class_data['class_id'])
        if existing_class:
            temp_dic['_id'] = class_data['_id']
            temp_dic['class_id'] = class_data['class_id']
            temp_dic['user_id'] = class_data['user_id']
            existing_class_data = existing_class.toJSON()
            temp_dic['teacher_id'] = existing_class_data['teacher_id']
            temp_dic['class_name'] = existing_class_data['class_name']
            new_data.append(temp_dic)

    print(new_data)

    return {'success': 'success',
            'msg': 'Success.',
            'data': new_data}, 200


###############################################################################
# SCHEDULE - CLASS
###############################################################################


@app.route('/api/user/teacher/class/schedule', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def schedule_view():
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        print(_class_id)
        students = Schedule.get_by_class_id(_class_id)
        print(students)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'Data': None}, 400

    if not students:
        return {'success': 'failed',
                'msg': 'No Schedule.',
                'Data': None}, 402

    return {'success': 'success',
            'msg': 'Success.',
            'data': Schedule.toJSONAll(students)}, 200


@app.route('/api/user/teacher/class/schedule/register', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def schedule_register():
    try:
        _user_data = json.loads(request.data)
        _class_id = _user_data['class_id']
        _start_time = f"{_user_data['start_date']}:00"
        _end_time = f"{_user_data['end_date']}:00"
        print(_start_time)
        existing_user = Classes.get_by_class_id(_class_id)
        if not existing_user:
            return {'success': 'failed',
                    'msg': 'Not a student.',
                    'data': None}, 400
        print("hello")
        new_schedule = Schedule(
            class_id=_class_id, start_time=datetime.strptime(_start_time, '%Y-%m-%d %H:%M:%S'), end_time=datetime.strptime(_end_time, '%Y-%m-%d %H:%M:%S'))
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'data': None}, 400

    try:
        new_schedule.save()
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong credentials.',
                'data': None}, 400

    return {'success': 'success',
            'msg': 'Student registration success.',
            'data': new_schedule.toJSON()}, 400


@app.route('/api/user/teacher/class/schedule/delete', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def schedule_delete():
    try:
        _user_data = json.loads(request.data)
        _schedule_id = _user_data['schedule_id']
        print(_schedule_id)
        schedule_data = Schedule.get_by_schedule_id(_schedule_id)
        print(schedule_data)
    except Exception as e:
        print(e)
        return {'success': 'failed',
                'msg': 'Wrong input.',
                'data': None}, 400

    if not schedule_data:
        return {'success': 'failed',
                'msg': 'Wrong credentials.',
                'data': None}, 400

    try:
        Schedule.delete_schedule_by_schedule_id(_schedule_id)
        return {'success': 'success',
                'msg': 'Delete data success.',
                'data': None}, 400
    except Exception as e:
        return {'success': 'failed',
                'msg': 'Delete data failed.',
                'data': None}, 400

###############################################################################


if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG, host=config.HOST, port=config.PORT)      