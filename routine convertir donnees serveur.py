descripteurs = ["Date", "Time", "Cloud Condition", "Cloud Value", "Rain Condition", "Rain Value", "Ambient Temperature", "Wind Condition", "Wind Value", "Switch Status"]
try:
    fichier_sortie = open("csv_serveur.csv", "r")
    fichier_sortie.close()
except:
    fichier_sortie = open("csv_serveur.csv", "a")
    fichier_sortie.write(",".join(descripteurs))
    fichier_sortie.write("\n")
    fichier_sortie.close()

fichier_sortie = open("csv_serveur.csv", "a")
fichier_sortie.close()

fichier_entree = open("extrait_donnees_brutes.csv", "r")
def get_2derniere_mins (fichier):
    tab = []
    fichier.readline()
    for row in range(12):
        ligne = fichier.readline()[1:-3]
        ligne = ligne.split('","')
        tab.append(ligne)
    return tab

print(get_2derniere_mins(fichier_entree))

fichier_entree.close()