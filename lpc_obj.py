# -*- coding: utf-8 -*-
# LPC_obj.py
# ----------
from __future__ import unicode_literals
__module__ = "LPC_obj"
__author__ = 'Yves Masur'

import copy  # usage pour copie d'objets

# noms symboliques, pour afficher les clefs
nom_clefs = \
    {
        1: "d-p-j",
        2: "k-v-z",
        3: "s-r",
        4: "b-n-ui",
        5: "m-t-f",
        6: "l-ch-gn-w",
        7: "g",
        8: "y-ing"
    }

# noms symboliques, pour afficher les positions
nom_positions = \
    {
        1: "pommette",
        2: "coté",
        3: "bouche",
        4: "menton",
        5: "cou"
    }

"""
Liste des remplacements: lrempl[]
Format de la liste: <segment>, <interprétation>, <segment>, <interpretation> ...
les segments de texte et l'interprétation sont séparés par virgule.
Particularités:
    '^' force l'interprétation du son 'é'
    '@' force ''       ''      '   '  'è'
"""
lRempl = \
    [

        # LES et DES avec liaison Z
        "les a", "l^ za", "les e", "l^ ze", "les i", "l^ zi", "les o", "l^ zo", "les u", "l^ zu",
        "des a", "d^ za", "des e", "d^ ze", "des i", "d^ zi", "des o", "d^ zo", "des u", "d^ zu",
        "ces a", "c^ za", "ces e", "c^ ze", "ces i", "l^ zi", "ces o", "c^ zo", "ces u", "c^ zu",

        # Accentuées
        "à", "A", "â", "A", "ä", "@",
        "é", "^", "ê", "@", "ë", "@", "è", "@",
        "ï", "I", "ô", "AU", "ù", "U",

        # Autres fariboles
        "ç", "S",

        # Particularités
        "LES ", " L^ ", " CES ", " C^ ", " DES ", " D^ ", " EST ", " @ ",


        # 'e' se dit 'AI' (belle, pet)
        "EL", "@L", "ET", "@T",
        # début ex -> égz (examen)
        " EX", " ^GZ",

        # Terminaisons S T ET X supprimées
        "S ", " ", "T ", " ", "X ", " ",
        # H aspiré, début en ER -> ér; es - és
        " H", " ", "ER ", "^ ", " ER", " ^R", " ES", " ^S",
        # fin en EZ -> é
        "EZ ", "^ ",
        # M -> N (lamproie, embauche)
        "MP", "NP", "MB", "NB",
        # PH -> f; QU ou Q -> k;
        "PH", "F", "QU", "K", "Q", "K",
        # *EX -> @X (texte, mexicain)
        "EX", "@X",
        # X ->KS
        "X", "KS",
        # signes ignorés
        "?", "", "!", "", "'", "",

        # 'S' entre voyelles
        "ASA", "AZA", "ASE", "AZE", "AS@", "AZ@", "AS^", "AZ^", "ASI", "AZI", "ASO", "AZO", "ASU", "AZU",
        "ESA", "EZA", "ESE", "EZE", "ES@", "EZ@", "ES^", "EZ^", "ESI", "EZI", "ESO", "EZO", "ESU", "EZU",
        "@SA", "@ZA", "@SE", "@ZE", "@S@", "@Z@", "@S^", "@Z^", "@SI", "@ZI", "@SO", "@ZO", "@SU", "@ZU",
        "^SA", "^ZA", "^SE", "^ZE", "^S@", "^Z@", "^S^", "^Z^", "^SI", "^ZI", "^SO", "^ZO", "^SU", "^ZU",
        "ISA", "IZA", "ISE", "IZE", "IS@", "IZ@", "IS^", "IZ^", "ISI", "IZI", "ISO", "IZO", "ISU", "IZU",
        "OSA", "OZA", "OSE", "OZE", "OS@", "OZ@", "OS^", "OZ^", "OSI", "OZI", "OSO", "OZO", "OSU", "OZU",
        "USA", "UZA", "USE", "UZE", "US@", "UZ@", "US^", "UZ^", "USI", "UZI", "USO", "UZO", "USU", "UZU",
        "ZIE", "ZIY", "ZIO", "ZYO",

        # Son mouillé (fille, veille)
        "TIO", "SYO", "ILLE", "IYE", "EIL", "@Y", "AIL", "AY", "IA", "YA", "IER", "YER",
        "IE", "IYE", "I@", "Y@", "I^", "Y^", "IO", "YO", "IU", "YU",

    ]  # lRempl[]


