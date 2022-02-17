import time
import routine_convertir_donnees_serveur as routine
import Simulateur_capteur as simu

temps_seuil_routine = time.time()
temps_seuil_simu = time.time()
#En secondes
delai_routine = 120
delai_simu = 10

numero_ligne = 0
simu.initialisation()

print("lancement Simulateur et Routine")

while True:
    temps_actu = time.time()
    if temps_actu >= temps_seuil_routine:
        print(time.strftime("%H:%M:%S", time.localtime()), "Routine")
        routine.lancer()
        temps_seuil_routine += delai_routine
    if temps_actu >= temps_seuil_simu:
        print(time.strftime("%H:%M:%S", time.localtime()), "Simulateur")
        simu.lancer()
        temps_seuil_simu += delai_simu
    #Pour ne pas sur-utiliser le processeur
    time.sleep(0.1)
