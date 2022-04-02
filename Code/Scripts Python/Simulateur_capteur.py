import time

nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"
nom_fichier_entree = "../Documents/donnees_brutes.csv"
nom_fichier_sortie = "../Documents/Simulateur_donnees.csv"

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

def fichier_existe(nom_fichier):
    try:
        fichier = open(nom_fichier, "r")
        fichier.close()
        return True
    except IOError as message_erreur:
        return False

def initialisation():
    #Crée le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_sortie):
        print("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
        ecrire_logs("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
        ecrire_erreur("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
        fichier_sortie = open(nom_fichier_sortie, "x")
        fichier_sortie.close()

    fichier_sortie = open(nom_fichier_sortie, "r")

    global numero_ligne
    numero_ligne = len(fichier_sortie.readlines())

    fichier_sortie.close()

def lancer():
    global numero_ligne

    #Vérifie si le fichier d'entrée existe
    if not fichier_existe(nom_fichier_entree):
        print("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        ecrire_logs("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        ecrire_erreur("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        return None

    #Ouvre les fichiers
    fichier_entree = open(nom_fichier_entree, "r")
    fichier_sortie = open(nom_fichier_sortie, "a")

    #Saute les lignes non necessaires
    for indice in range(numero_ligne):
        fichier_entree.readline()

    #Ecrit dans la fichier
    fichier_sortie.write(fichier_entree.readline())

    #Passe a la ligne suivante
    numero_ligne += 1

    #Ferme les fichiers
    fichier_entree.close()
    fichier_sortie.close()