class Transformeur():
    """
    classe des transformeurs - objet statique
    A initialiser au démarrage, avec: Transformeur(lRempl)
    """
    sseg = []  # segment de texte original
    srempl = []  # segment de remplacement
    dpointer = []  # delta avance de pointeur de texte
    idx = 0

    def __init__(self, l_rempl):
        self.init(l_rempl)  # est une méthode de classe

    # noinspection PyMethodParameters
    @classmethod
    def init(cls, l_rempl):
        """
        Reçoit une liste de chaines de caractères par paires
        """
        i = 0
        while i < len(l_rempl):
            cls.add_seg(l_rempl[i], l_rempl[i + 1])
            i += 2
            # print("Remplacements initialisés: %d" % self.idx)

    @classmethod
    def add_seg(cls, seg, rempl):
        """
        ajout d'une paire de textes: un segment à reconnaître et son remplacement
        """
        cls.sseg.insert(cls.idx, seg)
        cls.srempl.insert(cls.idx, rempl)
        # le pointeur est la différence du nombre de caractères  entre le texte original
        # et la séquence de remplacement.
        # Attention:
        # en UTF-8, les caractères accentués comportent 2 bytes; le pointeur doit
        # en tenir compte - ne pas convertir!
        # self.dpointer.insert(self.idx, len(seg.decode("utf-8")) - len(rempl.decode("utf-8")))
        # ce problème est évité en travaillant tout en Unicode
        cls.dpointer.insert(cls.idx, len(seg) - len(rempl))
        cls.idx += 1

    pass


"""
Listes des sons de base et leurs codages.
Format de la liste:
    n° de la position/clef, [liste des segments et avance du pointeur de texte du décodeur]
    Une avance de 0 pour une voyelle signifie que le même chr sera utilisé pour la consonne
"""
lCons3 = \
    [
        6, ["CHR", 2, "OIN", 1],
        7, ["GUE", 2, "GUI", 2, "GUE", 1],
    ]

lCons2 = \
    [
        1, ["GE", 1, "G@", 1, "G^", 1, "GI", 1],
        3, ["CE", 1, "CI", 1, "C^", 1, "C@", 1],
        4, ["UI", 1],
        6, ["OI", 2, "CH", 2, "GN", 2],
    ]

lCons1 = \
    [
        1, ["D", 1, "P", 1, "J", 1],
        2, ["C", 1, "K", 1, "V", 1, "Z", 1],
        3, ["S", 1, "R", 1],
        4, ["B", 1, "N", 1],
        5, ["T", 1, "M", 1, "F", 1],
        6, ["L", 1, "W", 1],
        7, ["G", 1],
        8, ["Y", 1],
    ]

lVoy3 = \
    [
        1, ["OEU", 3, "AIN", 3, "EIN", 3],
        2, ["ANA", 1, "ANE", 1, "AN@", 1, "AN^", 1, "ANI", 1, "ANO", 1, "EAU", 3, "OIN", 0],
        3, ["EON", 3, "INA", 1, "INE", 1, "IN@", 1, "IN^", 1, "INI", 1, "INO", 1, "INU", 1],
        4, ["ONA", 1, "ONE", 1, "ON@", 1, "ON^", 1, "ONI", 1, "ONO", 1, "ONU", 1,
            "ENA", 1, "ENE", 1, "EN@", 1, "EN^", 1, "ENO", 1, "ENU", 1],
        5, ["UNA", 1, "UNE", 1, "UNI", 1, "UNO", 1, "UNU", 1],
    ]

