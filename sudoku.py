import tkinter as tk 
fenetre=tk.Tk()
fenetre.title("jeu soudoku")

def fermer_fenetre ():
    fenetre.destroy()


x_sauv=0
y_sauv=0
x_ecran=0
y_ecran=0


def affichage_chiffre (event):
    global taille, canva, x_sauv, y_sauv, x_ecran, y_ecran
    y_ecran=event.y
    x_ecran=event.x
    x_sauv=canva.winfo_rootx()+ event.x
    y_sauv=canva.winfo_rooty()+ event.y
    roue_chifffre= tk.Menu(fenetre, tearoff=0)
    roue_chifffre.add_command(label="1",command= lambda: remplir_chiffre("1"))
    roue_chifffre.add_command(label="2",command= lambda: remplir_chiffre("2"))
    roue_chifffre.add_command(label="3",command= lambda: remplir_chiffre("3"))
    roue_chifffre.add_command(label="4",command= lambda: remplir_chiffre("4"))
    roue_chifffre.add_command(label="5",command= lambda: remplir_chiffre("5"))
    roue_chifffre.add_command(label="6",command= lambda: remplir_chiffre("6"))
    roue_chifffre.add_command(label="7",command= lambda: remplir_chiffre("7"))
    roue_chifffre.add_command(label="8",command= lambda: remplir_chiffre("8"))
    roue_chifffre.add_command(label="9",command= lambda: remplir_chiffre("9"))
    roue_chifffre.tk_popup(x_sauv, y_sauv)

def remplir_chiffre (nombre):
    global taille, canva, x_ecran, y_ecran
    ligne=x_ecran//taille
    colonne=y_ecran//taille
    x1 = ligne * taille
    y1 = colonne * taille
    x2 = x1 + taille//2
    y2 = y1 + taille//2
    canva.create_text(x2, y2, text=nombre, font=( 12) )  
    


boutton_quitter=tk.Button(fenetre, text='Quitter', command=fermer_fenetre)
boutton_quitter.grid(row=3, column=0)

canva=tk.Canvas(fenetre, width=500, height=500, background="white")
canva.grid(row=0, column=0, rowspan=3)

nombre_ligne=9
nombre_colonne=9
taille=500/nombre_colonne
for ligne in range(1, nombre_ligne-1):
    for colonne in range(1, nombre_colonne-1):
        x1=ligne*taille
        y1=colonne*taille
        canva.create_rectangle(x1,y1, x1+taille, y1+taille)

canva.bind("<Button-1>", affichage_chiffre)

fenetre.mainloop()