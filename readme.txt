Programme LPC
-------------
Auteur Yves Masur (ymasur@microclub.ch)
Version 1.0 du 24.06.2015

This programm doesnt work with english tongue, because the sound are too far of the
written text. In ENglish, the LPC method for deaf people is "Cued Speech". More
infos on https://en.wikipedia.org/wiki/Cued_speech

Le programme écrit en Python, permettant d'entrer du texte (français) à l'écran, 
et d'en extraire les codes LPC (langage parlé complété).
Plus d'info sur le LPC, voir http://alpc.ch/ et 
fr.wikipedia.org/wiki/Langage_parl%C3%A9_compl%C3%A9t%C3%A9

Utilisation
-----------
Programme en CLI: LPC_code.py 
En fenêtre : win_lpc.py
En fenêtre, avec QT: winqt_LPC.py 

Le programme est prévu pour faire fonctionner une main robotique, via le port 
série COM1. Celle-ci applique les clés du LPC pour démonstration.
Si le port ne s'ouvre pas, le programme continue en indiquant les codes à l'écran. 
Les codes sont un couple de valeur:
- positions de P1 à P5 
- configurations, avec C1 à C8

