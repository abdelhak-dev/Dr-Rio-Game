"""def loadMap(self, level):
    try:
        _map = []
        with open("map_" + str(level) + '.txt', 'r') as fichier:
            lines = fichier.readlines()
        for line in lines:
            _map.append([int(n) for n in line.split(",")])
    except:
        print("Erreur de lecture du niveau")
        return False
    return _map"""
_map = []
def loadMap(level):
    with open("map_" + str(level) + '.txt', 'r') as fichier:
     lines = fichier.readlines()
    for line in lines:
        for n in line:
            _map.append(n.split(","))
    #return _map*
    print(_map)
loadMap(1)