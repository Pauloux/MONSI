import time
import routine_convertir_donnees_serveur as routine
import Simulateur_capteur as simu
import creation_image as image
import alertes

nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"

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

#Création et remise a zéro des fichiers de logs et d'erreurs:
#Création des fichiers s'ils n'existent pas
if not fichier_existe(nom_fichier_logs) :
    fichier_logs = open(nom_fichier_logs, "x")
    fichier_logs.close()
if not fichier_existe(nom_fichier_erreurs) :
    fichier_erreurs = open(nom_fichier_erreurs, "x")
    fichier_erreurs.close()
#Remise a zéro des fichiers de logs et d'erreurs
fichier_logs = open(nom_fichier_logs, "w")
fichier_logs.close()
fichier_erreurs = open(nom_fichier_erreurs, "w")
fichier_erreurs.close()

temps_seuil_routine = get_temps()
temps_seuil_simu = get_temps()
temps_seuil_image = get_temps()
temps_seuil_alerte = get_temps()
#En secondes
acceleration = 10
delai_routine = 120 / acceleration
delai_simu = 10 / acceleration
delai_image = 120 / acceleration
delai_alerte = 120 / acceleration

#Récupère le nombre de lignes du fichier de sortie pour savoir quelle ligne récuperer dans le fichier d'entrée ensuite
numero_ligne = 0
simu.initialisation()

while True:
    temps_actu = time.time()
    if temps_actu >= temps_seuil_routine:
        print(get_heure() + " : Exécution Routine")
        ecrire_logs("Exécution Routine")
        routine.lancer()
        temps_seuil_routine += delai_routine
    if temps_actu >= temps_seuil_simu:
        print(get_heure() + " : Exécution Simulateur")
        ecrire_logs("Exécution Simulateur")
        simu.lancer()
        temps_seuil_simu += delai_simu
    if temps_actu >= temps_seuil_image:
        print(get_heure() + " : Exécution Image")
        ecrire_logs("Exécution Image")
        image.lancer()
        temps_seuil_image += delai_image
    if temps_actu >= temps_seuil_alerte:
        print(get_heure() + " : Exécution Alerte")
        ecrire_logs("Exécution Alerte")
        alertes.lancer()
        temps_seuil_alerte += delai_alerte
    #Pour ne pas sur-utiliser le processeur
    time.sleep(1 / acceleration)