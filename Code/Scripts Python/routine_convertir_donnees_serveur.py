from fonctions_communes_et_parametres import *

def get_2derniere_mins(fichier):
  """
  Renvoie un tableau de tableau. Il y a 12 sous-tableau et chaque sous-tableau est une ligne du fichier passé en argument.
  On a ainsi les 12 dernières lignes du fichier passé en argument, donc les valeurs des 2 dernières minutes du capteur.
  """

  #Récupère les 12 dernières lignes
  tableau = fichier.readlines()[-12:]

  for indice_ligne in range(len(tableau)):
    #Si la ligne est trop petite, on passe la ligne car elle causerait une erreur lors de la conversion en liste
    if len(tableau[indice_ligne]) < 5:
        tableau[indice_ligne] = "Fausse ligne"
        ecrire_erreur("Fausse ligne ajoutée " + str(tableau[indice_ligne]))
    else:
        #Autrement, on enlève le " au début de la ligne et le ", a la fin de la ligne puis on split cette ligne par les ","
        #Pour ainsi n'avoir que les valeurs
        tableau[indice_ligne] = tableau[indice_ligne][1:-3].split('","')
  return tableau

def moyenne_2mins(fichier):
  """
  Renvoie un tableau avec les moyennes des valeurs des deux dernières minutes pour les données qui nous intéréssents uniquement.
  On a ainsi:
    Date, Heure, Valeur du Vent, Condition du Vent, Valeur des nuages, Condition nuageuse, Temperature ambiante, Valeur de la pluie, Condition pluvieuse.
  """

  #On récupère le tableau des valeurs des deux dernières minutes
  tableau = get_2derniere_mins(fichier)

  def ligne_est_valide(ligne):
    """
    Prend en entrée l'argument ligne, qui est l'index de la ligne a vérfier. Renvoie True si la ligne est au format
    que notre routine peut traiter, renvoie False sinon.
    """

    #Si le premier élément est date, alors c'est une ligne de descripteur, et s'il n'y a pas 19  éléments, alors il
    #y a eu un problème avec le capteur
    return tableau[ligne][0]!="Date" and len(tableau[ligne]) == 19


  def get_derniere_valeur(num_colonne):
    """
    Renvoie la valeur présente dans la dernière ligne du fichier et à l'indice num_colonne passé en argument.
    """

    #Recherche de la dernière ligne valide
    indice_ligne = -1
    while not ligne_est_valide(indice_ligne) and indice_ligne > -12:
      indice_ligne -= 1

    #Renvoie la chaine "None" si aucune ligne n'est valide
    if indice_ligne > -12:
        return tableau[indice_ligne][num_colonne]
    else:
        return "None"

  def get_moyenne_colonne(num_colonne):
    """
    Renvoie la moyenne des valeurs de la colonne que l'on a passé en argument(numero de colonne) des 12 dernières lignes ajoutées au fichier (donc 2 minutes)
    """

    somme = 0
    for ligne in range(12):
      #Passe la ligne si elle n'est pas valide
      if not ligne_est_valide(ligne):
        continue
      valeur = tableau[ligne][num_colonne]

      #Remplace les virgules par des points pour pouvoir les convertir en float
      valeur = valeur.replace(",", ".")
      somme += float(valeur)

    #On retourne le résultat arrondis et sous forme de chaine de caractere pour l'injecter dans le document csv ensuite
    return str(round(somme / 12, 1))

  def get_valeur_majoritaire_colonne(num_colonne):
    """
    Renvoie la chaine de caractère majoritaire de la colonne que l'on a passé en argument(numero de colonne)
    des 12 dernières lignes ajoutées au fichier (donc 2 minutes).
    Si deux chaines de caractères ont le même nombre d'occurence, on prend la dernière qui a été rencontrée
    """

    #Nombre d'occurence ce chaque chaine de caractère
    #On crée un dictionnaire pour garder le compte de chaque valeur rencontrée
    dictionnaire = {}

    for ligne in range(12):
      #Passe la ligne si elle n'est pas valide
      if not ligne_est_valide(ligne):
        continue

      valeur = tableau[ligne][num_colonne]
      #Si la valeur n'est pas encore dans le dictionnaire, on l'ajoute
      if valeur not in dictionnaire.keys():
        dictionnaire[valeur] = {
          "compteur" : 0,
          "premiere occurrence" : ligne
        }
          
      #Ensuite on ajoute 1 au compteur de cette valeur dans tous les cas
      dictionnaire[valeur]["compteur"] += 1

    #On cherche le nombre d'occurrence le plus grand
    maximums = {}
    valeur_maximum = -float("inf")

    for cle, valeur in dictionnaire.items():
      #Si on a la meme valeur, on l'ajoute au dictionnaire maximums
      if valeur["compteur"] == valeur_maximum:
        maximums[cle] = valeur["premiere occurrence"]

      #Si c'est un nouveau maximum, on crée le dictionnaire avec seulement cette valeur
      elif valeur["compteur"] > valeur_maximum:
        valeur_maximum = valeur["compteur"]
        maximums = {cle : valeur["premiere occurrence"]}

    #On cherche la premiere occurrence la plus petite parmis les chaines de caractères qui ont le plus grand nombre d'occurence
    valeur_premiere_occurrence_min = float("inf")
    cle_premiere_occurrence_min = None

    for cle, valeur in maximums.items():
      if valeur < valeur_premiere_occurrence_min:
        cle_premiere_occurrence_min = cle
        valeur_premiere_occurrence_min = valeur

    return cle_premiere_occurrence_min

  #On ajoute à un tableau les valeurs que l'on va mettre dans notre ligne dans le fichier csv_serveur
  tableau_sortie = []
  for descripteur in descripteurs_csv_serveur:
    type = descripteur["type"]
    numero_colonne = descripteur["numero_colonne"]

    if type == "dernier":
        ligne = get_derniere_valeur(numero_colonne)
    elif type == "valeur":
        ligne = get_moyenne_colonne(numero_colonne)
    elif type == "condition":
        ligne = get_valeur_majoritaire_colonne(numero_colonne)
    else:
        raise ValueError("Type de descripteur inconnu")
        
    tableau_sortie.append(ligne)

  return tableau_sortie

def lancer():
  """
  Fonction principale de routine_convertir_donnes_serveur. Ajoute une ligne représentant la moyenne des deux dernières
  minutes des valeurs du capteur au fichier csv_serveur. Ne fait rien s'il n'y a pas assez de ligne dans le fichier d'entrée
  pour fonctionner correctement.
  """

  #Securite
  #S'il n'y a pas assez de lignes, on arrete tout (12 + 1 de descripteurs)
  if nombre_lignes(nom_fichier_capteur) < 13:
    print("Routine : valeurs d'entrées insuffisantes")
    ecrire_erreur("Routine : valeurs d'entrées insuffisantes")
    return

  #On ouvre les fichiers
  fichier_entree = open(nom_fichier_capteur, "r")
  fichier_sortie = open(nom_fichier_csv_serveur, "a")

  #On écrit dedans
  fichier_sortie.write(",".join(moyenne_2mins(fichier_entree)))
  fichier_sortie.write("\n")

  #On ferme les fichiers
  fichier_entree.close()
  fichier_sortie.close()
