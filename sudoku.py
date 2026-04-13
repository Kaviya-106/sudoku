import tkinter as tk
import random
import copy

fenetre=tk.Tk()
fenetre.title("jeu soudoku")

def fermer_fenetre ():
    fenetre.destroy()


text_canva={}
grille=[[0]*9 for _ in range (9)]

x_sauv=0
y_sauv=0
x_ecran=0
y_ecran=0
grille_sol=[]

def est_possible(grille, lig, col, nombre):
    if nombre in grille[lig]:
        return False
    if nombre in [grille[i][col] for i in range(9)]:
        return False
    lig0 = (lig // 3) * 3
    col0 = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grille[lig0+i][col0+j] == nombre:
                return False
    return True


def remplir_grille(grille):
    for lig in range(9):
        for col in range(9):
            if grille[lig][col] == 0:
                nombres = list(range(1, 10))
                random.shuffle(nombres)
                for nombre in nombres:
                    if est_possible(grille, lig, col, nombre):
                        grille[lig][col] = nombre
                        if remplir_grille(grille):
                            return True
                        grille[lig][col] = 0
                return False
    return True

def disparition_chiffres(grille, nb_trous=40):
    cases = [(lig, col) for lig in range(9) for col in range(9)]
    random.shuffle(cases)
    for lig, col in cases[:nb_trous]:
        grille[lig][col] = None

def generer_grille():
    global grille, text_canva, x_ecran, y_ecran, grille_sol
    remplir_grille(grille)
    grille_sol=copy.deepcopy(grille)
    disparition_chiffres(grille)
    for lig in range(9):
        for col in range(9):
            x = (lig + 1.5) * taille
            y = (col + 1.5) * taille
            if grille[lig][col] is not None:
                x1 = (lig+1)*taille
                y1 = (col+1)*taille
                canva.create_rectangle(x1, y1, x1+taille, y1+taille, fill="#d3e3d3")
            text_canva[(lig-1, col-1)] = canva.create_text(x, y, text=grille[lig][col], font=(12))

def affichage_chiffre (event):
    global taille, canva, x_sauv, y_sauv, x_ecran, y_ecran, entry
    y_ecran=event.y
    x_ecran=event.x
    ligne = int(x_ecran//taille)-1
    colonne = int(y_ecran//taille)-1
    if (ligne, colonne) in text_canva:
        couleur = canva.itemcget(text_canva[(ligne, colonne)], "fill")
        if couleur == "green":
            return
    elif grille[ligne][colonne] is not None:
        return
    entry= tk.Entry(canva, bd=0, relief="flat", highlightthickness=0, bg="white",font=("Arial", 12), justify="center")
    x=(event.x//taille)*taille+taille//2
    y=(event.y//taille)*taille+taille//2
    canva.create_window(x, y, window=entry,width=taille-2, height=taille-2)
    entry.focus()
    entry.bind("<Return>", valider_chiffre)
 
def valider_chiffre (event):
    global entry
    remplir_chiffre(entry.get())
    entry.destroy()

def remplir_chiffre (nombre):
    global taille, canva, x_ecran, y_ecran, grille, text_canva, grille_sol
    ligne = int(x_ecran//taille)-1
    colonne = int(y_ecran//taille)-1 
    grille[ligne][colonne] = int(nombre)
    if grille[ligne][colonne] == grille_sol[ligne][colonne]:
        color = "green"
    else:
        color = "red"
    x1 = (ligne+1) * taille
    y1 = (colonne+1) * taille
    x2 = x1 + taille//2
    y2 = y1 + taille//2
    if (ligne, colonne) in text_canva:
        canva.delete(text_canva[(ligne, colonne)])
    text_canva[(ligne, colonne)] = canva.create_text(x2, y2, text=nombre, font=(12), fill=color)
    


boutton_quitter=tk.Button(fenetre, text='Quitter', command=fermer_fenetre)
boutton_quitter.grid(row=3, column=0)

canva=tk.Canvas(fenetre, width=500, height=500, background="white")
canva.grid(row=0, column=0, rowspan=3)

nombre_ligne=11
nombre_colonne=11
taille=500/nombre_colonne
for ligne in range(1, nombre_ligne-1):
    for colonne in range(1, nombre_colonne-1):
        x1=ligne*taille
        y1=colonne*taille
        canva.create_rectangle(x1,y1, x1+taille, y1+taille)

canva.bind("<Button-1>", affichage_chiffre)
generer_grille()
fenetre.mainloop()