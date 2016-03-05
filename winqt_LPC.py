# -*- coding: utf-8 -*-
# winqt_LPC.py
# -----------
# __author__ = 'Yves Masur'

import sys
import lpc_obj as lpc
import serial
from PyQt4 import QtCore
from PyQt4.QtGui import *
import ui_qt_dialog


cp = sys.stdin.encoding  # encodage de la console
com_port = 'COM1'
s = 0  # instance d'interface seriel

@QtCore.pyqtSlot() # signal with no arguments
class HMI_LPC(QDialog, ui_qt_dialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(HMI_LPC, self).__init__(parent)
        self.setupUi(self)
        lpc.init()
        self.mon_texte = u"Texte bidon"
        self.p = lpc.Texte(self.mon_texte)
        self.connect()

    @QtCore.pyqtSlot() # signal with no arguments
    def disp_info(self, dispval=u"Démarrage complet de tous les modules de cette machine\n"
                                u"permettant de coder du LPC en interactif.\n"
        ):
        self.dispVal = dispval
        print(self.dispVal)
        self.dispInfo.setPlainText(self.dispVal)

    @QtCore.pyqtSlot() # signal with no arguments
    def on_pB_Coder_clicked(self):
        self.mon_texte = unicode(self.lineEdit.text())
        if len(self.mon_texte) < 2:
            return
        self.p = lpc.Texte(self.mon_texte )
        self.p.remplacements()
        msg = u"texte transformé:\n%s" % (self.p.to)
        self.p.maj()
        msg += u"\nen majuscules:\n%s" % (self.p.to)
        self.p.remplacements()
        self.disp_info(msg)
        pass

    @QtCore.pyqtSlot() # signal with no arguments
    def on_pB_Suivant_clicked(self):
        global s  # seriel

        if len(self.mon_texte) < 2:
            return
        if self.p.cherche > 0:
            msg = self.p.text_pointeur_ab(1) + "\n"
            msg += self.p.affiche(1) + "\n"
            s_cmd = self.p.cmd_arduino()
            msg = msg + u"cmd Arduino:" + s_cmd
        else:
            msg = u"Terminé!"
            self.lineEdit.clear()
            s_cmd = "a\n"

        assert isinstance(s, object)
        if s:
            s.write(s_cmd.encode(cp))
        self.disp_info(msg)
        pass

    @QtCore.pyqtSlot() # signal with no arguments
    def messageBox(self, msg):
        QMessageBox.warning(self, u"Message d'information", msg)

    def connect(self):
        global s  # seriel
        try:  # ouvrir le port serie pour Arduino
            s = serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
            me = u"Connexion serie %s OK" % com_port
        except IOError as com_error:
            me = u"Erreur serie %s" % com_port
            s = 0

        print(me)
        self.messageBox(me)
        self.disp_info(me)

    def disconnect(self):
        global s
        try:
            if s != 0:
                s.close()
                me = u"Dé-connexion serie %s OK" % com_port
                s = 0
            else:
                me = u"Pas de connection à détacher."

        except IOError as com_error:
            me = u"Erreur serie %s" % com_port

        print(me)
        self.messageBox(me)
        self.disp_info(me)

    @QtCore.pyqtSlot() # signal with no arguments
    def on_pB_Aide_clicked(self):
        print("aide")
        msg = u"Aide sur la main codeuse LPC.\n" \
            u"Entrez votre texte à coder, puis cliquez le bouton [Coder].\n" \
            u"Chaque code trouvé par analyse du texte est envoyé au contrôleur Arduino, qui déplacera la main.\n" \
            u"Après chaque code, pressez sur [Suivant]\n\n"    \
            u"La liaison USB (COM1) doit être établie via le menu 'File'"
        QMessageBox.warning(self,"Main LPC", msg)

    @QtCore.pyqtSlot() # signal with no arguments
    def on_pB_Quit_clicked(self):
        print(u"termine")
        exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = HMI_LPC()
    form.show()
    sys.exit(app.exec_())