def initialisation():
    #Crée le fichier s'il n'existe pas
    try:
        fichier_sortie = open("Simulateur_donnees.csv", "r")
        fichier_sortie.close()
    except IOError as message_erreur:
        fichier_sortie = open("Simulateur_donnees.csv", "a")
        fichier_sortie.close()

    fichier_sortie = open("Simulateur_donnees.csv", "r")
    
    global numero_ligne
    numero_ligne = len(fichier_sortie.readlines())

    fichier_sortie.close()

def lancer():
    global numero_ligne
    #Ouvre les fichiers
    fichier_entree = open("donnees_brutes.csv", "r")
    fichier_sortie = open("Simulateur_donnees.csv", "a")

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
