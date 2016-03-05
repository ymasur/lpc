# -*- coding: utf-8 -*-
# test_main.py
# -----------
from __future__ import unicode_literals
__author__ = 'Yves Masur'

import os
import sys
import signal
import serial
import time

com_port = 'COM1'

def fin_programme(signal, frame):
    """ ferme avec Ctrl-C """
    print("Bye!")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, fin_programme)
    cp = sys.stdin.encoding # encodage de la console
    try:                    # ouvrir le port serie pour Arduino
        s = serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1)
    except IOError as com_error:
        print("Erreur serie %s" % com_port)
        s = 0
        exit(-1)               # pas possible? on sort

    print "\n**** Test des codes ****"
    i = 1
    nombre = raw_input("Nombre de codes consécutifs à poser:".encode(cp))
    nb = int(nombre)
    while i <= nb:
        clef = i % 8 +1
        pos = i % 5 +1
        print("test de code [%d] c%d; position p%d" % (i, clef, pos))
        cmd_main = "c%d p%d\n" % (clef, pos)
        s.write(cmd_main.encode(cp))
        i += 1
        time.sleep(5)

    print u"Terminé!"
    s.write("a\n".encode(cp))