# -*- coding: utf-8 -*-
from os import name
from PySide import QtCore, QtGui
from ex_functions import r_path, listd, resetit
from sys import argv, exit
from time import sleep
from functools import partial


class UR_thread(QtCore.QThread):
    somesignal = QtCore.Signal(object)

    def speak_me(self):
        self.speak.emit()

    def __init__(self, inp=None, dur=None, thr_counter=0):
        QtCore.QThread.__init__(self)
        self.inp = inp
        self.dur = dur
        self.outp = None
        self.abo = None
        self.thr_counter = thr_counter

    def run(self):
        counter = 0
        dur = 0
        err = False
        while self.abo is None:
            if dur == 1 or dur == self.dur:
                if dur == self.dur:
                    dur = 2
                if resetit(self.inp):
                    counter += 1
                    self.somesignal.emit(
                        '%% Device got reset for ' + str(
                            counter) + ' times .. looping %%')
                else:
                    if name != 'nt':
                        self.somesignal.emit(
                            "# Error: maybe you need sudo permissions")
                    else:
                        self.somesignal.emit(
                            "# Error: maybe you need to add device to libusb")
                    err = True
                    break
            sleep(1)
            dur += 1
        if not err:
            self.somesignal.emit(
                '# loop number ' + str(self.thr_counter) + ' got terminated')

    def stop(self):
        self.dur = 0
        self.abo = True
        return True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.s_error = "QStatusBar{color:red;font-weight:1000;}"
        self.s_loop = "QStatusBar{color:black;font-weight:1000;}"
        self.s_norm = "QStatusBar{color:blue;font-style:italic;"
        self.s_norm += "font-weight:500;}"
        self.favicon = r_path("images/favicon.png")
        self.logo = r_path("images/logo.png")
        if name == 'nt':
            self.favicon = r_path("images\\favicon.png")
            self.logo = r_path("images\\logo.png")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(327, 340)
        MainWindow.setMinimumSize(QtCore.QSize(327, 340))
        MainWindow.setMaximumSize(QtCore.QSize(327, 340))
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(self.favicon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(self.icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 327, 340))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.logo),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(300, 100))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_2 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 0, 1, 1, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 0, 0, 1, 1)
        self.checkBox_4 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 1, 0, 1, 1)
        self.checkBox_5 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout.addWidget(self.checkBox_5, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.comboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.pushButton_2 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.lineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_3 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setText("Stop")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate(
                "MainWindow",
                "usb-resetter 0.1", None,
                QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "About usb-resetter",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "List usb audio devices",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Audio",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "List mass storage usb devices",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Mass storage",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_4.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "List network usb cards ",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_4.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Network card",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_5.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "List keyboard, mouse, control usb devices",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox_5.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Human interface",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "Select usb device by its descriptor, idvendor and idproduct",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "unplug and plug device",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Reset it",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "too repeat resetting selected device",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(
            QtGui.QApplication.translate(
                "MainWindow",
                "Loop",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "time on-which resetting is done",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setPlaceholderText(
            QtGui.QApplication.translate(
                "MainWindow",
                "duration in seconds",
                None,
                QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow",
                "stop looping",
                None,
                QtGui.QApplication.UnicodeUTF8))


class ControlMainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon = self.ui.icon
        self.P = UR_thread()
        self.thr_counter = 0
        self.Looping = None
        self.set_list()
        self.ui.pushButton.clicked.connect(self.show_about)
        self.ui.checkBox_2.clicked.connect(self.set_list)
        self.ui.checkBox_3.clicked.connect(self.set_list)
        self.ui.checkBox_4.clicked.connect(self.set_list)
        self.ui.checkBox_5.clicked.connect(self.set_list)
        self.ui.pushButton_2.clicked.connect(self.setbut_reset)
        self.ui.checkBox.clicked.connect(self.loop_status)
        self.ui.pushButton_3.clicked.connect(self.in_loop)

    def show_about(self):
        Amsg = "<center>All credit reserved to the author of "
        Amsg += "usb-resetter version 0.1"
        Amsg += ", This work is a free, open-source project licensed "
        Amsg += " under Mozilla Public License version 2.0 . <br><br>"
        Amsg += " visit us for more infos and how-tos :<br> "
        Amsg += "<b><a href='https://usb-resetter.github.io/'> "
        Amsg += "https://usb-resetter.github.io/ </a> </b></center>"
        Amsgb = "About usb-resetter"
        return QtGui.QMessageBox.about(
            self,
            Amsgb,
            Amsg)

    def closeEvent(self, event=None):
        if self.P.isRunning():
            response = QtGui.QMessageBox.question(
                self,
                "Making sure",
                "Sure, you want to exit while looping ?",
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if response == QtGui.QMessageBox.Yes:
                self.P.stop()
                if event is not None:
                    event.accept()
                exit(0)
            else:
                if event is not None:
                    event.ignore()
        else:
            if event is not None:
                event.accept()
            exit(0)

    def get_list(self):
        ol = []
        if self.ui.checkBox_2.isChecked():
            ol.append(1)
        if self.ui.checkBox_3.isChecked():
            ol.append(8)
        if self.ui.checkBox_4.isChecked():
            ol.append(2)
        if self.ui.checkBox_5.isChecked():
            ol.append(3)
        if len(ol) >= 1:
            return listd(ol, True)
        else:
            return listd(None, True)

    def set_list(self):
        self.ui.comboBox.clear()
        its = self.get_list()
        if len(its) >= 1:
            self.ui.comboBox.addItems(its)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.checkBox.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(False)
            self.ui.checkBox.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)

    def setbut_reset(self):
        t = self.ui.comboBox.currentText()
        if self.Looping is None:
            if resetit(t):
                self.ui.statusbar.setStyleSheet(self.ui.s_norm)
                self.ui.statusbar.showMessage(
                    "# Done: usb device got reset")
                return True
            self.ui.statusbar.setStyleSheet(self.ui.s_error)
            if name != 'nt':
                self.ui.statusbar.showMessage(
                    "# Error: maybe you need sudo permissions")
            else:
                self.ui.statusbar.showMessage(
                    "# Error: maybe you need to add device to libusb")
            return False
        else:
            tl = self.ui.lineEdit.text()
            self.ui.statusbar.setStyleSheet(self.ui.s_error)
            if len(tl) == 0:
                self.ui.statusbar.showMessage(
                    "# Error: you must enter duration for looping")
                return False
            try:
                self.thr_counter += 1
                tl = int(tl)
                self.P = UR_thread(t, tl, self.thr_counter)
                self.P.start()
                self.P.somesignal.connect(self.handleStatusMessage)
                self.P.setTerminationEnabled(True)
                self.in_loop(False)
            except:
                self.ui.statusbar.showMessage(
                    "# Error: only valid integers allowed")
                return False

    def loop_status(self):
        if self.Looping:
            self.Looping = None
            self.ui.lineEdit.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
        else:
            self.Looping = True
            self.ui.lineEdit.setEnabled(True)
        return True

    def in_loop(self, stop=True, tray=False):
        if stop:
            if self.P.isRunning():
                self.P.stop()
            else:
                if tray:
                    self.ui.statusbar.setStyleSheet(self.ui.s_error)
                    self.ui.statusbar.showMessage(
                        "# Error: no running loop alive to kill !")
                    return True
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.checkBox.setEnabled(True)
            if self.ui.checkBox.isChecked():
                self.ui.lineEdit.setEnabled(True)
            self.ui.checkBox_2.setEnabled(True)
            self.ui.checkBox_3.setEnabled(True)
            self.ui.checkBox_4.setEnabled(True)
            self.ui.checkBox_5.setEnabled(True)
            self.ui.comboBox.setEnabled(True)
        else:
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.checkBox.setEnabled(False)
            self.ui.lineEdit.setEnabled(False)
            self.ui.checkBox_2.setEnabled(False)
            self.ui.checkBox_3.setEnabled(False)
            self.ui.checkBox_4.setEnabled(False)
            self.ui.checkBox_5.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
        return True

    @QtCore.Slot(object)
    def handleStatusMessage(self, message):
        self.ui.statusbar.setStyleSheet(self.ui.s_loop)
        if message[:7] == '# Error':
            self.in_loop()
            self.ui.statusbar.setStyleSheet(self.ui.s_error)
        self.ui.statusbar.showMessage(message)


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        aboutAction = QtGui.QAction("About", self)
        aboutAction.triggered.connect(parent.show_about)
        self.stopAction = QtGui.QAction("Stop loop", self)
        self.stopAction.triggered.connect(partial(parent.in_loop, tray=True))
        quitAction = QtGui.QAction("Exit", self)
        quitAction.triggered.connect(parent.closeEvent)
        menu.addAction(self.stopAction)
        menu.addAction(aboutAction)
        menu.addAction(quitAction)
        self.setContextMenu(menu)


def gui():
    app = QtGui.QApplication(argv)
    mySW = ControlMainWindow()
    stray = SystemTrayIcon(mySW.icon, mySW)
    mySW.show()
    stray.show()
    exit(app.exec_())
