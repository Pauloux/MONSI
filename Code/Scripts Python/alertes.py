import time

nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"
nom_fichier_csv_serveur = "../Documents/csv_serveur.csv"
nom_fichier_alertes_historique = "../Documents/alertes_historique.txt"
nom_fichier_alertes_site = "../Documents/alertes_site.txt"

def get_heure():
    return time.strftime("%H:%M:%S", time.localtime())

def get_temps():
    return time.time()

def ecrire_logs(ligne):
    fichier = open(nom_fichier_logs, "a")
    ligne = get_heure() + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_erreur(ligne):
    fichier = open(nom_fichier_erreurs, "a")
    ligne = get_heure() + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_alertes_historique(ligne):
    fichier = open(nom_fichier_alertes_historique, "a")
    ligne = str(int(get_temps())) + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_alertes_site(ligne):
    fichier = open(nom_fichier_alertes_site, "a")
    ligne = ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def fichier_existe(nom_fichier):
    try:
        fichier = open(nom_fichier, "r")
        fichier.close()
        return True
    except IOError as message_erreur:
        return False

def clear_fichier(nom_fichier):
    fichier = open(nom_fichier, "w")
    fichier.close()

#Creer les fichiers s'ils n'existent pas
if not fichier_existe(nom_fichier_alertes_historique) :
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "x")
    fichier_alertes_historique.close()
if not fichier_existe(nom_fichier_alertes_site) :
    fichier_alertes_site = open(nom_fichier_alertes_site, "x")
    fichier_alertes_site.close()

#Vide les fichiers
clear_fichier(nom_fichier_alertes_historique)
clear_fichier(nom_fichier_alertes_site)

seuils = [
    {
        "nom" : "Vent",
        "numero_colonne" : 8,
        "minimum" : 0,
        "premier_seuil" : 5,
        "deuxieme_seuil" : 10,
        "maximum" : 40
    },
    {
        "nom" : "Nuage",
        "numero_colonne" : 3,
        "minimum" : -30,
        "premier_seuil" : -5,
        "deuxieme_seuil" : 0,
        "maximum" : 40
    },
    {
        "nom" : "Pluie",
        "numero_colonne" : 5,
        "minimum" : 0,
        "premier_seuil" : 1700,
        "deuxieme_seuil" : 2000,
        "maximum" : 2800
    },
    {
        "nom" : "Temperature",
        "numero_colonne" : 6,
        "minimum" : -10,
        "premier_seuil" : 0,
        "deuxieme_seuil" : 20,
        "maximum" : 40
    }
]

def lancer():
    clear_fichier(nom_fichier_alertes_site)
    #Recupere les alerets deja ecrites pour ne pas faire des alertes toutes les 2 minutes
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "r")
    lignes = fichier_alertes_historique.readlines()
    contenu_nouveau_fichier = []
    alertes_deja_ecrites = []
    for ligne in lignes:
        nom_alerte = ligne.split()[1]
        temps_alerte = int(ligne.split()[0])
        temps_actuel = int(get_temps())
        difference_secondes = temps_actuel - temps_alerte
        #Supprime les alertes du fichier historique toutes les x secondes
        if difference_secondes < 180:
            contenu_nouveau_fichier.append(ligne)
            alertes_deja_ecrites.append(nom_alerte)
    fichier_alertes_historique.close()

    #Réécrit le fichier historique avec les bonnes lignes
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "w")
    for ligne in contenu_nouveau_fichier:
        fichier_alertes_historique.write(ligne)
    fichier_alertes_historique.close()

    #Récupère les valeurs
    fichier_csv = open(nom_fichier_csv_serveur, "r")
    derniere_ligne = fichier_csv.readlines()[-1]
    derniere_ligne = derniere_ligne.split(",")    
    fichier_csv.close()

    #Verifie s'il y a des alertes
    for element in seuils:
        valeur = float(derniere_ligne[element["numero_colonne"]])
        if element["nom"] == "Pluie":
            valeur = element["maximum"] - valeur
        nom_alerte_2 = element["nom"] + "_2"
        nom_alerte_1 = element["nom"] + "_1"
        #Ajoute les alertes que si elles n'y sont pas deja
        if valeur > element["deuxieme_seuil"] and nom_alerte_2 not in alertes_deja_ecrites:
            ecrire_alertes_historique(nom_alerte_2)
            ecrire_alertes_site(nom_alerte_2)
            ecrire_logs("Alertes : alerte " + nom_alerte_2 + " ecrite")
            print("Alertes : alerte " + nom_alerte_2 + " ecrite")
        elif valeur > element["premier_seuil"] and nom_alerte_1 not in alertes_deja_ecrites:
            ecrire_alertes_historique(nom_alerte_1)
            ecrire_alertes_site(nom_alerte_1)
            ecrire_logs("Alertes : alerte " + nom_alerte_1 + " ecrite")
            print("Alertes : alerte " + nom_alerte_1 + " ecrite")