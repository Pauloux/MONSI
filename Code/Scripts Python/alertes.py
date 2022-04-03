from fonctions_communes_et_parametres import *

def lancer():
    clear_fichier(nom_fichier_alertes_site)
    #Recupere les alerets deja ecrites pour ne pas faire des alertes toutes les 2 minutes
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "r")
    lignes = fichier_alertes_historique.readlines()
    contenu_nouveau_fichier = []
    alertes_deja_ecrites = []
    for ligne in lignes:
        nom_alerte = ligne.split()[1]
        temps_alerte = int(ligne.split()[0])
        temps_actuel = int(get_temps())
        difference_secondes = temps_actuel - temps_alerte
        #Supprime les alertes du fichier historique toutes les x secondes
        if difference_secondes < 180:
            contenu_nouveau_fichier.append(ligne)
            alertes_deja_ecrites.append(nom_alerte)
    fichier_alertes_historique.close()

    #Réécrit le fichier historique avec les bonnes lignes
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "w")
    for ligne in contenu_nouveau_fichier:
        fichier_alertes_historique.write(ligne)
    fichier_alertes_historique.close()

    #Récupère les valeurs
    fichier_csv = open(nom_fichier_csv_serveur, "r")
    derniere_ligne = fichier_csv.readlines()[-1]
    derniere_ligne = derniere_ligne.split(",")    
    fichier_csv.close()

    #Verifie s'il y a des alertes
    for element in seuils:
        valeur = float(derniere_ligne[element["numero_colonne"]])
        if element["nom"] == "Pluie":
            valeur = element["maximum"] - valeur
        nom_alerte_2 = element["nom"] + "_2"
        nom_alerte_1 = element["nom"] + "_1"
        #Ajoute les alertes que si elles n'y sont pas deja
        if valeur > element["deuxieme_seuil"] and nom_alerte_2 not in alertes_deja_ecrites:
            ecrire_alertes_historique(nom_alerte_2)
            ecrire_alertes_site(nom_alerte_2)
            ecrire_logs("Alertes : alerte " + nom_alerte_2 + " ecrite")
            print("Alertes : alerte " + nom_alerte_2 + " ecrite")
        elif valeur > element["premier_seuil"] and nom_alerte_1 not in alertes_deja_ecrites:
            ecrire_alertes_historique(nom_alerte_1)
            ecrire_alertes_site(nom_alerte_1)
            ecrire_logs("Alertes : alerte " + nom_alerte_1 + " ecrite")
            print("Alertes : alerte " + nom_alerte_1 + " ecrite")