lVoy2 = \
    [
        1, ["IN", 2, "EU", 2],
        2, ["AU", 2, "OI", 0, "UI", 0],
        3, ["AN", 2, "EN", 2, "ON", 2],
        4, ["OU", 2, "AI", 2, "EI", 2],
    ]

lVoy1 = \
    [
        2, ["A", 1, "E", 1, ".", 1, " ", 1],
        3, ["I", 1],
        4, ["O", 1, "@", 1],
        5, ["U", 1, "^", 1],
    ]


class ClefPos():    # todo: implémenter positions
    """
    Définit la position x, y de la clef
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Seg():
    """
    Définit pour un segment de texte, son avance pointeur
    """

    def __init__(self, text="(none)", skip=1):
        self.text = text
        self.l = self.text.__len__()  # pré-calculer la long. du segment
        self.skip = skip

    def get_seg(self):
        return self.text, self.skip

    def get_skip(self):
        return self.skip

    def is_seg(self, t=" "):
        # tester sur la long. du segment
        if self.text == t[:self.l]:
            return True
        else:
            return False

    def show(self):
        print(self.val())

    def val(self):
        v = "text='%s', skip=%d" % (self.text, self.skip)
        return v

# listes globales au module
code_info = []  # stocke les attributs du dernier code trouvé
code_clef = []  # clef...
code_pos = []   # position.
code_clef_defaut = []
code_pos_defaut = []


class Code():
    """"
    Un code comprend:
    - un n° de clef ou de position
    - une longueur (nb de chr utilisés)
    - un nom symbolique (debug)
    - la clef et la position du code,  à placer
    - une liste de 1+ segments de même longueur

    A l'initialisation, le Code reçoit une série de segments, via add_seg()

    """

    global code_info  # stokage local, dernier élément de liste trouvé
    _seg = Seg()  # segment trouvé pour un code

    def __init__(self, key_nb, key_len, key_name):
        self.key_nb = key_nb  # n° de clef
        self.key_len = key_len
        self.key_name = key_name
        self.clef_pos = ClefPos(0, 0)  # position x, y
        self.segm = []  # liste des segments

    def add_seg(self, seg=Seg(" ", 1)):
        self.segm.append(seg)
        # print("Nb de segments: %d" % self.segm.__len__())
        self._seg = seg

    def get_seg(self):
        return self._seg

    def decode(self, text=" "):
        """
        Recherche parmis les segments si le texte passé en paramètre est trouvable
        """
        global code_info
        for s in self.segm:  # pour tous les segments
            if s.is_seg(text):  # Q: texte trouvé?
                self._seg = s  # R: oui, garder trace du segment
                code_info = copy.deepcopy(self)  # et s'annoncer à la référence globale
                return True  # terminé avec succès
        self._seg = Seg()  # R: non, mettre un segment vide (pour avance pointeur)
        return False  # terminé, échec

    def affiche(self, all_l=False):
        print(
            "Code: key_name='%s', key_nb=%d, key_len=%d skip:%d" %
             (self.key_name, self.key_nb, self.key_len, self._seg.skip)
            )
        if all_l:
            for s in self.segm:
                s.affiche()
# fin de classe Code

# liste des objets consonnes et voyelles
clefs_consonnes = []
clefs_voyelles = []  # d'objets Code


def init_clefs(clefs, datas, name="noname"):
    """
    @param clefs: liste contenant les objets clef
    @param datas: liste avec [n° de pos, liste de [segment, avance pointeurs],...]
    @param name: nom symbolique de la liste (pour affichage debug)
    @return: -
    Sortie:
    - liste de positions au format Code complétée
    """
    i = 0
    l = len(datas[i + 1][0])  # la long. du 1er élément est valable pour toute la liste
    while i < datas.__len__():  # tant qu'il y a des clefs/positions
        i2 = i / 2  # nombre de clefs/positions
        c = Code(datas[i], l, name)  # créer un objet Code
        clefs.append(c)  # l'ajouter à la liste
        j = 0
        while j < datas[i + 1].__len__():
            # créer un nouveau segment; avance pointeur
            s = Seg(datas[i + 1][j], datas[i + 1][j + 1])
            # s.affiche()
            clefs[i2].add_seg(s)  # l'ajouter à la clefs
            j += 2  # pointe le prochain segment
        i += 2  # clefs suivante
    pass


def init_positions(pos, datas, name="noname"):
    """
    @param pos: liste contenant les positions
    @param datas: liste avec [n° de pos, liste de [segment, avance pointeurs],...]
    @param name: nom symbolique de la liste (pour affichage debug)
    @return: -
    Sortie:
    - liste de positions au format Code complétée
    """
    init_clefs(pos, datas, name)    # idem ci-dessus!
    pass


def init_keys_all():
    """
    Création des listes d'objets "clefs"
    Entrée: -
    Var globales:
    - 3 listes de clefs ccnsonnes,a resp. 3, 2 et 1 char
    - 3 listes de clefs voyelles, a resp. 3, 2 et 1 char
    Sortie:
    - liste globale des clefs consonnes
    - liste globale des clefs voyelles
    """
    global clefs_consonnes, clefs_voyelles
    global code_pos_defaut, code_clef_defaut

    # listes locales, pour la construction
    k_cons3 = []
    k_cons2 = []
    k_cons1 = []
    k_voy3 = []
    k_voy2 = []
    k_voy1 = []

    # initialisation des clefs selon les listes
    init_clefs(k_cons3, lCons3, "k_cons3")
    init_clefs(k_cons2, lCons2, "k_cons2")
    init_clefs(k_cons1, lCons1, "k_cons1")
    init_positions(k_voy3, lVoy3, "k_voy3")
    init_positions(k_voy2, lVoy2, "k_voy2")
    init_positions(k_voy1, lVoy1, "k_voy1")

    # on somme le tout, dans l'ordre: 3, 2, 1 caractère(s)
    clefs_consonnes = k_cons3 + k_cons2 + k_cons1
    clefs_voyelles = k_voy3 + k_voy2 + k_voy1

    # mettre en place les clefs par défaut, par simple recherche
    # utilisation de copie en profondeur pour stocker l'objet
    s = "F"  # clef 5, m-t-f
    for c in clefs_consonnes:
        if c.decode(s):
            code_clef_defaut = copy.deepcopy(c)

    s = "A"  # pos. coté, ò - e - a
    for c in clefs_voyelles:
        if c.decode(s):
            code_pos_defaut = copy.deepcopy(c)
    pass


def decode_cons(s=" "):
    """
    Décode la consonne dont le texte est passé en paramètre
    variable globale modifiée: code_clef
    @param s: string à décoder
    @return: True si le texte est trouvé, False sinon
    """
    global code_clef

    for c in clefs_consonnes:
        if c.decode(s[:3]):
            code_clef = c
            print "consonne %s" % s
            return True
    code_clef = code_clef_defaut
    return False


def decode_voyl(s=" "):
    """
    Décode la voyelle dont le texte est passé en paramètre
    variable globale modifiée: code_pos
    @param s: texte à décoder
    @return: True si le texte est trouvé, False sinon
    """
    global code_pos

    for c in clefs_voyelles:
        if c.decode(s[:3]):
            code_pos = c
            print "voyelle %s" % s
            return True
    code_pos = code_pos_defaut
    print "defaut pour %s" % s
    return False


def affiche_cons():
    print "affiche consonnes"
    for c in clefs_consonnes:
        c.affiche()


def affiche_voyl():
    print "affiche voyelles"
    for c in clefs_voyelles:
        c.affiche()


class Texte():
    """
    Tient à jour le texte original et la copie de travail, ainsi que
    Les index respectifs
    Utilisation:
        à l'instanciation, passer en paramètre le texte à décoder
        p = Texte("blabla")
        appliquer les remplacements:
        p.remplacements()
        mettre en majuscule:
        p.maj()
        boucler pour chaque décodage:
        while p.cherche > 0:
            p.affiche()

    """
    global code_clef, code_pos
    ti = ""             # input text
    to = ""             # output texte
    ti_idx = []
    to_idx = []
    pointer_mem = 0     # texte début d'analyse
    pointer_mid = 1     # fin du texte utilisé
    pointer = 0         # prochain texte à coder

    def __init__(self, t=u""):
        self.ti = t.strip()         # supression espaces inutiles
        self.ti += " "  # ajout d'un final
        self.ti_idx = [x for x in xrange(len(self.ti) * 2)]  # index 0..n + réserve
        self.to = self.ti   # copie
        self.to_idx = [x for x in xrange(len(self.to) * 2)]  # index 0..n + réserve
        self.pointer = 0

    def remplacements(self, seg_list=Transformeur(lRempl)):
        """
        parcourir la liste de segments pour remplacer les séquences reconnues dans to
        Entrée: seg_list, une liste de type Segment
        Sortie: to, texte modifié
                to_idx, pointeur avec différence de longueur des segments remplacés
        @type self: object Texte
        """
        i = 0  # index de parcours des segments
        while i < seg_list.idx:
            idx = self.to.find(seg_list.sseg[i])    # index d'un segment à remplacer
            if idx > -1:  # tant qu'on trouve un segment, remplacer un à un
                self.to = self.to.replace(seg_list.sseg[i], seg_list.srempl[i], 1)
                print("remplacement: %s par:%s" % (seg_list.sseg[i], seg_list.srempl[i]))
                # ajuster les index après ce point
                i2 = idx + 1
                # pour le reste de l'index, reporter le delta jusqu'à la fin du tableau
                while i2 < len(self.to_idx):
                    self.to_idx[i2] += seg_list.dpointer[i]  # correction delta
                    # si to_idx est plus long, compléter avec la dernière valeur de ti_idx
                    if (self.to_idx[i2]) >= len(self.ti):
                        self.to_idx[i2] = len(self.ti) - 1
                    i2 += 1
            else:
                i += 1  # prochain segment
        pass

    def maj(self):
        self.to = self.to.upper()   # mettre en majuscules
        pass

    def text_pointeur(self):
        """
        Affiche un pointeur sous le texte original, tenant compte du remplacement
        fait pour représenter les sons.

        Exemple, montre le codage de 'à':
        'texte à coder'
        '------^      '
        """
        print self.ti   # texte entré, original
        # version avec insertion du pointeur dans le texte
        # s = self.ti[:self.pointer_mem]+"^"+self.ti[self.pointer_mem:]
        debut = self.to_idx[self.pointer_mem]
        fin = self.to_idx[self.pointer]
        s = "".ljust(debut, ' ') + '^'
        if fin-debut > 1:
            s = s.ljust(fin, '-') + '^'
        print "%s %i-%i" % (s, debut, fin)
        # print "012345678901234567890123456789"

    def text_pointeur_ab(self, m=0):
        """
        Prépare le texte à coder en encadrant la syllabe en cours avec des crochets
        entre l'ancienne position mémorisée et le pointeur actuel
        @param m: Si > 0, n'affiche pas le texte mais le retourne
        @return: texte modifié avec syllabe entre crochets.
        """
        debut = self.to_idx[self.pointer_mem]
        fin = self.to_idx[self.pointer]
        msg = self.ti[:debut] + "[" + self.ti[debut:fin] + "]" + self.ti[fin:]
        if m == 0 :
            print msg
        else:
            return msg

    @staticmethod
    def affiche(m=0):
        """
        affiche le code de clef, son nom; la position, son nom
        """
        msg = "Code clef: %d, %s\nPosition: %d, %s" % \
              (code_clef.key_nb, nom_clefs[code_clef.key_nb],
               code_pos.key_nb, nom_positions[code_pos.key_nb])

        if m == 0:
            print msg
        else:
            return msg

    @staticmethod
    def cmd_arduino():
        """
        Prépare la commande à envoyer à l'interpréteur Arduino
        @return: string de la commande
        """
        s = "C%dP%d\n" % (code_clef.key_nb, code_pos.key_nb)
        return s

    @property
    def cherche(self):
        """
        Cherche la prochaine clef dans le texte, par segment de 3 lettres; puis
        cherche la position, basée sur des voyelles
        Avance l'index du nombre de chr effectivement décodés.
        Variables modifiée:
        pointer_mem: memorise la position de départ d'analyse
        pointer_mid: pointeur entre consonne et voyelle
        pointer : prochaine position à analyser
        @return: nb de char restant à décoder
        """

        global code_clef, code_pos
        notfound = 0

        self.pointer_mem = self.pointer

        s = self.to[self.pointer:self.pointer + 3]  # prend un segment du texte, 3 lettres max
        if decode_cons(s):  # decode ce segment
            self.pointer += code_clef.get_seg().skip  # avance de l'index
            # print "skip c:%d" % code_clef._seg.skip
            self.pointer_mid = self.pointer
        else:               # decodage pas de consonne
            notfound += 1   # compte comme pas trouvé
            code_clef = code_clef_defaut

        s = self.to[self.pointer:self.pointer + 3]  # segment suivant...
        if decode_voyl(s):  # le décoder comme voyelle
            self.pointer += code_pos.get_seg().skip  # avancer l'index
            # print "skip v:%d" % code_pos._seg.skip
        else:
            notfound += 1   # pas de voyelle, compter pas trouvé
            code_pos = code_pos_defaut

        if notfound == 2:  # ni consonne, ni voyelle ? passer le chr
            self.pointer_mid = self.pointer_mem + 1
            self.pointer += 1

        if self.pointer < len(self.to):  # tant que texte to pas traité complètement
            return len(self.to) - self.pointer  # retourner le restant

        return 0  # sinon, retourner 0

# fin de class Texte


def init():
    """
    Initialise les clefs
    """
    init_keys_all()
    print("Init done.\n")
    pass

# test du module
if __name__ == '__main__':

    print(u"\nModule:%s Auteur:%s" % (__module__, __author__))
    init()

    # print(code_pos_defaut.val())

    # for l in voyelles:
    # for f in l.segm: print f.get_seg()
    #
    # for l in consonnes:
    # for f in l.segm: print f.get_seg()
    """
    print "\n1ere consonne CHR"
    decode_cons("CHR")
    print(code_info.val())
    print "\ndernière: Y"
    decode_cons("Y")
    print(code_info.val())

    print "\n1ere voyelle OEU"
    decode_voyl("OEU")
    print(code_info.val())
    print "\nDernière du groupe 4, ENU"
    decode_voyl("ENU")
    print(code_info.val())

    print "\nDernière ^"
    decode_voyl("^")
    print(code_info.val())
    """

    print "Test de texte"
    p = Texte(" texte examen ")
    print "texte entré: %s" % p.ti
    p.remplacements()
    p.maj()
    p.remplacements()
    print "texte transformé: %s" % p.to

    while p.cherche > 0:
        p.text_pointeur()
        p.text_pointeur_ab()
        p.affiche()
        print p.cmd_arduino()
        print(u"*****\n")
        pass

    print "Terminé!"

# end main
