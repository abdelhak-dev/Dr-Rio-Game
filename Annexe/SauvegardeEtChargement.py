# -*- coding:Utf8 -*-

class Joueur(object):
    def __init__(self, name="Player", x=0, y=0, level=0):
        self.x      = x
        self.y      = y
        self.level  = level
        self.name   = name

    def record(self):
        try:
            with open(self.name + '.txt', 'w') as fichier:
                fichier.write(str(self.x) + "\n")
                fichier.write(str(self.y) + "\n")
                fichier.write(str(self.level) + "\n")
        except:
            print("Erreur d'enregistrement du joueur et son niveau")
            return False
         
    def load(self):
        try:
            with open(self.name + '.txt', 'r') as fichier:
                content = fichier.readlines()
            self.x     = int(content[0])
            self.y     = int(content[1])
            self.level = int(content[2])
        except:
            print("Erreur de lecture du joueur et son niveau")
            return False

    def __str__(self):
        return "je suis " + self.name + ", de niveau " + str(self.level) + \
               ", en position (" + str(self.x) + "," + str(self.y) + ")"
    
pascal =Joueur("pascal")
print(pascal)
pascal.record()
richard = Joueur("richard")
print(richard)
richard.load()
print(richard)

