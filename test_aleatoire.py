# -*- coding: utf-8 -*-
# test_aleatoire.py
# -----------------
from __future__ import unicode_literals
__author__ = 'Yves Masur'

import os
import sys
import signal
import serial
import time
import random

com_port = 'COM1'

def fin_programme(signal, frame):
    """ ferme avec Ctrl-C """
    print("Bye!")
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, fin_programme)
    cp = sys.stdin.encoding # encodage de la console
    try:                    # ouvrir le port serie pour Arduino
        s = serial.Serial(port=com_port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.5)
    except IOError as com_error:
        print("Erreur serie %s" % com_port)
        s = 0
        exit(-1)               # pas possible? on sort

    print "\n**** Test de codes aléatoires ****"
    s.write("e=0\n".encode(cp)) # pas d'echo des commandes, seulement résultats
    time.sleep(1)
    s.flushInput()              # vider le buffer d'entrée
    nombre = raw_input("Nombre de codes consécutifs à poser:".encode(cp))
    nb = int(nombre)
    i = 1
    while i < nb:
        n = random.randint(1, 9999) # nb aléatoire entre 1 et 9999
        clef = n % 8 +1             # modulo 8 pour clef
        pos = n % 5 +1              # modulo 5 pour consonnes
        print("test de code [%d] c%d; position p%d" % (i, clef, pos))
        cmd_main = "c%d p%d\n" % (clef, pos)
        s.write(cmd_main.encode(cp))
        reponse = s.readline()      # voyons la réponse... 4 chrs
        print("Arduino: %s" % reponse)
        time.sleep(5)
        i += 1

    print u"Terminé!"
    s.write("a\n".encode(cp))