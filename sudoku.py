import tkinter as tk 
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


def affichage_chiffre (event):
    global taille, canva, x_sauv, y_sauv, x_ecran, y_ecran, entry
    y_ecran=event.y
    x_ecran=event.x
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
    global taille, canva, x_ecran, y_ecran, grille, text_canva
    ligne = int(x_ecran//taille)-1
    colonne = int(y_ecran//taille)-1
    grille[ligne][colonne] = int(nombre)
    x1 = (ligne+1) * taille
    y1 = (colonne+1) * taille
    x2 = x1 + taille//2
    y2 = y1 + taille//2
    if (ligne, colonne) in text_canva:
        canva.delete(text_canva[(ligne, colonne)])
    text_canva[(ligne, colonne)] = canva.create_text(x2, y2, text=nombre, font=(12))
    


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

fenetre.mainloop()