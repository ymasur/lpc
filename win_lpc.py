# -*- coding: utf-8 -*-
# win_lpc.py
# -----------
# 6.4.2015
__author__ = 'Yves Masur'

import sys
import lpc_obj as lpc
import serial
import tkMessageBox
import Tkinter as tk
# from Tkinter import *
# from ttk import Frame, Button, Label, Style

cp = sys.stdin.encoding  # encodage de la console
com_port = 'COM1'
s = 0  # interface seriel


class HMI_LPC(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()
        lpc.init()
        self.mon_texte = ""
        self.p = lpc.Texte(self.mon_texte)

    def initUI(self):
        """
    I   nitilisation du graphique
        """
        # barre de menu
        self.menubar = tk.Menu(self.parent)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Connecte Main_LPC", command=self.connect)
        self.filemenu.add_command(label="Clore seriel", command=self.disconnect)
        self.filemenu.add_command(label="Save as...", command=self.donothing)

        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.parent.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.parent.config(menu=self.menubar)
        self.parent.title("Main LPC")

        # place les éléments dans une grille
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        # texte statique
        self.lbl = tk.Label(self, text="Texte à coder")
        self.lbl.grid(sticky=tk.W, pady=4, padx=5)
        # ligne d'édition, largeur 2 colonnes
        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2,
                        sticky=tk.E + tk.W, padx=5)

        self.disp_info()
        # self.area.pack(side=tk.LEFT, fill=tk.Y)

        # place des boutons et associe les commandes
        self.btW = 10  # 10 chr pour les boutons (assure même largeur)

        self.abtn = tk.Button(self, text="Coder", width=self.btW, command=self.traiteText)
        self.abtn.grid(row=1, column=3)

        self.sbtn = tk.Button(self, text="Suivant", width=self.btW, command=self.suivant)
        self.sbtn.grid(row=3, column=3)

        self.hbtn = tk.Button(self, text="Aide", width=self.btW, command=self.help)
        self.hbtn.grid(row=4, column=3)

        self.qbtn = tk.Button(self, text="Quitter", width=self.btW, command=self.quit)
        self.qbtn.grid(row=5, column=3)

    def disp_info(self, dispval="Démarrage complet de tous les modules de cette machine\n"
                                "permettant de coder du LPC en interactif.\n"
        ):
        self.dispVal = dispval
        self.area = tk.Label(self, justify=tk.LEFT, text=self.dispVal)
        self.area['bg'] = 'black';
        self.area['fg'] = 'grey'
        self.area.grid(row=2, column=0, rowspan=2, columnspan=3,
                       padx=5, sticky=tk.E + tk.W + tk.S + tk.N)
        self.pack(fill=tk.Y, expand=1)
        print(self.dispVal)

    @staticmethod
    def help():
        msg = " Aide sur la main codeuse LPC.\n" \
            "Entrez votre texte à coder, puis cliquez le bouton [Coder].\n" \
            "Chaque code trouvé par analyse du texte est envoyé au contrôleur Arduino, qui déplacera la main.\n" \
            "Après chaque code, pressez sur [Suivant]"    \
            "La liaison USB (COM1) doit être établie via le menu 'File'"

        tkMessageBox.showinfo("Aide sur la main codeuse LPC", msg)


    def traiteText(self):
        self.mon_texte = self.entry.get()
        if len(self.mon_texte) < 2:
            return
        self.p = lpc.Texte(self.mon_texte)
        self.p.remplacements()
        msg = u"texte transformé:\n%s" % (self.p.to)
        self.p.maj()
        msg += u"\nen majuscules:\n%s" % (self.p.to)
        self.p.remplacements()
        self.disp_info(msg)


    def suivant(self):
        global s  # seriel
        
        if len(self.mon_texte) < 2:
            return
        if self.p.cherche > 0:
            msg = self.p.text_pointeur_ab(1) + "\n"
            msg += self.p.affiche(1) + "\n"
            s_cmd = self.p.cmd_arduino()
            msg = msg + "cmd Arduino:" + s_cmd
        else:
            msg = "Terminé!"
            self.entry.delete(0, len(self.mon_texte))
            s_cmd = "a\n"

        assert isinstance(s, object)
        if s:
            s.write(s_cmd.encode(cp))
        self.disp_info(msg)
        pass

    @staticmethod
    def messageBox(msg):
        tkMessageBox.showinfo("Message d'erreur", msg)

    def connect(self):
        global s  # seriel
        try:  # ouvrir le port serie pour Arduino
            s = serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
            me = "Connexion serie %s OK" % com_port
        except IOError as com_error:
            me = "Erreur serie %s" % com_port
            s = 0

        print(me)
        self.messageBox(me)
        self.disp_info(me)

    def disconnect(self):
        global s
        try:
            if s != 0:
                s.close()
                me = "Dé-connexion serie %s OK" % com_port
                s = 0
            else:
                me = "Pas de connection à détacher."

        except IOError as com_error:
            me = "Erreur serie %s" % com_port

        print(me)
        self.messageBox(me)
        self.disp_info(me)

    def donothing(self):
        filewin = tk.Toplevel(self.parent)
        button = tk.Button(filewin, text="inactif")
        button.pack()


def main():
    root = tk.Tk()
    root.geometry("600x300")  # H x V
    app = HMI_LPC(root)
    app.pack(fill=tk.Y, expand=1)
    root.mainloop()


if __name__ == '__main__':
    main()


