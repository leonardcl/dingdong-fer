# Leonard Christopher - 2022
# Ding Dong - Emotion Recognition

from PyQt5.QtGui import QImage, QPixmap, QWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer, QDate, Qt, QThread, QPoint
from PyQt5.QtWidgets import QDialog, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from pygrabber.dshow_graph import FilterGraph

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import cv2
# import face_recognition
import numpy as np
import datetime
import os
import csv
import mediapipe as mp
import time
import requests
import json
from datetime import datetime
from user import User
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

F_DM = '%d-%m-%Y %H:%M'

class Ui_MainDialog(QDialog):
    def __init__(self):
        super(Ui_MainDialog, self).__init__()
        loadUi('main.ui', self)
        
        # Buttons
        self.minimizeAppBtn.clicked.connect(self.minimized)
        self.closeAppBtn.clicked.connect(self.close)
        
        self.videoThread = VideoThread()
        self.videoThread.indicator(self.indicatorLabel, 
                                   self.indicatorLamp, 
                                   self.faceAbsenceLabel, 
                                   self.emotionStatusLabel)
        self.videoThread.start()
        self.videoThread.change_pixmap_signal.connect(self.update_image)
        
        # Default Status
        self.indicatorLabel.setText("Loading...")
        self.indicatorLamp.setStyleSheet(
            "border-radius: 10px;background-color: rgb(220, 220, 220);")
        self.updateCameraList()
        self.cameraBox.activated[str].connect(self.changeSelectedVideoCapture) 
        self.classBox.activated[str].connect(self.changeSelectedClass)
        self.scheduleBox.activated[str].connect(self.changeSelectedSchedule)
        
        self.checkOutButton.clicked.connect(self.checkOut)
        self.checkInButton.clicked.connect(self.checkIn)
        self.checkInButton.setEnabled(True)
        self.checkOutButton.setEnabled(False)
    
    def checkOut(self):
        self.videoThread.check_in = 0
        self.labelBoxBlenderInstalation.setText(f"Emotion Recognition - Welcome, {self.userData.username}!")
        self.checkInButton.setEnabled(True)
        self.checkOutButton.setEnabled(False)
        
    def checkIn(self):
        if self.classBox.currentText() != "Class" and self.scheduleBox.currentText() != "Schedule":
            if self.selected_schedule_start < datetime.now() and self.selected_schedule_end > datetime.now():
                self.checkInButton.setEnabled(False)
                self.checkOutButton.setEnabled(True)
                self.videoThread.check_in = 1
                self.labelBoxBlenderInstalation.setText(
                    f"Emotion Recognition - Welcome, {self.userData.username}! You're already checked in.")
                self.videoThread.class_id = self.selected_class
                self.videoThread.schedule_id = self.selected_schedule_id
            else:
                self.criticalWindow("You can't check in yet. Please check in later.")
                self.checkInButton.setEnabled(True)
                self.checkOutButton.setEnabled(False)
        else:
            self.checkInButton.setEnabled(True)
            self.checkOutButton.setEnabled(False)
    
    # Set User Data ############################################################
        
    def user_data(self, userData=""):
        self.userData = userData
        self.videoThread.user_data(self.userData)
        self.labelBoxBlenderInstalation.setText(f"Emotion Recognition - Welcome, {self.userData.username}!")
        self.get_class_scedule()
        
    # Get Class & Schedule ####################################################
    
    def get_class_scedule(self):
        _data = {'user_id': self.userData.user_id}
        _data = json.dumps(_data)
        try:
            response = requests.post('http://iot.petra.ac.id:5000/api/user/student/class', data=_data)
            responseData = response.json()
            print(responseData)
            if responseData["success"] == 'success':
                if responseData["data"]:
                    for class_data in responseData["data"]:
                        self.classBox.addItem(f"{class_data['class_id']} - {class_data['class_name']}")
                # self.outputMainWindow_.user_data(userData)
            else:
                self.criticalWindow(responseData['msg'])
        except Exception as e:
            print(e)
            self.criticalWindow("Error. Please try again later.")
        pass
    
    def changeSelectedClass(self, selected_class):
        print(selected_class)
        print(selected_class.split(" - ")[0])
        selected_class_id = selected_class.split(" - ")[0]
        self.selected_class = selected_class_id
        _data = {'class_id': selected_class_id}
        _data = json.dumps(_data)
        self.scheduleBox.clear()
        self.scheduleBox.addItem("Schedule")
        try:
            response = requests.post(
                'http://iot.petra.ac.id:5000/api/user/teacher/class/schedule', 
                data=_data)
            responseData = response.json()
            print(responseData)
            if responseData["success"] == 'success':
                if responseData["data"]:
                    for class_data in responseData["data"]:
                        start_time = datetime.strptime(
                            class_data['start_time'], 
                            '%a, %d %b %Y %H:%M:%S %Z')
                        end_time = datetime.strptime(
                            class_data['end_time'], 
                            '%a, %d %b %Y %H:%M:%S %Z')
                        self.scheduleBox.addItem(f"{class_data['_id']} : {start_time.strftime(F_DM)} - {end_time.strftime(F_DM)}")
                # self.outputMainWindow_.user_data(userData)
            else:
                self.criticalWindow(responseData['msg'])
        except Exception as e:
            print(e)
            self.criticalWindow("Error. Please try again later.")
        
    
    def changeSelectedSchedule(self, selected_schedule):
        print(selected_schedule)
        print(selected_schedule.split(" : ")[0])
        self.selected_schedule_id = selected_schedule.split(" : ")[0]              
        self.selected_schedule_start = datetime.strptime(
            selected_schedule.split(" : ")[1].split(" - ")[0], 
                                                         F_DM)
        self.selected_schedule_end = datetime.strptime(
            selected_schedule.split(" : ")[1].split(" - ")[1], 
                                                       F_DM)
        
        
    # Minimize App ############################################################
        
    def minimized(self):
        self.setWindowState(self.windowState() | QWindow.Minimized)
    
    # Close App ###############################################################
    
    def close(self):
        self.videoThread.terminate()
        cv2.destroyAllWindows()
        self.closeAppDialog()
    
    def closeEvent(self, event):
        self.videoThread.terminate()
        self.videoThread.terminate()
        QCoreApplication.instance().quit()
        
    def ImageUpdateSLot(self, Image):
        self.imgLabel.setPixmap(QPixmap.fromImage(Image))
    
    def closeAppDialog(self):
        msg = QMessageBox()
        msg.setWindowTitle("Ding Dong")
        msg.setText("Are you sure want to quit?")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        
        msg.buttonClicked.connect(self.quitApplication)
        
        x = msg.exec_()
        
    def quitApplication(self, i):
        print(i.text())
        if i.text() == "&Yes":
            # self.videoThread.terminateThis()
            QCoreApplication.instance().quit()
        else:
            self.videoThread.start()
    
    def criticalWindow(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Ding Dong")
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
            
    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()

    # def mouseMoveEvent(self, event):
    #     delta = QPoint (event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()
       
    # Camera App ##############################################################
            
    def updateCameraList(self):
        graph = FilterGraph()

        self.vCaptureList = graph.get_input_devices()                              
        print(self.vCaptureList)
        for vCapture in self.vCaptureList:
            self.cameraBox.addItem(vCapture)
        self.cameraBox.setCurrentIndex(0)
            
    def changeSelectedVideoCapture(self, vCapture):
        vCaptureNum = self.vCaptureList.index(vCapture)
        print(vCaptureNum)
        # self.videoThread.videoThread = False
        # self.videoThread.capture.release()
        # self.videoThread.terminate()
        self.videoThread.changeVideoCapture(vCaptureNum)
        self.videoThread.avg_fps = []
        # self.videoThread.terminate()
        # self.videoThread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.imgLabel.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

###############################################################################

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    facecasc = cv2.CascadeClassifier(
        'haarcascade_files/haarcascade_frontalface_default.xml')
    emotion_dict = {0: "Negatif - Marah", 
                    1: "Negatif - Jijik", 
                    2: "Negatif - Takut", 
                    3: "Positif - Senang", 
                    4: "Netral - Netral", 
                    5: "Negatif - Sedih", 
                    6: "Positif - Terkejut"
                    }
    
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))

    model.load_weights('model.h5')
    video_num = 0
    cap = cv2.VideoCapture(0)
    camera_detected = 0;
    check_in = 0;
    class_id = 0;
    schedule_id = 0;
    last_emo = None;
    last_face = None;
    
    def run(self):
        if self.camera_detected != 1:
            self.indicatorLamp.setStyleSheet(
                "border-radius: 10px;background-color: rgb(255, 85, 0);")
            self.indicatorLabel.setText("Waitttt")
            self.camera_detected = 1
        face_found = False
        prediction = None
        nft = 0
        pft = time.time()-1
        self.avg_fps = []
        while True:
            nft = time.time()
            ret, cv_img = self.cap.read()
            if ret:
                if self.camera_detected != 2:
                    self.indicatorLamp.setStyleSheet(
                        "border-radius: 10px;background-color: rgb(0, 255, 0);")
                    self.indicatorLabel.setText("Camera Detected")
                    self.camera_detected = 2
                    
                # Emotion Recognition #########################################
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                faces = self.facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)

                if len(faces) > 0 and face_found == False:
                    face_found = True
                    self.faceAbsenceLabel.setText("Face Detected")
                elif len(faces) == 0 and face_found == True:
                    face_found = False
                    self.faceAbsenceLabel.setText("Face Absense")

                for (x, y, w, h) in faces:
                        
                    cv2.rectangle(cv_img, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    cropped_img = np.expand_dims(np.expand_dims(
                        cv2.resize(roi_gray, (48, 48)), -1), 0)
                    if face_found == True:
                        prediction = self.model.predict(cropped_img)
                        print(prediction)
                        maxindex = int(np.argmax(prediction))
                        
                        cv2.putText(cv_img, self.emotion_dict[maxindex], 
                                    (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                                    (255, 255, 0), 2, cv2.LINE_AA)
                        
                        if self.emotionStatusLabel.text() != self.emotion_dict[maxindex]:
                            self.emotionStatusLabel.setText(self.emotion_dict[maxindex])
                self.avg_fps.append(1/(nft-pft))
                cv2.putText(cv_img, "FPS: {0:.2f}".format(1/(nft-pft)), 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                            (255, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(cv_img, 
                            "AVG FPS: {0:.2f}".format(sum(self.avg_fps)/len(self.avg_fps)), 
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                            (255, 255, 0), 2, cv2.LINE_AA)
                pft = nft
                self.change_pixmap_signal.emit(cv_img)
                
            else:
                if self.camera_detected != 0:
                    self.indicatorLamp.setStyleSheet(
                        "border-radius: 10px;background-color: rgb(255, 85, 0);")
                    self.indicatorLabel.setText("Camera Not Detected")
                    self.camera_detected = 0
                self.cap.release()
                self.cap = cv2.VideoCapture(self.video_num)
                self.start()
                
            # Send Data #############################################
            if self.check_in == 1:
                if self.last_face != int(face_found) or self.last_emo != int(maxindex):
                    try:
                        emotion_data = {'angry': np.float64(prediction[0][0]), 
                                        'disgust': np.float64(prediction[0][1]), 
                                        'fear': np.float64(prediction[0][2]), 
                                        'happy': np.float64(prediction[0][3]), 
                                        'neutral': np.float64(prediction[0][4]),
                                        'sad': np.float64(prediction[0][5]), 
                                        'surprise': np.float64(prediction[0][6]), 
                                        }
                        send_data = {
                            "user_id": self.userData.user_id,
                            "class_id": self.class_id,
                            "schedule_id": self.schedule_id,
                            "face_detection": int(face_found),
                            "emotion": emotion_data
                        }

                        send_data = json.dumps(send_data)
                        response = requests.post(
                            "http://iot.petra.ac.id:5000/api/user/data/emotion/register", 
                            data=send_data)
                        responseData = response.json()
                    except Exception as e:
                        print(e)
                        
                self.last_face = int(face_found)
                self.last_emo = int(np.argmax(prediction))
            
    def user_data(self, userData):
        self.userData = userData
                
    def indicator(self, indicatorLabel, indicatorLamp, faceAbsenceLabel, emotionStatusLabel):
        self.indicatorLabel = indicatorLabel
        self.indicatorLamp = indicatorLamp
        self.faceAbsenceLabel = faceAbsenceLabel
        self.emotionStatusLabel = emotionStatusLabel
    
    def terminateThis(self):
        pass

    def changeVideoCapture(self, vCaptureNum):
        # self.terminate()
        self.indicatorLamp.setStyleSheet("border-radius: 10px;background-color: rgb(255, 85, 0);")
        self.indicatorLabel.setText("Waitttt")
        self.video_num = vCaptureNum
        self.cap.release()
        self.cap = cv2.VideoCapture(vCaptureNum)
        print('change')
        self.start()
