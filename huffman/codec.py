###fonctions auxiliaires
def occurences(texte):
    """fonction qui renvoie une liste dont les éléments sont des instances de la classe Node tq leaf.key est une lettre du texte ou un espace et leaf.value son nombre d'occurences dans le texte, et les fils gauche et droit de l'instance sont deux feuilles vide"""
    d=dict()
    for x in texte:
        try:
            d[x]=d[x] + 1
        except KeyError:#si la clé n'existe pas encore, i.e on n'avait pas encore vu la lettre on la crée, sinon on ajoute 1 à la valeur correspondante
            d[x]=1
    l=[]
    for cle,valeur in d.items():
        n=Node()
        n.key,n.value=cle,valeur#on crée des noeuds de clé et valeur les couples du dictionnaire crée, et de fils droits et gauches Leaf('',0)
        l.append(n)
    return l

def cle(d,value):
    """fonction qui retourne la clé du dictionnaire d dont la valeur dans le dictionnaire est celle passée en argument. On sait ici qu' elle existe et qu'il n'y en a qu'une grâce au codage de Huffman"""
    for cle, valeur in d.items():
        if valeur== value:
            return cle


def Node_minimal(e):
    """fonction qui renvoie l'indice de l'instance de classe leaf ou Node du container pris en paramètre dont l'attribut valeur est minimal, ainsi que cette instance """
    min=e[0].value
    indice=0
    instance=e[0]
    n=len(e)
    for i in range (n):
        if e[i].value<min:
            min=e[i].value
            indice=i
            instance=e[i]
    return indice, instance

###Programme principal

class Leaf:
    """on crée une classe feuille. Une feuille a une étiquette (attribut key) qui est une lettre, et un poids (attribut value) qui est une valeur numérique"""
    def __init__(self, lettre, valeur):
        self.key=lettre
        self.value=valeur

class Node:
    """on crée une classe Noeud de manière récursive: un noued peut être la fusion de deux feuilles, d'une feuille et d'un noeud ou de 2 noeuds. Un noeud a de même les attributs key et value, et les valeurs de ces attributs de la fusion de 2 noeuds correspondent à la somme des valeurs des attributs des noeuds fusionnés. Il a églement un attribut fils_gauche qui correspond au premier Noeud passé en parmètre, et un attribut fils_droit qui correspond au second"""
    def __init__(self, Node1=Leaf('',0), Node2=Leaf('',0)):
        self.value = Node1.value + Node2.value
        self.key = Node1.key + Node2.key
        self.fils_gauche=Node1
        self.fils_droit=Node2

class TreeBuilder:
    '''classe qui à partir d'une chaîne de caractère construit un arbre binaire tel qu'on le définit en informatique, et qui respecte le principe de construction du codage de Huffman'''
    def __init__(self, text):
        self.text = text
    def tree(self):
        text=self.text
        l=occurences(text)
        if len(l)<=1:
            if len(l)==0:
                return "le texte ne contient aucune lettre"
            else:
                return l[0]#l'arbre correspond au noeud d'étiquette l'unique lettre du texte et de valeur son nombre d'occurences
        else:
            while len(l)>1:
                i1, Node1=Node_minimal(l)#on sélectionne le noeud d'étiquette minimale et on le supprime
                del l[i1]
                i2, Node2=Node_minimal(l)#on réitère cette action
                del l[i2]
                a=Node(Node1,Node2)
                l.append(a)#on ajoute à la liste le noeud qui est la fusion des deux noeuds sélectionnés
        return l[0]

def fonction_auxiliaire(arbre,direction,str):
    '''fonction récursive qui remplace la valeur de chaque noeud de l'abre par un nombre en écriture binaire calculé par: la valeur de la racine est 0, et si l'on va à gauche dans l'arbre, on ajoute 1 à droite de l'écriture binaire, 0 sinon'''
    if isinstance(arbre,Node):
        if direction == 'gauche':
            arbre.value=str + '1'
            fonction_auxiliaire(arbre.fils_gauche,'gauche',arbre.value)
            fonction_auxiliaire(arbre.fils_droit,'droit',arbre.value)
        else:
            arbre.value=str + '0'
            fonction_auxiliaire(arbre.fils_gauche,'gauche',arbre.value)
            fonction_auxiliaire(arbre.fils_droit,'droit',arbre.value)

