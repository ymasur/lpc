# -*- coding: utf-8 -*-
# Init.py
# -------
__author__ = 'Yves'

"""
Module: init.py
Contains the initialization steps at startup

Created on 8.11.2014
@author: Yves Masur (YM)

"""
NAME = "init.py"
VERSION = "Version 1.00 - Yves Masur"
ERR_ARGS = 1
ERR_INFILE = 2
ERR_LABELS = 3
ERR_CONFIG = 4
ERR_OUTFILE = 5
ERR_FORMAT = 6

par = {}

import sys
import os
import logging

def LPC_help():
    """ Aide en ligne sur le programme
    """
    print(u"\nUtilisation:\n"
          u"%s <infile> \n"
          u"\nAvec:\n"
          u"infile : chemin/fichier à analyser\n"
          u"Le fichier log de l'application est \'lpc_show.log\'\n" % NAME
    )
    return

def set_config(cfgFile = "conf.txt"):
    """
    Fonction de setup des variables par le fichier 'conf.txt'.

    """
    try:
        f = open(cfgFile, 'r')  ## Ouverture du fichier de configuration en mode lecture
        lignes = f.readlines()  ## Récupération du contenu du fichier
        # Traitement ligne par ligne
        for l in lignes:
            sp = l.split('#')[0] # Elimination des commentaires potentiels
            sp = sp.split('=') # Séparation variable / valeur
            # on teste la longueur de sp;  si elle n'est pas égale à 2,
            # c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            # difficulté: le tableau par[] contient de l'unicode; le fichier de l'utf-8
            if len(sp) == 2: par[unicode(sp[0].strip(), 'utf-8')] = unicode(sp[1].strip(), 'utf-8')
        f.close() # Fermeture du fichier de configuration

    except IOError:
        so = u"Fichier de configuration %s introuvable!" % cfgFile
        logging.error(so)
        print(so)


def setargs(argv):
    """ lit les arguments en ligne de commande
    """

    if len(argv) > 1:
        # les noms de fichiers vont dans les paramètres
        par["infile"] = argv[1]

    if len(argv) > 1 and ("/?" in argv[1]):
        LPC_help()
        sys.exit(ERR_ARGS)

# test du module
if __name__ == '__main__':
    import sys
    """ main process
    """
    # initialiser le journal de log
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s',
                        datefmt='%d-%m %H:%M',
                        filename='lpc_show.log',
                        filemode='w')
    print("%s %s\n" % (NAME, VERSION))
    set_config()        # la configuration via fichier d'abord
    setargs(sys.argv)   # param. en ligne de commande sur-écrit (prioritaire)
    print("Param: %s" % par)

#end main