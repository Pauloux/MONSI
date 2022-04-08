import time

nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"
nom_fichier_donnees_brutes_simu = "../Documents/donnees_brutes.csv"
nom_fichier_capteur = "../Documents/Simulateur_donnees.csv"
nom_fichier_csv_serveur = "../Documents/csv_serveur.csv"
nom_fichier_alertes_historique = "../Documents/alertes_historique.txt"
nom_fichier_alertes_site = "../Documents/alertes_site.txt"

#En secondes
delai_entre_deux_alertes = 1800

#Liste des descripteurs que l'on récupère dans csv_serveur
descripteurs_csv_serveur = ["Date", "Time", "Wind Value", "Wind Condition", "Cloud Value", "Cloud Condition", "Ambient Temperature", "Rain Value", "Rain Condition"]

seuils = [
    {
        "nom" : "Vent",
        "numero_colonne_valeur" : 2,
        "numero_colonne_condition" : 3,
        "condition_moyenne" : "Windy",
        "condition_mauvaise" : "Very Windy",
        "minimum" : 0,
        "premier_seuil" : 5,
        "deuxieme_seuil" : 10,
        "maximum" : 40,
        "inverser_image" : False
    },
    {
        "nom" : "Nuage",
        "numero_colonne_valeur" : 4,
        "numero_colonne_condition" : 5,
        "condition_moyenne" : "Cloudy",
        "condition_mauvaise" : "Overcast",
        "minimum" : -30,
        "premier_seuil" : -5,
        "deuxieme_seuil" : 0,
        "maximum" : 40,
        "inverser_image" : False
    },
    {
        "nom" : "Pluie",
        "numero_colonne_valeur" : 7,
        "numero_colonne_condition" : 8,
        "condition_moyenne" : "Wet",
        "condition_mauvaise" : "Rain",
        "minimum" : 0,
        "premier_seuil" : 1700,
        "deuxieme_seuil" : 2000,
        "maximum" : 2800,
        "inverser_image" : True
    },
    {
        "nom" : "Temperature",
        "numero_colonne_valeur" : 6,
        "numero_colonne_condition" : None,
        "minimum" : -10,
        "premier_seuil" : 0,
        "deuxieme_seuil" : 20,
        "maximum" : 40,
        "inverser_image" : False
    }
]

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
    except:
        return False

def nombre_lignes(nom_fichier):
    if not fichier_existe(nom_fichier):
        return 0
    fichier = open(nom_fichier, "r")
    retour = len(fichier.readlines())
    fichier.close()
    return retour

def clear_fichier(nom_fichier):
    fichier = open(nom_fichier, "w")
    fichier.close()

def verifier_fichiers():
    #logs
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_logs):
        fichier_logs = open(nom_fichier_logs, "x")
        fichier_logs.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_logs)

    #erreurs
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_erreurs):
        fichier_erreurs = open(nom_fichier_erreurs, "x")
        fichier_erreurs.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_erreurs)

    #fichier donnees_brutes_simu
    #Vérifie si le fichier existe, sinon il lève une erreur
    if not fichier_existe(nom_fichier_donnees_brutes_simu):
        print("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        ecrire_logs("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        ecrire_erreur("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        raise ValueError("Fichier " + nom_fichier_donnees_brutes_simu + "inexistant")

    #Fichier_capteur
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_capteur):
        print("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_capteur)
        ecrire_logs("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_capteur)
        ecrire_erreur("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_capteur)
        fichier_sortie = open(nom_fichier_capteur, "x")
        fichier_sortie.close()

    #Fichier csv_serveur
    #Créer un fichier csv avec la liste des descripteur si le fichier n'existe pas
    if not fichier_existe(nom_fichier_csv_serveur):
        print("Routine : Fichier de sortie inexistant, création de " + nom_fichier_csv_serveur)
        ecrire_logs("Routine : Fichier de sortie inexistant, création de " + nom_fichier_csv_serveur)
        ecrire_erreur("Routine : Fichier de sortie inexistant, création de " + nom_fichier_csv_serveur)
        fichier_sortie = open(nom_fichier_csv_serveur, "a")
        fichier_sortie.write(",".join(descripteurs_csv_serveur))
        fichier_sortie.close()

    #Fichier alertes_historique
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_alertes_historique) :
        fichier_alertes_historique = open(nom_fichier_alertes_historique, "x")
        fichier_alertes_historique.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_alertes_historique)

    #Fichier alertes_site
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_alertes_site) :
        fichier_alertes_site = open(nom_fichier_alertes_site, "x")
        fichier_alertes_site.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_alertes_site)
