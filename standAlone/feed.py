# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalFeed.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMessageBox, QPushButton, QWidget, QInputDialog,
                            QLineEdit, QApplication)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 627)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setMaximumSize(QtCore.QSize(1092, 726))
        Form.setStyleSheet("QWidget{\n"
"    background:    #4a6572;\n"
"}")
        self.AlertBtn = QtWidgets.QPushButton(Form)
        self.AlertBtn.setGeometry(QtCore.QRect(820, 550, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AlertBtn.setFont(font)
        self.AlertBtn.setStyleSheet("#AlertBtn{\n"
"    background:#F9AA33;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
".AlertBtn:hover {\n"
"  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);\n"
"}")
        self.AlertBtn.setObjectName("AlertBtn")
        self.feedLabel = QtWidgets.QLabel(Form)
        self.feedLabel.setGeometry(QtCore.QRect(10, 10, 800, 600))
        self.feedLabel.setStyleSheet("#feedLabel{\n"
"    background:#344955;\n"
"}")
        self.feedLabel.setText("")
        self.feedLabel.setPixmap(QtGui.QPixmap("img/ak11.jpg"))
        self.feedLabel.setScaledContents(True)
        self.feedLabel.setObjectName("feedLabel")
        self.feedLabel.setObjectName("feedLabel")
        self.ActLogs = QtWidgets.QListView(Form)
        self.ActLogs.setGeometry(QtCore.QRect(820, 10, 251, 531))
        self.ActLogs.setStyleSheet("#ActLogs{\n"
"    background:#344955;\n"
"}")
        self.ActLogs.setObjectName("ActLogs")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.AlertBtn.clicked.connect(self.send_alert)


    def send_alert(self):
        alrt = QMessageBox()
        alrt.setWindowTitle("SEND ALERT")
        alrt.setText("Sieg Heil!!")
        #alrt.QInputDialog.getText(self, "Enter your name: ")
        alrt.setIcon(QMessageBox.Warning)

        #dont ask me I dont know either
        x = alrt.exec_()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AlertBtn.setText(_translate("Form", "Send Alert"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
