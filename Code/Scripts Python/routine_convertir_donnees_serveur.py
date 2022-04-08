from fonctions_communes_et_parametres import *

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

  tableau_sortie = []
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

  tableau_sortie = []
  #Ajoute les colonnes utiles
  #Date
  tableau_sortie.append(get_derniere_valeur(0))
  #Heure
  tableau_sortie.append(get_derniere_valeur(1))
  #Wind Value
  tableau_sortie.append(get_moyenne_colonne(18))
  #Wind Condition
  tableau_sortie.append(valeur_majoritaire_colonne(17))
  #Cloud Value
  tableau_sortie.append(get_moyenne_colonne(5))
  #Cloud condition
  tableau_sortie.append(valeur_majoritaire_colonne(2))
  #Ambient Temperature
  tableau_sortie.append(get_moyenne_colonne(9))
  #Rain Value
  tableau_sortie.append(get_moyenne_colonne(7))
  #Rain Condition
  tableau_sortie.append(valeur_majoritaire_colonne(3))

  return tableau_sortie

def lancer():
  """
  Ouvre les fichiers, écrit dedans et les referme
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
  fichier_sortie.write("\n")
  fichier_sortie.write(",".join(moyenne_2mins(fichier_entree)))

  #On ferme les fichiers
  fichier_entree.close()
  fichier_sortie.close()
