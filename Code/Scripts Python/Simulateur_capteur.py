from fonctions_communes_et_parametres import *

def initialisation():
    """
    Initialise le simulateur du capteur
    """
    #Modifie la variable globale numero_ligne pour que le capteur sache quelle ligne lire dans sa base de données
    global numero_ligne
    numero_ligne = nombre_lignes(nom_fichier_capteur)

def lancer():
    """
    Fonction principale de Simulateur_capteur. Simulte le fonctionnement du
    capteur que nous n'avons pas en ajoutant une ligne dans le fichier
    de sortie toutes les 10 secondes, comme le capteur le fera.
    """
    #Met la variable numero_ligne en global
    global numero_ligne

    #Ouvre les fichiers
    fichier_entree = open(nom_fichier_donnees_brutes_simu, "r")
    fichier_sortie = open(nom_fichier_capteur, "a")

    #Saute les lignes non necessaires
    for indice in range(numero_ligne):
        fichier_entree.readline()

    #Ecrit dans le fichier la bonne ligne de la base de données
    fichier_sortie.write(fichier_entree.readline())

    #Passe a la ligne suivante pour le prochain appel de la fonction
    numero_ligne += 1

    #Ferme les fichiers
    fichier_entree.close()
    fichier_sortie.close()
