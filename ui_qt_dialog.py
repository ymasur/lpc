# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yves\Documents\code source\Python\LPC\qt_dialog.ui'
#
# Created: Sun Jun 07 14:59:58 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(567, 315)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 421, 22))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(12, 20, 411, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.pB_Coder = QtGui.QPushButton(Dialog)
        self.pB_Coder.setGeometry(QtCore.QRect(450, 50, 93, 28))
        self.pB_Coder.setObjectName(_fromUtf8("pB_Coder"))
        self.dispInfo = QtGui.QPlainTextEdit(Dialog)
        self.dispInfo.setGeometry(QtCore.QRect(10, 100, 421, 201))
        self.dispInfo.setObjectName(_fromUtf8("dispInfo"))
        self.pB_Suivant = QtGui.QPushButton(Dialog)
        self.pB_Suivant.setGeometry(QtCore.QRect(450, 100, 93, 28))
        self.pB_Suivant.setObjectName(_fromUtf8("pB_Suivant"))
        self.pB_Aide = QtGui.QPushButton(Dialog)
        self.pB_Aide.setGeometry(QtCore.QRect(450, 230, 93, 28))
        self.pB_Aide.setObjectName(_fromUtf8("pB_Aide"))
        self.pB_Quit = QtGui.QPushButton(Dialog)
        self.pB_Quit.setGeometry(QtCore.QRect(450, 270, 93, 28))
        self.pB_Quit.setObjectName(_fromUtf8("pB_Quit"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Texte à coder en LPC", None))
        self.pB_Coder.setText(_translate("Dialog", "Coder", None))
        self.dispInfo.setPlainText(_translate("Dialog", "Init...", None))
        self.pB_Suivant.setText(_translate("Dialog", "Suivant", None))
        self.pB_Aide.setText(_translate("Dialog", "Aide", None))
        self.pB_Quit.setText(_translate("Dialog", "Quitter", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

