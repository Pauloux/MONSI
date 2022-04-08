from fonctions_communes_et_parametres import *
import routine_convertir_donnees_serveur as routine
import Simulateur_capteur as simu
import creation_image as image
import alertes

verifier_fichiers()

temps_seuil_routine = get_temps()
temps_seuil_simu = get_temps()
temps_seuil_image = get_temps()
temps_seuil_alerte = get_temps()
#En secondes
acceleration = 20
delai_routine = 120 / acceleration
delai_simu = 10 / acceleration
delai_image = 120 / acceleration
delai_alerte = 120 / acceleration

#Récupère le nombre de lignes du fichier de sortie pour savoir quelle ligne récuperer dans le fichier d'entrée ensuite
numero_ligne = 0
simu.initialisation()

while True:
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
    #Pour ne pas sur-utiliser le processeur
    time.sleep(1 / acceleration)
