import time

nom_fichier_logs = "../Documents/logs.txt"
nom_fichier_erreurs = "../Documents/erreurs.txt"
nom_fichier_entree = "../Documents/Simulateur_donnees.csv"
nom_fichier_sortie = "../Documents/csv_serveur.csv"
#Liste des descripteurs que l'on récupère
descripteurs = ["Date", "Time", "Cloud Condition", "Cloud Value", "Rain Condition","Rain Value", "Ambient Temperature", "Wind Condition", "Wind Value","Switch Status"]

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

def get_2derniere_mins(fichier):
  """
  Renvoie un tableau de tableaux les sous-tableaux les lignes de fichier passé en argument. Cela prend les deux dernières minutes.
  """
  tableau = fichier.readlines()[-13:-1]
  nouveau_tableau = []
  for i in range(len(tableau)):
    if len(tableau[i]) < 5 :
      continue
    ligne = tableau[i][1:-3].split('","')
    nouveau_tableau.append(ligne)
  #Securité
  while len(nouveau_tableau) < 12:
    nouveau_tableau.append("Fausse ligne")
    ecrire_logs("Fausse ligne ajoutée")
    ecrire_erreur("Fausse ligne ajoutée")
  return nouveau_tableau

def moyenne_2mins(fichier):
  """
  Renvoie un tableau avec la moyenne des valeurs des deux dernieres minutes
  """
  #On récupère le tableau des valeurs des deux dernières minutes
  tableau = get_2derniere_mins(fichier)

  def ligne_est_valide(ligne):
    """
    Renvoie un booléen, True si la ligne est valide (elle ne commence pas par "date" et il y a bien 19 éléments), renvoie False sinon
    """
    return tableau[ligne][0]!="Date" and len(tableau[ligne]) == 19


  def get_derniere_valeur(num_colonne):
    """
    Renvoie la valeur de la colonne que l'on a passé en argument(numero de colonne) de la dernière ligne ajoutée au fichier
    """
    indice = -1
    while not ligne_est_valide(indice):
      indice -= 1
    return tableau[indice][num_colonne]

  def get_moyenne_colonne(num_colonne):
    """
    Renvoie la moyenne des valeurs de la colonne que l'on a passé en argument(numero de colonne) des 12 denières lignes ajoutées au fichier (2 minutes)
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

  def valeur_majoritaire_colonne(num_colonne):
    """
    Renvoie la valeur majoritaire des valeurs de la colonne que l'on a passé en argument(numero de colonne) des 12 denières lignes ajoutées au fichier (2 minutes)
    """
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


    #On cherche la premiere occurrence la plus petite
    valeur_premiere_occurrence_min = float("inf")
    cle_premiere_occurrence_min = None

    for cle, valeur in maximums.items():
      if valeur < valeur_premiere_occurrence_min:
        cle_premiere_occurrence_min = cle
        valeur_premiere_occurrence_min = valeur

    return cle_premiere_occurrence_min

  def valeur_status():
    """
    Renvoie "Closed" si la valeur du capteur est "Closed" au moins une fois durant les deux dernières minutes. Renvoie "Opened" sinon
    """
    reponse = "Opened"
    for ligne in range(12):
      #Passe la ligne si elle n'est pas valide
      if not ligne_est_valide(ligne):
        continue
      valeur = tableau[ligne][13]
      #Dès qu'on l'a trouvé une fois, on peut arreter de chercher
      if valeur == "Closed":
        reponse = "Closed"
        break
    return reponse

  tableau_sortie = []
  #Ajoute les colonnes utiles
  #Date
  tableau_sortie.append(get_derniere_valeur(0))
  #Heure
  tableau_sortie.append(get_derniere_valeur(1))
  #Cloud condition
  tableau_sortie.append(valeur_majoritaire_colonne(2))
  #Cloud Value
  tableau_sortie.append(get_moyenne_colonne(5))
  #Rain Condition
  tableau_sortie.append(valeur_majoritaire_colonne(3))
  #Rain Value
  tableau_sortie.append(get_moyenne_colonne(7))
  #Ambient Temperature
  tableau_sortie.append(get_moyenne_colonne(9))
  #Wind Condition
  tableau_sortie.append(valeur_majoritaire_colonne(17))
  #Wind Value
  tableau_sortie.append(get_moyenne_colonne(18))
  #Switch Status
  tableau_sortie.append(valeur_status())

  return tableau_sortie

def lancer():
  """
  Ouvre les fichiers, écrit dedans et les referme
  """
  #Créer un fichier csv avec la liste des descripteur si le fichier n'existe pas
  if not fichier_existe(nom_fichier_sortie):
    print("Routine : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
    ecrire_logs("Routine : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
    ecrire_erreur("Routine : Fichier de sortie inexistant, création de " + nom_fichier_sortie)
    fichier_sortie = open(nom_fichier_sortie, "a")
    fichier_sortie.write(",".join(descripteurs))
    fichier_sortie.close()

  #Vérifie si le fichier d'entrée existe
  if not fichier_existe(nom_fichier_entree):
    print("Routine : Fichier d'entrée inexistant, arrêt de la routine")
    ecrire_logs("Routine : Fichier d'entrée inexistant, arrêt de la routine")
    ecrire_erreur("Routine : Fichier d'entrée inexistant, arrêt de la routine")
    return None

  #On ouvre les fichiers
  fichier_entree = open(nom_fichier_entree, "r")
  fichier_sortie = open(nom_fichier_sortie, "a")

  #Securite
  #Compte le nombre de ligne
  nombre_lignes = len(fichier_entree.readlines())
  #Replace le curseur au début du fichier pour pouvoir le lire
  fichier_entree.seek(0, 0)
  #S'il n'y a pas assez de lignes, on arrete tout (12 + 1 de descripteurs)
  if nombre_lignes < 13:
    print("Routine : valeurs d'entrées insuffisantes (" + str(nombre_lignes) + " lignes)")
    fichier_entree.close()
    fichier_sortie.close()
    return

  #On écrit dedans
  fichier_sortie.write("\n")
  fichier_sortie.write(",".join(moyenne_2mins(fichier_entree)))
  print("Routine : Données écrites dans " + nom_fichier_sortie)
  ecrire_logs("Routine : Données écrites dans " + nom_fichier_sortie)

  #On ferme les fichiers
  fichier_entree.close()
  fichier_sortie.close()
