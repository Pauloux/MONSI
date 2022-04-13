from fonctions_communes_et_parametres import *

def lancer():
    """
    Fonction principale de alertes. Genère les alertes à afficher sur le site, et fait en sorte de ne pas le surcharger non plus
    en mettant un délai minimum entre chaque alerte de même type.
    """
    clear_fichier(nom_fichier_alertes_site)
    #Securite
    #S'il n'y a pas assez de lignes, on arrete tout (1 + 1 de descripteurs)
    if nombre_lignes(nom_fichier_csv_serveur) < 2:
        print("Alerte : valeurs d'entrées insuffisantes")
        ecrire_erreur("Alerte : valeurs d'entrés insuffisantes")
        return

    #Recupere les alertes deja ecrites pour ne pas faire des alertes à chaque appel
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "r")

    lignes = fichier_alertes_historique.readlines()
    alertes_deja_ecrites = []
    contenu_nouveau_fichier = []

    #On récupère les alertes déjà présentes dans le fichier alertes historique
    for ligne in lignes:
        nom_alerte = ligne.split()[1]
        temps_alerte = int(ligne.split()[0])
        temps_actuel = int(get_temps())
        difference_secondes = temps_actuel - temps_alerte
        #Supprime les alertes du fichier historique au bout d'un moment, sinon, les réécrit dans le fichier
        if difference_secondes < delai_entre_deux_alertes:
            contenu_nouveau_fichier.append(ligne)
            alertes_deja_ecrites.append(nom_alerte)
    fichier_alertes_historique.close()

    #Réécrit le fichier historique avec les bonnes lignes
    clear_fichier(nom_fichier_alertes_historique)
    fichier_alertes_historique = open(nom_fichier_alertes_historique, "a")
    for ligne in contenu_nouveau_fichier:
        fichier_alertes_historique.write(ligne)
    fichier_alertes_historique.close()

    #Récupère les valeurs du fichier csv_serveur
    fichier_csv = open(nom_fichier_csv_serveur, "r")
    derniere_ligne = fichier_csv.readlines()[-1]
    derniere_ligne = derniere_ligne.split(",")
    fichier_csv.close()

    #Verifie s'il y a des alertes
    for element in seuils:
        numero_colonne = element["numero_colonne_condition"]
        if numero_colonne != None:
            valeur = derniere_ligne[numero_colonne]
            nom = element["nom"]
            nom_alerte_1 = nom + "_1"
            nom_alerte_2 = nom + "_2"
            #Ajoute les alertes que si elles n'y sont pas déjà
            if valeur == element["condition_moyenne"] and nom_alerte_1 not in alertes_deja_ecrites:
                ecrire_alertes_historique(nom_alerte_1)
                ecrire_alertes_site(nom_alerte_1)
                print("alerte 1")
            if valeur == element["condition_mauvaise"] and nom_alerte_2 not in alertes_deja_ecrites:
                ecrire_alertes_historique(nom_alerte_2)
                ecrire_alertes_site(nom_alerte_2)
                print("alerte 2")


