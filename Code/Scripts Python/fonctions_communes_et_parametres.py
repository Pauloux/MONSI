import time
import datetime as dt
import shutil

#Définition des noms des fichiers et de leur chemins d'accès
nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"
nom_fichier_donnees_brutes_simu = "../Documents/donnees_brutes.csv"
nom_fichier_capteur = "../Documents/Simulateur_donnees.csv"
nom_fichier_csv_serveur = "../Documents/csv_serveur.csv"
nom_fichier_alertes_historique = "../Documents/alertes_historique.txt"
nom_fichier_alertes_site = "../Documents/alertes_site.txt"
nom_fichier_image_capteur_arrete = "../Documents/Capteur_arrete.png"
chemin_enregistrement_images = "../Documents/"

#En secondes
delai_entre_deux_alertes = 1800 #Cela correspond à 30 minutes

#Heure de lancement et d'arrêt du programme
heure_debut = "17h30"
heure_arret = "7h30"

#Défini ces variables pour qu'elles soient globales mais on leur affecte une valeur dans verifier_fichiers_et_initialisation()
horaire_debut_secondes = None
horaire_arret_secondes = None

#Liste des descripteurs que l'on récupère dans csv_serveur
descripteurs_csv_serveur = [
    {
    "nom" : "Date",
    "numero_colonne" : 0,
    "type" : "dernier"
    },
    {
    "nom" : "Time",
    "numero_colonne" : 1,
    "type" : "dernier"
    },
    {
    "nom" : "Wind Value",
    "numero_colonne" : 18,
    "type" : "valeur"
    },
    {
    "nom" : "Wind Condition",
    "numero_colonne" : 17,
    "type" : "condition"
    },
    {
    "nom" : "Cloud Value",
    "numero_colonne" : 5,
    "type" : "valeur"
    },
    {
    "nom" : "Cloud Condition",
    "numero_colonne" : 2,
    "type" : "condition"
    },
    {
    "nom" : "Ambient Temperature",
    "numero_colonne" : 9,
    "type" : "valeur"
    },
    {
    "nom" : "Rain Value",
    "numero_colonne" : 7,
    "type" : "valeur"
    },
    {
    "nom" : "Rain Condition",
    "numero_colonne" : 3,
    "type" : "condition"
    }
]

#Définition des seuils pour génerer les alertes et les images
seuils = [
    {
        "nom" : "Vent",
        "numero_colonne_valeur" : 2,
        "numero_colonne_condition" : 3,
        "condition_moyenne" : "Windy",
        "condition_mauvaise" : "Very Windy",
        "minimum" : 0,
        "premier_seuil" : 5,
        "deuxieme_seuil" : 10,
        "maximum" : 40,
        "inverser_image" : False
    },
    {
        "nom" : "Nuage",
        "numero_colonne_valeur" : 4,
        "numero_colonne_condition" : 5,
        "condition_moyenne" : "Cloudy",
        "condition_mauvaise" : "Overcast",
        "minimum" : -30,
        "premier_seuil" : -5,
        "deuxieme_seuil" : 0,
        "maximum" : 40,
        "inverser_image" : False
    },
    {
        "nom" : "Pluie",
        "numero_colonne_valeur" : 7,
        "numero_colonne_condition" : 8,
        "condition_moyenne" : "Wet",
        "condition_mauvaise" : "Rain",
        "minimum" : 0,
        "premier_seuil" : 1700,
        "deuxieme_seuil" : 2000,
        "maximum" : 2800,
        "inverser_image" : True
    },
    {
        "nom" : "Temperature",
        "numero_colonne_valeur" : 6,
        "numero_colonne_condition" : None,
        "minimum" : -10,
        "premier_seuil" : 0,
        "deuxieme_seuil" : 20,
        "maximum" : 40,
        "inverser_image" : False
    }
]

def get_heure():
    """
    Retourne l'heure actuelle sous le format Heures:Minutes:Secondes
    """

    return time.strftime("%H:%M:%S", time.localtime())

def get_temps():
    """
    Retourne l'Heure Unix
    """
    return time.time()

def ecrire_logs(ligne):
    """
    Ecrit dans le fichier de logs la ligne passée en argument en ajoutant l'heure au début de la ligne
    """

    fichier = open(nom_fichier_logs, "a")
    ligne = get_heure() + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_erreur(ligne):
    """
    Ecrit dans le fichier d'erreur la ligne passée en argument en ajoutant l'heure au début de la ligne
    """

    fichier = open(nom_fichier_erreurs, "a")
    ligne = get_heure() + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_alertes_historique(ligne):
    """
    Ecrit dans le fichier alertes_historique la ligne passée en argument en ajoutant l'Heure Unix au début de la ligne
    """

    fichier = open(nom_fichier_alertes_historique, "a")
    ligne = str(int(get_temps())) + " " + ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def ecrire_alertes_site(ligne):
    """
    Ecrit dans le fichier alertes_site la ligne passée en argument
    """

    fichier = open(nom_fichier_alertes_site, "a")
    ligne = ligne + "\n"
    fichier.write(ligne)
    fichier.close()

def fichier_existe(nom_fichier):
    """
    Renvoie True si le fichier passé en argument existe et peut être ouvert, renvoie False sinon
    """

    try:
        fichier = open(nom_fichier, "r")
        fichier.close()
        return True
    except:
        return False

def nombre_lignes(nom_fichier):
    """
    Renvoie le nombre de lignes du fichier passé en argument. Renvoie 0 si le fichier n'existe pas
    """
    if not fichier_existe(nom_fichier):
        return 0
    fichier = open(nom_fichier, "r")
    retour = len(fichier.readlines())
    fichier.close()
    return retour

