from fonctions_communes_et_parametres import *
import routine_convertir_donnees_serveur as routine
import Simulateur_capteur as simu
import creation_image as image
import alertes

#Vérification que les fichiers existes
print("Vérification des fichiers...", end=" ")
verifier_fichiers_et_initialisation()
print("Fichiers vérifiés !")

#Initialisation des timers
temps_seuil_routine = get_temps()
temps_seuil_simu = get_temps()
temps_seuil_image = get_temps()
temps_seuil_alerte = get_temps()

#Définition des délais d'exécution(en secondes)
acceleration = 1 #A retirer lors de la fin du projet, uniquement pour les tests
delai_routine = 120 / acceleration
delai_simu = 10 / acceleration
delai_image = 120 / acceleration
delai_alerte = 120 / acceleration

#Uniquement pour le simulateur
#Récupère le nombre de lignes du fichier de sortie pour savoir quelle ligne récuperer dans le fichier d'entrée ensuite
numero_ligne = 0
print("Initialisation du simulateur...", end=" ")
simu.initialisation()
print("Simulateur initialisé !")

print("Lancement du programme !")

while True:
    #Vérifie si c'est la bonne heure pour déclencher le programme
    if not heure_pour_declencher():
        remplacer_images_capteur_arrete()
        #Attends 1 minute avant de revérifier
        time.sleep(60)
        continue

    #Déclenchement des autres scripts au bon moment
    temps_actu = get_temps()
    if temps_actu >= temps_seuil_routine:
        routine.lancer()
        temps_seuil_routine += delai_routine
    if temps_actu >= temps_seuil_simu:
        simu.lancer()
        temps_seuil_simu += delai_simu
    if temps_actu >= temps_seuil_image:
        image.lancer()
        temps_seuil_image += delai_image
    if temps_actu >= temps_seuil_alerte:
        alertes.lancer()
        temps_seuil_alerte += delai_alerte
        
    #On attend un peu pour ne pas sur-utiliser le processeur
    time.sleep(1 / acceleration)
