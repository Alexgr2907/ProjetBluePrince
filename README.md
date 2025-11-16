Ceci est un projet de jeu vidéo de type roguelite-puzzle réalisé dans le cadre d'un projet universitaire en Programmation Orientée Objet. C'est une implémentation simplifiée du jeu "Blue Prince", développée en Python à l'aide de la bibliothèque Pygame.

Le joueur explore un manoir hanté, gère ses ressources (pas, clés, gemmes...) et tente de construire un chemin jusqu'à la salle de sortie.

Prérequis : 
Python 3.10 (ou plus récent)
Pygame
Installation
Clonez ce dépôt sur votre machine locale :
git clone [https://github.com/Alexgr2907/ProjetBluePrince.git]
cd ProjetBluePrince

Créez et activez un environnement virtuel
Sur Windows : 
python -m venv .venv
.venv\Scripts\activate

Sur macOS/Linux :
python3 -m venv .venv
source .venv/bin/activate
 
Puis : pip install -r requirements.txt

Pour démarrer le jeu, exécutez le fichier main.py :
python main.py

Les commandes au clavier :  
ZQSD :"Sélectionner une direction (Haut, Gauche, Bas, Droite)."
ENTRÉE / ESPACE : Valider le déplacement ou l'ouverture de la porte sélectionnée.
ECHAP : Quitter le jeu 
C : "Creuser à l'emplacement actuel (si vous avez une ""Pelle"" et que la salle le permet)."

Sélection de salle : 

FLÈCHE HAUT : Sélectionner la salle du dessus.
FLÈCHE BAS : Sélectionner la salle du dessous.
ENTRÉE : Confirmer le choix de la salle.
X : Relancer le tirage des 3 salles (coûte 1 Dé)
ECHAP : Annuler la sélection et refermer la porte.

Inventaire : 

I : Ouvrir ou fermer le menu de l'inventaire.
Q / D : Changer d'onglet (Consommables, Permanents, Autres).
Z / S : Naviguer dans la liste d'objets de l'onglet actif.
ENTRÉE : Sélectionner un objet pour ouvrir le menu contextuel.
Dans le menu contextuel ("Utiliser", "Infos", "Retour") :
Z / S : Naviguer dans les options.
ENTRÉE : "Valider l'option (ex: ""Utiliser"")."
ECHAP : Revenir en arrière.

Magasins et Pop-ups : 
Q / S / D : Acheter l'objet correspondant dans un magasin.
O / N "Confirmer ou annuler l'ouverture d'une porte verrouillée."
ENTRÉE : Quitter l'interface du magasin.    