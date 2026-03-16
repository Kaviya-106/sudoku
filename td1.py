def insert_tableau (indice, valeur, liste):
    liste1=[]
    for j in liste:
        if j==indice:
            liste1.append(valeur)
        liste1.append(j)
    return liste1

l=[1,2,3,1]
print (insert_tableau(2, 12, l))

def suppression_tableau (liste, indice):
    for i in range(len(liste)-1):
        if i>= indice:
            liste[i]=liste[i+1]
    liste.pop()
    return liste

print(suppression_tableau(l, 2))  

def minimun (liste):
    min=liste[0]
    for i in liste:
        if min<i:
            min=i
    return min

def tri_min (liste):
    for j in range (len(liste)):
        for k in range (len(liste)):
            if liste[j]<liste[k]:
                liste[j], liste[k]= liste[k], liste [j]
    return liste

def ajouter_trie (liste, valeur):
    liste1=[]
    insert=False
    for i in liste:
        if  valeur<=i and not insert:
            liste1.append(valeur)
            insert=True
        else: liste1.append(i)
    return liste1
l=tri_min([1,2,5,6,7,3])
print(ajouter_trie(l, 4))

def deplacer (liste, valeur):
    for i in liste:
        if i<valeur:
            i=valeur
    return liste
print(deplacer([1,2,5,2,3,4,9,8],5))
