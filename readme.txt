Programme LPC
-------------
Auteur Yves Masur (ymasur@microclub.ch)
Version 1.0 du 24.06.2015

This programm doesnt work with english tongue, because the sound are too far of the
written text. In ENglish, the LPC method for deaf people is "Cued Speech". More
infos on https://en.wikipedia.org/wiki/Cued_speech

Le programme �crit en Python, permettant d'entrer du texte (fran�ais) � l'�cran, 
et d'en extraire les codes LPC (langage parl� compl�t�).
Plus d'info sur le LPC, voir http://alpc.ch/ et 
fr.wikipedia.org/wiki/Langage_parl%C3%A9_compl%C3%A9t%C3%A9

Utilisation
-----------
Programme en CLI: LPC_code.py 
En fen�tre : win_lpc.py
En fen�tre, avec QT: winqt_LPC.py 

Le programme est pr�vu pour faire fonctionner une main robotique, via le port 
s�rie COM1. Celle-ci applique les cl�s du LPC pour d�monstration.
Si le port ne s'ouvre pas, le programme continue en indiquant les codes � l'�cran. 
Les codes sont un couple de valeur:
- positions de P1 � P5 
- configurations, avec C1 � C8