d=dict()#on crée un dictionnaire en tant que variable globale
def fonction_auxiliaire2(self):
    """fonction qui parcourre une instance de la classe Codec jusqu'à arriver à ses feuilles, et remplit un dictionnaire initailement par d[feuilles.key]=feuilles.value"""
    def aux(arbre,pere):#d'après la construction de l'arbre que l'on fait avec tree, seul les noeuds d'étiquette une lettre du texte ont un fils de type Leaf. Il suffit donc de connaître le noeud père de chaque noeud pour déterminer la valeur des noeuds d'étiquette une lettre du texte
        try:
            aux(arbre.fils_gauche,arbre)
            aux(arbre.fils_droit,arbre)
        except AttributeError:#on lève une exception de type AttributeError car lorsqu'on arrive aux feuilles celle-ci n'ont pas de fils gauche ou droit
            d[pere.key]=pere.value
    aux(self,self)

class Codec:
    """classe qui à partir d'une instance tree de classe TreeBuilder construit une instance d'attributs tree=tree, fils_gauche=tree.fils_gauche, fils droit, value=0 et key=tree.key. Cette classe possède également les méthodes encode et decode qui à partir d'une chaine de caractère code celle-ci suivant le codage de Huffman, ou à partir d'un code renvoie le texte correspodnant"""
    def __init__(self,tree):
        fonction_auxiliaire(tree,'gauche', '0')
        fonction_auxiliaire(tree,'droit', '0')
        self.tree=tree
        self.fils_gauche=tree.fils_gauche
        self.fils_droit=tree.fils_droit
        self.value='0'
        self.key=tree.key


    def encode(self,text):
        fonction_auxiliaire2(self)
        str=''
        n=len(text)
        for i in range(n):
            str+= d[text[i]]#on a construit le dictionnaire d tel que ses clés soient les lettres du texte et leurs valeurs leurs nombres binaires associés calculés d'après le codage de Huffman. Il suffit donc de remplacer chaque lettre par ce nombre contenu dans une chaîne de caractère
        return str

    def decode(self, encoded):
        indice1 = 0
        indice2 = 1
        n = len(encoded)
        L = list(d.values())
        chaine = ''
        l = []
        while (indice1 + indice2) <= n:#voir explication ci-dessous
            if chaine in L:
                l.append(chaine)
                indice1= indice1 + indice2
                indice2=1
            else:
                indice2+=1
            chaine=encoded[indice1:(indice1+indice2)]
        text = ''
        for x in l:
            text += cle(d,x)
        return text

#à ce niveau on dispose d'une chaîne de caractère constitué de 0 et de 1, sans espaces, et des couples (clés,valeurs) du dictionnaire d. Et on veut retrouver les lettres du texte. Pour retrouver la première lettre, on part du premier caractère du texte, et tant qu'on ne reconnaît pas une des valeurs du dictionnaire on se décale de un rang vers la droite. Une fois qu'on reconnaît une des valeurs du dictionnaire, on l'ajoute à une liste et on recommence à l'indice suivant de la chaîne de caractère. Ce processus fonctionne car dans le dictionnaire, aucune des valeurs n'est un préfixe d'une autre valeur. Cela impliquerait en effet que dans l'abre construit, l'un des noeuds dont la valeur est l'une de ces valeurs soit un ancêtre du noeud dont la valeur est cette autre valeur, ce qui est exclu car ces noeuds ont pour étiquette une lettre du texte, et pour fils droit et gauche Leaf('',0)

text = "a dead dad ceded a bad babe a beaded abaca bed"

# on analyse les fréquences d'occurrence dans text
# pour fabriquer un arbre binaire
builder = TreeBuilder(text)
binary_tree = builder.tree()


# on passe l'arbre binaire à un encodeur/décodeur
codec = Codec(binary_tree)
# qui permet d'encoder
encoded = codec.encode(text)
# et de décoder
decoded = codec.decode(encoded)
# si cette assertion est fausse il y a un gros problème avec le code
assert text == decoded

# on affiche le résultat
print(f"{text}\n{encoded}")
if decoded != text:
    print("OOPS")










