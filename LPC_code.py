# -*- coding: utf-8 -*-
# LPC_code.py
# -----------
from __future__ import unicode_literals

__author__ = 'Yves Masur'

import os
import sys
import lpc_obj as lpc
import serial

com_port = 'COM1'

if __name__ == '__main__':
    cp = sys.stdin.encoding  # encodage de la console
    lpc.init()  # initialise la machine à décoder
    try:  # ouvrir le port serie pour Arduino
        s = serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
    except IOError as com_error:
        print("Erreur serie %s" % com_port)
        s = 0
        # exit(-1)               # pas possible? on sort

    while True:
        mon_texte = raw_input("Texte à coder ('exit' pour terminer) :".encode(cp))
        if mon_texte == "exit":
            exit(0);

        else:
            p = lpc.Texte(mon_texte.decode(cp))
            print "texte entré: %s" % (p.ti)
            p.remplacements()
            print "texte transformé: %s" % (p.to)
            p.maj()
            print "texte: majuscule: %s" % (p.to)
            p.remplacements()
            print "\n**** Décodage ****"

            while p.cherche > 0:
                p.text_pointeur_ab()
                # p.text_pointeur()
                p.affiche()
                s_cmd = p.cmd_arduino()
                print "cmd Arduino:%s" % s_cmd
                if s:
                    s.write(s_cmd.encode(cp))
                # print(u"*****\n")
                r = raw_input('suite...'.encode(cp))
                pass

            print "Terminé!\n"

