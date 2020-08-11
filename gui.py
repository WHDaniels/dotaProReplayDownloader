# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 250)
        MainWindow.setMinimumSize(QtCore.QSize(500, 250))
        MainWindow.setMaximumSize(QtCore.QSize(500, 250))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.heroSelectCombo = QtWidgets.QComboBox(self.centralwidget)
        self.heroSelectCombo.setGeometry(QtCore.QRect(310, 100, 121, 22))
        self.heroSelectCombo.setObjectName("heroSelectCombo")
        self.amountSelectCombo = QtWidgets.QComboBox(self.centralwidget)
        self.amountSelectCombo.setGeometry(QtCore.QRect(310, 140, 121, 22))
        self.amountSelectCombo.setObjectName("amountSelectCombo")
        self.heroLabel = QtWidgets.QLabel(self.centralwidget)
        self.heroLabel.setGeometry(QtCore.QRect(50, 100, 131, 16))
        self.heroLabel.setWordWrap(False)
        self.heroLabel.setObjectName("heroLabel")
        self.amountLabel = QtWidgets.QLabel(self.centralwidget)
        self.amountLabel.setGeometry(QtCore.QRect(50, 140, 221, 16))
        self.amountLabel.setWordWrap(False)
        self.amountLabel.setObjectName("amountLabel")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(20, 10, 261, 21))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(310, 190, 121, 23))
        self.downloadButton.setObjectName("downloadButton")
        self.browseLabel = QtWidgets.QLabel(self.centralwidget)
        self.browseLabel.setGeometry(QtCore.QRect(50, 60, 181, 16))
        self.browseLabel.setObjectName("browseLabel")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(310, 60, 121, 23))
        self.browseButton.setObjectName("browseButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 190, 161, 23))
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DotaProReplayDownloader"))
        self.heroLabel.setText(_translate("MainWindow", "Hero you want replays of:"))
        self.amountLabel.setText(_translate("MainWindow", "Amount of most recent matches of that hero:"))
        self.titleLabel.setText(_translate("MainWindow", "Dota Pro Replay Downloader"))
        self.downloadButton.setText(_translate("MainWindow", "Download"))
        self.browseLabel.setText(_translate("MainWindow", "Select your Dota 2 replays directory:"))
        self.browseButton.setText(_translate("MainWindow", "Browse..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
