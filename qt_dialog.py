# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_dialog.ui'
#
# Created: Mon Jun 08 21:46:01 2015
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

class Ui_CodeLPC(object):
    def setupUi(self, CodeLPC):
        CodeLPC.setObjectName(_fromUtf8("CodeLPC"))
        CodeLPC.resize(567, 314)
        CodeLPC.setWindowOpacity(1.0)
        CodeLPC.setSizeGripEnabled(False)
        CodeLPC.setModal(False)
        self.pB_Coder = QtGui.QPushButton(CodeLPC)
        self.pB_Coder.setGeometry(QtCore.QRect(450, 40, 93, 28))
        self.pB_Coder.setObjectName(_fromUtf8("pB_Coder"))
        self.pB_Suivant = QtGui.QPushButton(CodeLPC)
        self.pB_Suivant.setGeometry(QtCore.QRect(450, 140, 93, 28))
        self.pB_Suivant.setObjectName(_fromUtf8("pB_Suivant"))
        self.pB_Aide = QtGui.QPushButton(CodeLPC)
        self.pB_Aide.setGeometry(QtCore.QRect(450, 230, 93, 28))
        self.pB_Aide.setObjectName(_fromUtf8("pB_Aide"))
        self.pB_Quit = QtGui.QPushButton(CodeLPC)
        self.pB_Quit.setGeometry(QtCore.QRect(450, 270, 93, 28))
        self.pB_Quit.setObjectName(_fromUtf8("pB_Quit"))
        self.widget = QtGui.QWidget(CodeLPC)
        self.widget.setGeometry(QtCore.QRect(10, 20, 431, 281))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setStyleSheet(_fromUtf8("font: 9pt \"Arial\";"))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        self.dispInfo = QtGui.QPlainTextEdit(self.widget)
        self.dispInfo.setStyleSheet(_fromUtf8("font: 9pt \"Arial\";"))
        self.dispInfo.setObjectName(_fromUtf8("dispInfo"))
        self.verticalLayout.addWidget(self.dispInfo)

        self.retranslateUi(CodeLPC)
        QtCore.QObject.connect(self.pB_Quit, QtCore.SIGNAL(_fromUtf8("clicked()")), CodeLPC.close)
        QtCore.QMetaObject.connectSlotsByName(CodeLPC)

    def retranslateUi(self, CodeLPC):
        CodeLPC.setWindowTitle(_translate("CodeLPC", "Code LPC - analyseur", None))
        self.pB_Coder.setText(_translate("CodeLPC", "Coder", None))
        self.pB_Suivant.setText(_translate("CodeLPC", "Suivant", None))
        self.pB_Aide.setText(_translate("CodeLPC", "Aide", None))
        self.pB_Quit.setToolTip(_translate("CodeLPC", "<html><head/><body><p>Quitter le programme. Ferme aussi la connexion sérielle avec la main robotique.</p></body></html>", None))
        self.pB_Quit.setText(_translate("CodeLPC", "Quitter", None))
        self.label.setText(_translate("CodeLPC", "Texte à coder en LPC", None))
        self.dispInfo.setPlainText(_translate("CodeLPC", "Init...", None))

