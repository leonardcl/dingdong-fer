# Leonard Christopher - 2022
# Ding Dong - Emotion Recognition

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import QCoreApplication, QPoint
from PyQt5.QtGui import QCursor, QWindow
from PyQt5.QtWidgets import QDialog, QMessageBox, QDesktopWidget, QLineEdit
import sys
import mainWindow
import requests
import json
import resources
import webbrowser

from user import User

LOGIN_API = 'http://iot.petra.ac.id:5000/api/user/login'

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("login.ui", self)
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        
        # Buttons
        self.minimizedButton.clicked.connect(self.minimized)
        self.closeButton.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.openwebbrowser)
        
    def login(self):
        print("Clicked Login")
        _email = self.emailInput.text()
        _password = self.passwordInput.text()
        
        if _email != "" or _password != "":
            _data = {'email': _email, 'password': _password}
            _data = json.dumps(_data)
            responseData = ""
            try:
                response = requests.post(LOGIN_API, data=_data)
                responseData = response.json()
                print(responseData)
                if responseData["success"] == 'success':
                    userData = User(username=responseData['user']["username"], 
                                     email=responseData['user']["email"], 
                                     user_id=responseData['user']["_id"],
                                     role=responseData['user']['role'])
                    if responseData['user']['role'] == "student":
                        ui.hide()
                        self.outputMainWindow_(userData)
                    else:
                        self.criticalWindow("Sorry, You are not a student")
                else:
                    self.criticalWindow(responseData['msg'])
            except Exception as e:
                print(e)
                self.criticalWindow("Error. Please try again later.")
        else:
            self.criticalWindow("Please Input Email and Password")

    
    def outputMainWindow_(self, userData=""):
        self._mainWindow = mainWindow.Ui_MainDialog()
        self._mainWindow.user_data(userData)
        self._mainWindow.show()
        
    def minimized(self):
        self.setWindowState(self.windowState() | QWindow.Minimized)
    
    def close(self):
        QCoreApplication.instance().quit()
    
    def criticalWindow(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Ding Dong")
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
        
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()    
        
    def openwebbrowser(self):
        webbrowser.open_new("http://iot.petra.ac.id/dingdong/")
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec())