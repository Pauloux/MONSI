import matplotlib.pyplot as plt
from fonctions_communes_et_parametres import *

def get_derniere_heure(fichier):
  """
  Renvoie un tableau de tableau. Il y a 31 sous-tableau et chaque sous-tableau est une ligne du fichier passé en argument.
  On a ainsi les 31 dernières lignes du fichier passé en argument, donc les valeurs de la dernière heure du capteur.
  """

  #Récupère les 30 dernières lignes
  tableau = fichier.readlines()[-31:]

  #Remet le curseur de lecture au début du fichier
  fichier.seek(0, 0)

  #Convertit les lignes en tableaux pour pouvoir accéder aux données que l'on souhaite
  for indice_ligne in range(len(tableau)):
    #On pense a enlever le retour à la ligne
    tableau[indice_ligne] = tableau[indice_ligne][:-1].split(",")
  return tableau

def get_date_heure(tableau):
    """
    Renvoie la date et l'heure de la dernière ligne du fichier csv_serveur sous le format : Date | Heure
    """

    #On récupère la dernière ligne du fichier
    ligne = tableau[-1]
    date = ligne[0]
    heure = ligne[1]
    return date + " | " + heure

def get_abscisse(tableau):
    """
    Renvoie un tableau de valeur correspondant aux valeurs des abscisses des points à dessiner sur la dernière heure.
    Permet de ne pas afficher les points invalides (trop éloignés en temps)
    """

    abscisses = []
    for indice_ligne in range(31):
        #Récupère les données
        ligne = tableau[indice_ligne]
        difference_en_secondes = delai_secondes_ligne_et_mtn(ligne)

        #Si la ligne est trop ancienne, on ne l'affiche pas (On met NaN)
        if difference_en_secondes <= 3600:
            minutes_abscisses = -(60-(indice_ligne * 2))
            abscisses.append(minutes_abscisses)
        else:
            abscisses.append(float("NaN"))

    return abscisses

def get_ordonnee(num_colonne, tableau):
    """
    Renvoie un tableau de valeur correspondante aux 30 dernières valeurs de la colonne passé en argument (num_colonne)
    """

    ordonnees = []
    for ligne in range(31):
      valeur = tableau[ligne][num_colonne]
      #Remplace les virgules par des points pour pouvoir les convertir en float
      valeur = valeur.replace(",", ".")
      valeur = float(valeur)
      ordonnees.append(valeur)

    return ordonnees

def generer_image(minimum, premier_palier, deuxieme_palier, maximum, num_colonne, titre, tableau, inverser, **kargs):
    """
    Génère une image à partir des paramètres passés en arguments.
    Arguments attendus :
        valeur minimum, valeur du premier palier, valeur du deuxième palier, valeur maximale,
        numéro de la colonne dont on récupère les valeurs pour faire le graphique, titre du graphique, fichier où
        sont stockées les valeurs, si l'on doit inverser l'axe des ordonnées.
    Des paramètres peuvent être modifié en faisant à la fin des paramères obligatoires : nom_parametre = valeur
    On retrouve dans ces paramètres optionnels qui ont une valeur par défaut autrement:
        couleur de la première zone, couleur de la deuxième zone, couleur de la troisième zone, couleur du texte
        et des axes, couleur du trait représentant les valeurs, la valeur du canal alpha et le nom de l'axe des ordonnées.
    """

    #Stocke les paramètres dans un dictionnaire, permettant de mettre des valeurs par défaut et de les modifier si besoin.
    parametres = {
        "minimum" : minimum,
        "premier_palier" : premier_palier,
        "deuxieme_palier" : deuxieme_palier,
        "maximum" : maximum,
        "num_colonne" : num_colonne,
        "titre" : titre,
        "couleur_premiere_zone" : "#85C58C",
        "couleur_deuxieme_zone" : "#DCDD78",
        "couleur_troisieme_zone" : "#FF6961",
        "couleur_ecriture" : "#BBE1FA",
        "couleur_trait" : "black",
        "alpha" : 1,
        "inverser" : inverser,
        "nom_axe_y" : None
    }

    #Modifie les paramètres par ceux passés en arguments optionnels
    for cle, valeur in kargs.items():
        #Lève une erreur si le nom du paramètre n'existe pas
        if cle in parametres.keys():
            parametres[cle] = valeur
        else:
            raise ValueError("mauvais nom de variable passé en argument")

    #Récupère les valeurs des abscisses
    abscisse = get_abscisse(tableau)
    #Récupère les valeurs des ordonnées
    ordonnees = get_ordonnee(parametres["num_colonne"], tableau)

    #Inverse les valeur si besoin
    if parametres["inverser"]:
        ordonnees = [parametres["maximum"] - element for element in ordonnees]

    #Dessine le trait des valeurs
    plt.plot(abscisse, ordonnees, color=parametres["couleur_trait"])

    #Dessine les trois zones en fond
    plt.axhspan(parametres["minimum"], parametres["premier_palier"], facecolor=parametres["couleur_premiere_zone"], alpha=parametres["alpha"])
    plt.axhspan(parametres["premier_palier"], parametres["deuxieme_palier"], facecolor=parametres["couleur_deuxieme_zone"], alpha=parametres["alpha"])
    plt.axhspan(parametres["deuxieme_palier"], parametres["maximum"], facecolor=parametres["couleur_troisieme_zone"], alpha=parametres["alpha"])

    #Ajoute le titre
    titre_image = parametres["titre"] + "\n" + get_date_heure(tableau)
    plt.title(titre_image, color=parametres["couleur_ecriture"])

    #Modifie la couleur des axes
    plt.xticks(color=parametres["couleur_ecriture"])
    plt.yticks(color=parametres["couleur_ecriture"])

    #Ajoute le nom des axes. L'axe des ordonnées n'a pas de nom par défaut
    plt.xlabel("Minutes", color=parametres["couleur_ecriture"])
    if parametres["nom_axe_y"] != None:
        plt.ylabel(parametres["nom_axe_y"], color=parametres["couleur_ecriture"])

    #Place deux points invisibles en -60, 0 pour que le graphique aille de -60 à 0 même quand il n'y a pas de valeurs au lancement du programme
    #0 est une valeur arbitraire qui est commune à toutes les plages des graphiques
    plt.plot(-60, 0)
    plt.plot(0, 0)

    #Enregistre le fichier
    nom_fichier = chemin_enregistrement_images + parametres["titre"] + ".png"
    plt.savefig(nom_fichier, transparent=True)

    #Réinitialise le graphique pour qu'il n'y ait pas d'interférence avec le prochain
    plt.cla()

def lancer():
    """
    Fonction principale de creation_image. Genère les images pour le site avec les valeurs sur la dernière heure.
    """

    #Securite
    #S'il n'y a pas assez de lignes, on arrete tout (31 + 1 de descripteurs)
    if nombre_lignes(nom_fichier_csv_serveur) < 32:
        print("Image : valeurs d'entrées insuffisantes")
        ecrire_erreur("Image : valeurs d'entrés insuffisantes")
        return

    #Récupère dans un tableau les valeurs de la dernière heure car on va l'utiliser plusieurs fois
    fichier = open(nom_fichier_csv_serveur, "r")
    tableau_valeurs_derniere_heure = get_derniere_heure(fichier)
    fichier.close()
    
    #Génère les images une par une
    for element in seuils:
        generer_image(element["minimum"], element["premier_seuil"], element["deuxieme_seuil"], element["maximum"], element["numero_colonne_valeur"], element["nom"], tableau_valeurs_derniere_heure, element["inverser_image"])
