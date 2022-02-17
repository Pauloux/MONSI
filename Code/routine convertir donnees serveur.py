descripteurs = ["Date", "Time", "Cloud Condition", "Cloud Value", "Rain Condition","Rain Value", "Ambient Temperature", "Wind Condition", "Wind Value","Switch Status"]
#Si on a égalités dans les "Calm" etc, on choisis le dernier qui est apparu

#Vérifier si les fichiers d'entrées sont présents

def get_2derniere_mins(fichier):
  """
  Renvoie un tableau de tableaux les sous-tableaux les lignes de fichier passé en argument. Cela prend les deux dernières minutes.
  """
  tableau = fichier.readlines()[-21:-1]
  nouveau_tableau = []
  for i in range(len(tableau)):
    ligne = tableau[i][1:-3].split('","')
    nouveau_tableau.append(ligne)
  return nouveau_tableau


def moyenne_2mins(fichier):
  """
  Renvoie un tableau avec la moyenne des deux dernieres minutes des colonnes que l'on a choisis (numero de colonne en argument)
  """
  #On récupère le tableau des valeurs des deux dernières minutes
  tableau = get_2derniere_mins(fichier)


  def ligne_est_valide(ligne):
    #La ligne est valide si elle ne commence pas par "Date", ce qui signifierais que c'est une ligne de descripteurs et si elle a bien 19 éléments
    return tableau[ligne][0]!="Date" and len(tableau[ligne]) == 19


  def get_derniere_valeur(num_colonne):
    """
    Renvoie la valeur que l'on a choisis (numero de colonne en argument) de la dernière ligne ajoutée au fichier
    """
    return tableau[-1][num_colonne]

  def get_moyenne_colonne(num_colonne):
    """
    Renvoie la moyenne des valeurs des deux dernières minutes de la colonne que l'on a passé en argument
    """
    somme = 0
    #Pour les 12 prochaines lignes (2 minutes)
    for ligne in range(12):
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
    Renvoie la valeur majoritaire des deux dernieres minutes de la colonne que l'on a passé en argument
    """
    #On crée un dictionnaire pour garder le compte de chaque valeur rencontrée
    dictionnaire = {}
    #Pour les 12 prochaines lignes (2 minutes)
    for ligne in range(12):
      if not ligne_est_valide(ligne):
        continue
      valeur = tableau[ligne][num_colonne]
      #Si la valeur n'est pas encore dans le dictionnaire, on l'ajoute
      if valeur not in dictionnaire.keys():
        dictionnaire[valeur] = 0
      #Ensuite on ajoute 1 au compteur de cette valeur
      dictionnaire[valeur] += 1
    
    #Maximum du dictionnaire
    cle_maximum = ""
    #On prend - infini au début comme maximum
    valeur_maximum = -float("inf")
    for cle, valeur in dictionnaire.items():
      if valeur > valeur_maximum:
        valeur_maximum = valeur
        cle_maximum = cle
    return cle_maximum

  def valeur_status():
    """
    Renvoie Closed si la valeur du capteur est Closed au moins une fois dans les deux dernières minutes. Renvoie Opened sinon
    """
    reponse = "Opened"
    for ligne in range(12):
      if not ligne_est_valide(ligne):
        continue
      valeur = tableau[ligne][13]
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
  #Créer un fichier csv avec la liste des descripteur si le fichier n'existe pas
  try:
    fichier_sortie = open("csv_serveur.csv", "r")
    fichier_sortie.close()
  except IOError as message_erreur:
    fichier_sortie = open("csv_serveur.csv", "a")
    fichier_sortie.write(",".join(descripteurs))
    fichier_sortie.close()

  #On ouvre les fichiers
  fichier_entree = open("Simulateur_donnees.csv", "r")

  fichier_sortie = open("csv_serveur.csv", "a")

  #Securite
  nombre_lignes = len(fichier_entree.readlines())
  fichier_entree.seek(0, 0)
  if nombre_lignes < 20:
    fichier_entree.close()
    fichier_sortie.close()
    return

  #On écrit dedans
  fichier_sortie.write("\n")
  fichier_sortie.write(",".join(moyenne_2mins(fichier_entree)))

  #On ferme les fichiers
  fichier_entree.close()
  fichier_sortie.close()
