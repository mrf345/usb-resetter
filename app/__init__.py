# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from os import name
from PySide.QtGui import QIcon, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide.QtGui import QLabel, QCheckBox, QLineEdit, QStatusBar, QComboBox
from PySide.QtGui import QCheckBox, QPixmap, QMessageBox, QMenu, QAction
from PySide.QtGui import QSystemTrayIcon, QApplication, QFont
from PySide.QtCore import QThread, Signal, Slot, QSize
from ex_functions import r_path, listd, resetit
from sys import argv, exit, platform
from time import sleep
from functools import partial


class UR_thread(QThread):
    somesignal = Signal(object)

    def speak_me(self):
        self.speak.emit()

    def __init__(self, inp=None, dur=None, thr_counter=0):
        QThread.__init__(self)
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


class UsbResetter(QWidget):
    def __init__(self):
        super(UsbResetter, self).__init__()
        self.P = UR_thread()
        self.thr_counter = 0
        self.Looping = None
        self.Hidden = None
        self.Fhidden = None
        self.s_error = "QStatusBar{color:red;font-weight:1000;}"
        self.s_loop = "QStatusBar{color:black;font-weight:1000;}"
        self.s_norm = "QStatusBar{color:blue;font-style:italic;"
        self.s_norm += "font-weight:500;}"
        favicon = r_path("images/favicon.png")
        logo = r_path("images/logo.png")
        if name == 'nt':
            favicon = r_path("images\\favicon.png")
            logo = r_path("images\\logo.png")
        self.favicon = QIcon(favicon)
        self.plogo = logo
        self.logo = QIcon(logo)
        self.setStyle()
        mlayout = QVBoxLayout()
        self.setAbout(mlayout)
        self.setUlist(mlayout)
        self.setCboxs(mlayout)
        self.setReset(mlayout)
        self.setLoop(mlayout)
        self.setSb(mlayout)
        # functionalities
        self.set_list()
        self.rootWarn()
        # initiation
        self.activateWindow()
        self.setLayout(mlayout)
        self.show()

    def setSb(self, m):
        self.statusbar = QStatusBar()
        m.addWidget(self.statusbar)

    def setStyle(self):
        self.setMaximumWidth(350)
        self.setMinimumWidth(350)
        self.setMaximumHeight(340)
        self.setMinimumHeight(340)
        self.setWindowTitle("usb-resetter 1.0")
        self.setWindowIcon(self.favicon)
        self.show()

    def setAbout(self, m):
        self.pushButton = QPushButton()
        self.icon1 = QIcon()
        self.icon1.addPixmap(QPixmap(self.plogo),
                             QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(self.icon1)
        self.pushButton.setIconSize(QSize(300, 100))
        self.pushButton.clicked.connect(self.show_about)
        m.addWidget(self.pushButton)

    def setUlist(self, m):
        self.comboBox = QComboBox()
        m.addWidget(self.comboBox)

    def setCboxs(self, m):
        ml = QVBoxLayout()
        fl = QHBoxLayout()
        self.checkBox_2 = QCheckBox("Audio")
        self.checkBox_3 = QCheckBox("Mass storage")
        self.checkBox_2.setToolTip("Filter by audio devices")
        self.checkBox_3.setToolTip("Filter by mass storage devices")
        fl.addWidget(self.checkBox_2)
        fl.addWidget(self.checkBox_3)
        ml.addLayout(fl)
        sl = QHBoxLayout()
        self.checkBox_4 = QCheckBox("Network")
        self.checkBox_4.setToolTip("Filter by network devices")
        self.checkBox_5 = QCheckBox("Human interface")
        self.checkBox_5.setToolTip("Filter by Keyboard, mouse, joystick ..etc")
        sl.addWidget(self.checkBox_4)
        sl.addWidget(self.checkBox_5)
        ml.addLayout(sl)
        self.checkBox_2.clicked.connect(self.set_list)
        self.checkBox_3.clicked.connect(self.set_list)
        self.checkBox_4.clicked.connect(self.set_list)
        self.checkBox_5.clicked.connect(self.set_list)
        m.addLayout(ml)

    def setReset(self, m):
        self.pushButton_2 = QPushButton("Reset it")
        font = QFont()
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.setbut_reset)
        m.addWidget(self.pushButton_2)

    def setLoop(self, m):
        ml = QHBoxLayout()
        self.checkBox = QCheckBox("Looping")
        self.checkBox.setToolTip("To repeat resetting for specified duration")
        self.lineEdit = QLineEdit()
        self.lineEdit.setToolTip("Duration in-which the resetting is done")
        self.pushButton_3 = QPushButton("Stop")
        self.pushButton_3.setToolTip("Stop looping")
        ml.addWidget(self.checkBox)
        ml.addWidget(self.lineEdit)
        ml.addWidget(self.pushButton_3)
        self.pushButton_3.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setPlaceholderText("duration in seconds")
        self.checkBox.clicked.connect(self.loop_status)
        self.pushButton_3.clicked.connect(self.in_loop)
        m.addLayout(ml)

    # Functionalities

    def show_about(self):
        Amsg = "<center>All credit reserved to the author of "
        Amsg += "usb-resetter version 1.0"
        Amsg += ", This work is a free, open-source project licensed "
        Amsg += " under Mozilla Public License version 2.0 . <br><br>"
        Amsg += " visit us for more infos and how-tos :<br> "
        Amsg += "<b><a href='https://usb-resetter.github.io/'> "
        Amsg += "https://usb-resetter.github.io/ </a> </b></center>"
        Amsgb = "About usb-resetter"
        v = QMessageBox.about(self, Amsgb, Amsg)
        v = str(v)
        return v

    def closeEvent(self, event=None):
        if self.Hidden is None:
            response = QMessageBox.question(
                self,
                "Hide or close",
                "Do you want to hide the application ?",
                QMessageBox.Yes, QMessageBox.No)
            if response == QMessageBox.Yes:
                if event is not None:
                    event.ignore()
                self.Hidden = True
                self.hide()
            elif response == QMessageBox.No:
                if event is not None:
                    event.accept()
                return self.exitEvent()
            else:
                return False
        else:
            return self.exitEvent()

    def exitEvent(self):
        if self.P.isRunning():
            response = QMessageBox.question(
                self,
                "Making sure",
                "Sure, you want to exit while looping ?",
                QMessageBox.Yes, QMessageBox.No)
            if response == QMessageBox.Yes:
                self.P.stop()
                exit(0)
            else:
                return False
        else:
            exit(0)

    def get_list(self):
        ol = []
        if self.checkBox_2.isChecked():
            ol.append(1)
        if self.checkBox_3.isChecked():
            ol.append(8)
        if self.checkBox_4.isChecked():
            ol.append(2)
        if self.checkBox_5.isChecked():
            ol.append(3)
        if len(ol) >= 1:
            return listd(ol, True)
        else:
            return listd(None, True)

    def set_list(self):
        self.comboBox.clear()
        its = self.get_list()
        if len(its) >= 1:
            self.comboBox.addItems(its)
            self.pushButton_2.setEnabled(True)
            self.checkBox.setEnabled(True)
        else:
            self.pushButton_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.pushButton_3.setEnabled(False)

    def setbut_reset(self):
        t = self.comboBox.currentText()
        if self.Looping is None:
            if resetit(t):
                self.statusbar.setStyleSheet(self.s_norm)
                self.statusbar.showMessage(
                    "# Done: usb device got reset")
                return True
            self.statusbar.setStyleSheet(self.s_error)
            if name != 'nt':
                self.statusbar.showMessage(
                    "# Error: maybe you need sudo permissions")
            else:
                self.statusbar.showMessage(
                    "# Error: maybe you need to add device to libusb")
            return False
        else:
            tl = self.lineEdit.text()
            self.statusbar.setStyleSheet(self.s_error)
            if len(tl) == 0:
                self.statusbar.showMessage(
                    "# Error: you must enter duration for looping")
                return False
            try:
                self.thr_counter += 1
                tl = int(tl)
                if tl < 2:
                    self.statusbar.showMessage(
                        "# Error: the least allowed value is 2")
                    return False
                self.P = UR_thread(t, tl, self.thr_counter)
                self.P.start()
                self.P.somesignal.connect(self.handleStatusMessage)
                self.P.setTerminationEnabled(True)
                self.in_loop(False)
            except:
                self.statusbar.showMessage(
                    "# Error: only valid integers allowed")
                return False

    def loop_status(self):
        if self.Looping:
            self.Looping = None
            self.lineEdit.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        else:
            self.Looping = True
            self.lineEdit.setEnabled(True)
        return True

    def in_loop(self, stop=True):
        if stop:
            if self.P.isRunning():
                self.P.stop()
            self.pushButton_3.setEnabled(False)
            self.pushButton_2.setEnabled(True)
            self.checkBox.setEnabled(True)
            if self.checkBox.isChecked():
                self.lineEdit.setEnabled(True)
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True)
            self.checkBox_5.setEnabled(True)
            self.comboBox.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(True)
            self.pushButton_2.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.checkBox_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)
            self.checkBox_4.setEnabled(False)
            self.checkBox_5.setEnabled(False)
            self.comboBox.setEnabled(False)
        return True

    def rootWarn(self):
        if platform[:len(platform) - 1] == "linux":
            from os import getuid
            if getuid() != 0:
                self.statusbar.setStyleSheet(self.s_error)
                self.statusbar.showMessage(
                    "# Error: you must use sudo on Linux")

    @Slot(object)
    def handleStatusMessage(self, message):
        self.statusbar.setStyleSheet(self.s_loop)
        if message[:7] == '# Error':
            self.in_loop()
            self.statusbar.setStyleSheet(self.s_error)
        self.statusbar.showMessage(message)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip("usb-resetter 1.0 (Left\Right-Click)")
        self.parent = parent
        self.activated.connect(self.toggleP)
        menu = QMenu(parent)
        self.fmenu = QMenu("Fast reset", parent)
        self.fmenu.setToolTip("List of filtered devices to fast reset")
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(parent.show_about)
        quitAction = QAction("Exit", self)
        quitAction.triggered.connect(parent.exitEvent)
        menu.addMenu(self.fmenu)
        menu.addSeparator()
        menu.addAction(aboutAction)
        menu.addAction(quitAction)
        self.setContextMenu(menu)

    def toggleP(self, ar):
        if ar in [QSystemTrayIcon.ActivationReason.Context,
                  QSystemTrayIcon.ActivationReason.Trigger]:
            self.set_Freset()
        else:
            if self.parent.Hidden:
                self.parent.show()
                self.parent.Hidden = None
            else:
                self.parent.hide()
                self.parent.Hidden = True

    def set_Freset(self):
        self.fmenu.clear()
        for l in self.parent.get_list():
            ac = QAction(l, self)

            def actdo(t):
                if resetit(t):
                    self.parent.statusbar.setStyleSheet(self.parent.s_norm)
                    self.parent.statusbar.showMessage(
                        "# Done: usb device got reset")
                    return True
                self.parent.statusbar.setStyleSheet(self.parent.s_error)
            ac.triggered.connect(partial(actdo, l))
            self.fmenu.addAction(ac)


def gui():
    app = QApplication(argv)
    app.setQuitOnLastWindowClosed(False)
    mySW = UsbResetter()
    stray = SystemTrayIcon(mySW.favicon, mySW)
    mySW.show()
    stray.show()
    exit(app.exec_())
