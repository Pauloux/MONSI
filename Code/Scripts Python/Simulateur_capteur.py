from fonctions_communes_et_parametres import *

def initialisation():
    #Crée le fichier s'il n'existe pas
    fichier_sortie = open(nom_fichier_capteur, "r")

    global numero_ligne
    numero_ligne = len(fichier_sortie.readlines())

    fichier_sortie.close()

def lancer():
    global numero_ligne

    #Ouvre les fichiers
    fichier_entree = open(nom_fichier_donnees_brutes_simu, "r")
    fichier_sortie = open(nom_fichier_capteur, "a")
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
