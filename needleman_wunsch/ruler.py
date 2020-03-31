###Imports
import numpy as np
from colorama import init, Fore, Style

###Fonctions auxiliaires
def red_text(text):
    init(convert=True)#nécessaire avec windows
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def fonction_intermediaire(self,i, j):
    """cette fonction intermédiaire construit à partir d'une instance de la classe Ruler deux chaînes de caractère de même taille égale à max(len(str1[0:i]), len(str2[0:j]) et qui contient les modifications à apporter aux deux chaînes pour qu'elles soient identiques."""

    M = self.matrice#je rappelle ici que la matrice est de taille(len(str1)+1, len(str2)+1)
    str1, str2=self.str1, self.str2
    (n, m) = self.shape
    if i == 1 and j != 1: #si l'une des chaînes ne contient qu'une seule lettre:
        if M[i][j] == j: #si celle-ci n'est pas dans la deuxième, on la change et on lui ajoute le nombre de lettres de la plus grande - 1
            l=['change'] + ['insert' for k in range (j-1)]
            return l , ['None']*(j)#on ne fait aucun changement sur la deuxième
        else:
            k = str2[0:j].index(str1[0])#sinon on repère en quelle position celle-ci se trouve dans la deuxième chaîne
            l=['insert' for l in range(k)] + ['None'] + ['insert']*max(0, (j-k-1))#on insère pour la première chaîne des lettres de part et d'autres de cett position pour la première chaîne
            return l, ['None']*(j)#on ne fait aucun changement pour la deuxième
    elif j == 1 and i != 1:#idem mais rôles échangés
        if M[i][j] == i:
            l=['change'] + ['insert' for k in range (i-1)]
            return ['None']*(i), l
        else:
            k = str1[0:i].index(str2[0])
            l=['insert' for l in range(k)] + ['change'] + ['None']*max(0, (i-k-1))
            return ['None'] *(i), l
    elif i==1 and j==1:
        if str1[0]==str2[0]:
            return ['None'], ['None']
        else:
            return ['None'], ['change']
    else: #si i et j sont différents de 1, il va falloir procéder récursivement, en s'aidant de la façon dont self.matrice a été construite
        if str1[i-1] == str2[j-1]: #si les dernières lettres de str1[0:i] et str2[0:j] sont égales:
            if M[i][j] == M[i-1][j-1]: #on regarde en premier si il est possible de n effectuer aucune modification
                l1, l2 = fonction_intermediaire(self,i-1, j-1)
                l1.append('None')
                l2.append('None')
                return l1, l2
            elif M[i][j] == M[i][j-1] + 1: #sinon, on regarde dans quelle chaîne il faut insérer une lettre
                l1, l2 = fonction_intermediaire(self,i, j-1)
                l1.append('None')
                l2.append('insert')
                return l1, l2
            else:
                l1, l2 = fonction_intermediaire(self,i-1, j)
                l1.append('None')
                l2.append('insert')
                return l1, l2
        else: #si les dernières lettres sont différentes:

            if M[i][j] == M[i-1][j] + 1: #on regarde dans quelle chaîne il faut insérer de lettre
                l1, l2 = fonction_intermediaire(self,i-1, j)
                l1.append('None')
                l2.append('insert')
                return l1, l2
            else :
                l1, l2 = fonction_intermediaire(self,i, j-1)
                l1.append('insert')
                l2.append('None')
                return l1, l2

###Programme principal

class Ruler:
    """les éléments de cette classe sont dotés des attributs distance, shape, matrice str1 et str2. Cette classe est également munie des méthodes compute et report définies dans l'énoncé"""
    def __init__(self, str1, str2):
        self.distance = np.random.random()
        self.str1 = str1
        self.str2 = str2
        self.shape=len(self.str1)+1,len(self.str2)+1
        self.matrice=np.zeros((self.shape))

    def compute(self):
        '''compute modifie les attributs distance et matrice d'un élément de la classe Ruler de telle sorte que self.distance correspod à la distance entre sel.str1 et self.str2 et self.matrice est la matricce M tel que M[i][j] correspond à la distance entre self.str1[0:i] et self.str2[0:j]'''
        str1 = self.str1
        str2 = self.str2
        n, m = self.shape
        M = np.zeros((n, m))
        for i in range (1, n):#la première ligne de la matrice est "réservée" à la chaîne de caractère str1
            M[i][0]=i #si la deuxième chaîne est de longueur nulle, il faut la construire totalement en ajoutant des lettres
            if not(str2[0] in str1):#sinon on regarde si le premier élément de str2 est dans str1 et on agit en conséquence
                M[i][1] = i
            else:
                M[i][1] = i-1
        for i in range (1, m):#on fait de même en inversant les rôles
            M[0][i]=i
            if not(str1[0] in str2):
                M[1][i] = i
            else:
                M[1][i] = i-1
        for i in range(1, n):#pour i et j plus grand que 1, on applique les règles la programmation dynamique avec un poids de 1 pour chaque changement
            for j in range (1, m):
                M[i][j] = min(M[i-1][j-1], M[i][j-1] + 1, M[i-1][j] + 1)
        self.distance = M[n-1][m-1] #on modifie les valeurs de self.distance et self.matrice
        self.matrice=M

    def report (self):
        M = self.matrice
        str1,str2=self.str1,self.str2
        (n, m) = self.shape
        L1, L2 = fonction_intermediaire(self,n-1, m-1) #on construit 2 nouvelles chaînes de caractère avec fonction_intermédiaire.
        str1_changed=f""
        str2_changed=f""
        compteur1=0
        compteur2=0
        for i in range (0, len(L1)):#on parcourre L1 et:
            if L1[i] == 'insert':# s'il faut insérer une lettre, on affiche un "=" en rouge
                str1_changed += red_text('=')
                compteur1+=1
            if L1[i] == 'change': # s'il faut changer une lettre, on affiche cette lettre en rouge
                a=str1[i-compteur1]
                str1_changed += red_text(a)
            if L1[i] == 'None':# s'il ne faut rien faire, on affiche simplement la lettre
                str1_changed += str1[i-compteur1]
        for i in range (0, len(L2)):#de même pour L2
            if L2[i] == 'insert':
                compteur2+=1
                str2_changed += red_text('=')
            if L2[i] == 'change':
                a=str2[i-compteur2]
                str2_changed += red_text(a)
            if L2[i] == 'None':
                str2_changed += str2[i-compteur2]
        return str1_changed, str2_changed #on renvoie les 2 chaînes de caractères modifiées et de même longueur

ruler = Ruler("abcdefghi", "abcdfghi")

# on impose à l'utilisateur de la classe
# de lancer explicitement le calcul
ruler.compute()

# on obtient la distance
print(ruler.distance)

# et pour afficher les différences
top, bottom = ruler.report()
print(top)
print(bottom)

