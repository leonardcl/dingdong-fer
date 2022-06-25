import json
import requests

# # send_data = json.dumps("{'user_id': 1, 'class_id': 1, 'face_detection': 1, 'emotion': {'angry': 0.0, 'disgust': 0.0, 'fear': 4.1596297e-31, 'happy': 0.0, 'netral': 1.0, 'sad': 0.0, 'surprise': 0.0}}")
# send_data = json.dumps("{'user_id': 1, 'class_id': 1, 'face_detection': 1, 'emotion': {'angry': 0.0, 'disgust': 0.0, 'fear': 4.1596297e-31, 'happy': 0.0, 'netral': 1.0, 'sad': 0.0, 'surprise': 0.0}}")
# print(send_data)
# # print(json.loads(send_data))
# response = requests.post("http://192.168.100.55:5000/api/user/data/emotion", data=send_data)
# responseData = response.json()
# print(responseData)


# _data = {'email': "admin@example.com", 'password': "admin"}
# _data = json.dumps(_data)
# responseData = ""

# response = requests.post('http://192.168.100.55:5000/api/user/login', data=_data)
# responseData = response.json()
# print(responseData)

data = {'user_id': 1, 'class_id': 1, 'face_detection': 1, 'emotion': {'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'netral': 1.0, 'sad': 0.0, 'surprise': 0.0}}
data = json.dumps(data)
print(data)