def clear_fichier(nom_fichier):
    """
    Vide le fichier passé en argument
    """
    fichier = open(nom_fichier, "w")
    fichier.close()

def remplacer_images_capteur_arrete():
    """
    Remplace les graphiques Vent, Nuage, Pluie et Temperature par une image indiquant que le capteur est arrêté
    """

    for element in seuils:
        nom = element["nom"]
        nom_enregistrement = chemin_enregistrement_images + nom + ".png"
        shutil.copy(nom_fichier_image_capteur_arrete, nom_enregistrement)

def verifier_fichiers_et_initialisation():
    """
    Vérifie si tous les fichiers nécéssaires au fonctionnement du programme existent et les créés dans le cas échéant, sauf pour le fichier qui sert
    de base de données pour le simulateur puisqu'on ne peut pas l'inventer.
    """

    #logs
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_logs):
        print("Création du fichier de logs !")
        fichier_logs = open(nom_fichier_logs, "x")
        fichier_logs.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_logs)

    #erreurs
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_erreurs):
        print("Création du fichier d'erreurs !")
        fichier_erreurs = open(nom_fichier_erreurs, "x")
        fichier_erreurs.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_erreurs)

    #Fichier alertes_historique
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_alertes_historique):
        print("Création du fichier alertes_historique")
        fichier_alertes_historique = open(nom_fichier_alertes_historique, "x")
        fichier_alertes_historique.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_alertes_historique)

    #Fichier alertes_site
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_alertes_site) :
        print("Création du fichier alertes_site")
        fichier_alertes_site = open(nom_fichier_alertes_site, "x")
        fichier_alertes_site.close()
    #Puis le remet à zéro
    clear_fichier(nom_fichier_alertes_site)

    #fichier donnees_brutes_simu
    #Vérifie si le fichier existe, sinon il lève une erreur
    if not fichier_existe(nom_fichier_donnees_brutes_simu):
        print("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        ecrire_erreur("Simulateur : Fichier d'entrée inexistant, arrêt du Simulateur")
        raise ValueError("Fichier " + nom_fichier_donnees_brutes_simu + "inexistant")

    #Fichier_capteur
    #Créer le fichier s'il n'existe pas
    if not fichier_existe(nom_fichier_capteur):
        print("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_capteur)
        ecrire_erreur("Simulateur : Fichier de sortie inexistant, création de " + nom_fichier_capteur)
        fichier_sortie = open(nom_fichier_capteur, "x")
        fichier_sortie.close()

    #Fichier csv_serveur
    #Créer un fichier csv avec la liste des descripteur si le fichier n'existe pas
    if not fichier_existe(nom_fichier_csv_serveur):
        print("Routine : Fichier de sortie inexistant, création de " + nom_fichier_csv_serveur)
        ecrire_erreur("Routine : Fichier de sortie inexistant, création de " + nom_fichier_csv_serveur)
        fichier_sortie = open(nom_fichier_csv_serveur, "a")

        #Récupère la liste des descripteurs à écrire
        descripteurs = [descripteur["nom"] for descripteur in descripteurs_csv_serveur]

        fichier_sortie.write(",".join(descripteurs))
        fichier_sortie.write("\n")
        fichier_sortie.close()

    #Convertit les horaires de début et d'arrêt du programme en secondes
    def convertir_secondes(horaire):
        """
        Convertit en secondes l'horaire passée en argument sous la forme : 00h00 (ici correspondant à minuit)
        """

        horaire = horaire.split("h")
        heure = int(horaire[0])
        minute = int(horaire[1])
        return heure * 3600 + minute * 60

    #Convertit en secondes une fois au début du programme plutôt qu'à chaque appel
    global horaire_debut_secondes, horaire_arret_secondes
    horaire_debut_secondes = convertir_secondes(heure_debut)
    horaire_arret_secondes = convertir_secondes(heure_arret)

    #Vérifie que les horaires entrés sont corrects
    if horaire_debut_secondes < horaire_arret_secondes:
        raise ValueError("L'heure de début doit être après l'heure d'arrêt (car c'est pendant la nuit)")

def heure_pour_declencher():
    """
    Retourne True si l'heure est valide pour que les programmes se déclenchent, retourne False sinon.
    Les paramètres pour changer l'heure de début et de fin des programmes est dans fonction_communes_et_parametres
    """

    #Convertit l'heure actuelle en secondes
    horaire_actuelle = get_heure().split(":")

    heure = int(horaire_actuelle[0])
    minute = int(horaire_actuelle[1])
    seconde = int(horaire_actuelle[2])

    horaire_actuelle_secondes = heure * 3600 + minute * 60 + seconde

    if horaire_actuelle_secondes > horaire_debut_secondes or horaire_actuelle_secondes < horaire_arret_secondes:
        return True
    else:
        return False

def delai_secondes_ligne_et_mtn(ligne):
    """
    Retourne le délai en secondes entre l'heure où l'on appelle la fonction et l'heure contenue dans la ligne passée en argument. La ligne est au format de nos fichiers csv
    """

    date = ligne[0].split("-")
    heure = ligne[1].split(":")

    annee = int(date[0])
    mois = int(date[1])
    jour = int(date[2])

    seconde = int(heure[2])
    minute = int(heure[1])
    #Attnetion, remplace le contenu de la variable heure
    heure = int(heure[0])

    #Calcule la différence en secondes entre la date de la ligne et la date actuelle
    heure_lue = dt.datetime(annee, mois, jour, heure, minute, seconde)
    heure_actuelle = dt.datetime.now()

    difference_en_secondes = int((heure_actuelle - heure_lue).total_seconds())

    return difference_en_secondes
