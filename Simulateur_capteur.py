import time

#Est-t-il mieux de tout le temps laisser les fichiers ouverts ?

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

print("Lancement simulateur")
numero_ligne = 0
initialisation()

temps_seuil = time.time()
#En secondes
delai = 10

while True:
    temps_actu = time.time()
    if temps_actu >= temps_seuil:
        print(time.strftime("%H:%M:%S", time.localtime()))
        lancer()
        temps_seuil += delai
    #Pour ne pas sur-utiliser le processeur
    time.sleep(0.1)
