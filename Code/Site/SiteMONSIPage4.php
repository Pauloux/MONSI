<html>
  <head>
    <title>Projet MONSI</title>
    <link rel="stylesheet" href="style2.css">
  </head>
  <body>
    <h1 class="center text_color">Projet MONSI</h1>

    <header>
       <!--Boutons pour passer d'une page à l'autre -->
    <div id ="menu-centered">
      <ul>
        <li><a href="SiteMONSIPage1" title="Vent/Nuages">Vent/Nuage</a></li>
        <li><a href="SiteMONSIPage2" title="Temperature">Temperature</a></li>
        <li><a href="SiteMONSIPage3" title="Pluie">Pluie</a></li>
        <li><a href="" title="Caméra">Caméra</a></li>
      </ul>
      </div>
    </header>

    <!--Image-->
    <img src="" class="image">

    <!--Affichage des dernières alertes-->
    <div class="Dernieres_alertes">
      <h4 id="Titre_alertes">Alertes des 30 dernieres minutes :</h4>
      <ul>
        <?php
          $aucune_alerte = true;
          //On ouvre le document
          $handle = fopen("../Documents/alertes_historique.txt", "r");
          //Et on lit chaque ligne
          while (($ligne = fgets($handle)) !== false) {
            $aucune_alerte = false;
            //Convertit la chaine de caractère en tableau
            $ligne = str_split($ligne);
            $nouvelle_ligne = "";
            $recopier = false;
            #On enlève le premier mot car c'est le temps Unix
            for ($i = 1; $i < count($ligne); $i++){
              if ($ligne[$i] == " "){
                $recopier = true;
              }
              if ($recopier == true){
                $nouvelle_ligne = $nouvelle_ligne . $ligne[$i];
              }
            }
            //On enlève les espaces au début et la fin car cela pourrait gêner les comparaisons suivantes
            $nouvelle_ligne = trim($nouvelle_ligne);
            if ($nouvelle_ligne == "Vent_1") {
              $nouvelle_ligne = "Vent en zone jaune";
            }
            else if ($nouvelle_ligne == "Vent_2") {
              $nouvelle_ligne = "Vent en zone rouge";
            }
            else if ($nouvelle_ligne == "Nuage_1") {
              $nouvelle_ligne = "Nuage en zone jaune";
            }
            else if ($nouvelle_ligne == "Nuage_2") {
              $nouvelle_ligne = "Nuage en zone rouge";
            }
            else if ($nouvelle_ligne == "Pluie_1") {
              $nouvelle_ligne = "Pluie en zone jaune";
            }
            else if ($nouvelle_ligne == "Pluie_2") {
              $nouvelle_ligne = "Pluie en zone rouge";
            }
            else {
              $nouvelle_ligne = "Alerte inconnue";
            }
            //Et on ajoute l'alerte à la liste
            echo "<li>$nouvelle_ligne</li>";
          }
      //On referme le document quand on a fini
      fclose($handle);
      //S'il n'y a aucune alerte, on l'affiche
      if ($aucune_alerte == true) {
        echo "<li>Aucune alerte ces 30 dernières minutes</li>";
      }
      ?>
      </ul>
    </div>
      
    <?php
  //Gestion des alertes pop-up
  //On ouvre le document
  $handle = fopen("../Documents/alertes_site.txt", "r");
  //Et on lit chaque ligne
  while (($line = fgets($handle)) !== false) {
    //On enlève les espaces au début et la fin car cela pourrait gêner les comparaisons suivantes
    $line = trim($line);
    if($line == "Vent_1") {
      echo "<script>alert(\"Le vent passe en zone jaune !\")</script>";
    }
    else if($line == "Vent_2") {
      echo "<script>alert(\"Le vent passe en zone rouge !\")</script>";
    }
    else if($line == "Nuage_1") {
      echo "<script>alert(\"Les nuages passent en zone jaune !\")</script>";
    }
    else if($line == "Nuage_2") {
      echo "<script>alert(\"Les nuages passent en zone rouge !\")</script>";
    }
    else if($line == "Pluie_1") {
      echo "<script>alert(\"La pluie passe en zone jaune !\")</script>";
    }
    else if($line == "Pluie_2") {
      echo "<script>alert(\"La pluie passe en zone rouge !\")</script>";
    }
    else {
      echo "<script>alert(\"Alerte inconnue\")</script>";
    }
  }
  //On referme le document quand on a fini
  fclose($handle);
  //On actualise la page toutes les 120 secondes
  header("Refresh:120");
?>
  </body>
</html>
