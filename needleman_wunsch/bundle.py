import sys
from ruler import Ruler

try:#il faut vérifier que le fichier n'est pas vide
    argument1 = sys.argv[0]
    argument2 = sys.argv[1]
except IndexError:
    print("fichier vide")
    exit()

liste_str=[]
with open(argument2) as txtfile:
    contenu = txtfile.read()
    contenu = contenu.split("\n")
    n = len(contenu)
    i1 , i2 = 0 , 1
    while i2 < n:
        while (i1 == '' and i2 == '' and i2 < n):#on cherche les deux chaînes de caractère non vides les plus proches des indices i1 et i2 actuels
            if contenu[i1] == "" :
                i1 += 1
                i2 += 1
            else:
                if contenu[i2] == '':
                    i2 += 1
        if i2<=n-1: #on vérifie qu on a bien trouvé deux chaînes non vides
            liste_str.append((contenu[i1],contenu[i2]))
            i1 = i2 + 1 #on réitère cette opération au rang suivant i2
            i2 += 2

if liste_str == []:#Si le fichier ne contenait pas deux chaines de caractère non vides au moins:
    print("Il y a moins de deux chaînes non vides dans le fichier")
    exit()




for indice, tuple in enumerate(liste_str):
    ruler = Ruler(tuple[0], tuple[1])
    ruler.compute()
    print(f"___Exemple {indice+1}___distance = {ruler.distance}")
    top, bottom = ruler.report()
    print(top)
    print(bottom)
