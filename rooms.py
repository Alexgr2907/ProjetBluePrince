from abc import ABC, abstractmethod
import random as r
import pygame
import objet
import inventaire

# dans ce fichier python ai défini toute les classes des pièces dans le jeu
# les nom des classes, variables etc.. seront en anglais (pour une compréhension globale sur github)
# les docstrings en revanche seront en français pour faciliter la compréhension des codes 


# je l'utilise pour les classe pumpkin et Closet
proba_objets = {
    # Ici 1 représente une rareté de 3 (légendaire) et 10 une rareté de 0 (commun), plus le poids est élevé plus l'objets a de chance d'être pioché
    # Nourriture 
    objet.Pomme : 10, 
    objet.Banane : 9, 
    objet.Gateau : 7, 
    objet.Sandwich : 5, 
    objet.Repas : 3,

    # Permanent
    objet.DetecteurMetaux :1,
    objet.KitCrochetage :1,
    objet.Marteau :1,
    objet.PatteLapin:1,
    objet.Pelle :1
}


class Room(ABC):
    """
    Classe de base abstraite pour toutes les pièces du manoir.
    """
    def __init__(self, name, rarity, gem_cost, color, image_path=None ):
        self.name = name # Nom, ex: "Entrance Hall"
        self.rarity = rarity # Entier de 0 à 3 
        self.gem_cost = gem_cost # Coût en gemmes 
        self.color = color # "blue", "green", etc. 
        # Portes "modèles" (indique ou il y a une porte)
        self.door_location = {'north': False, 'south': False, 'east': False, 'west': False}
        self.objects_in_room = [] # Objets qui seront dans la pièce
        self.dig_spot = False # Endroit à creuser
        self.First_time = True # Drapeau 1er entrée


        # Statut des portes (-1 pas de porte, 0 pour ouverte, 1 une clé ou kit crochetage,2 que une clé)
        # sera utilisé par Dimitri pour dire si les portes sont vérouillé où non (logique de clés)
        # ex: {'north': 0, 'south': 1, 'east': -1 (pas de porte), 'west': 2}
        self.doors_statut = {} 

        #  nous dit si le joueur est déjà entré DANS CETTE instance
        # logique d'effet d'entrée 
        self.First_time = True

        # 0 = 0° (Original), 1 = 90° anti-horaire, 2 = 180°, 3 = 270° anti-horaire
        self.rotation = 0 
        
        # Stockera les rotations valides (ex: [0, 2]) lors du tirage
        self.valid_rotations = []

        self.image = None
        # Je laisse ce if le temps de bien configurer tout les salles pour éviter les erreurs
        if image_path:
            try:
                # Charge l'image et la convertit pour des performances optimales
                # Garde-la en taille originale pour l'instant
                self.image = pygame.image.load(image_path).convert_alpha() 
            except pygame.error as e:
                print(f"Erreur de chargement d'image pour {name}: {e}")
                self.image = None # S'assure que self.image est None si ça échoue

    @abstractmethod
    def set_doors(self):
        """Méthode abstraite pour définir les portes de la pièce modèle."""
        pass

    def get_rotated_doors(self):
        """
        Retourne le dictionnaire des portes (le "plan") en tenant 
        compte de la rotation actuelle de la pièce.
        """
        doors = self.door_location # Le 'plan' original
        
        # Rotation 0: 0° (Identique)
        if self.rotation == 0:
            return doors
        
        # Rotation 1: 90° anti-horaire
        elif self.rotation == 1: 
            return {
                'north': doors['east'], 
                'south': doors['west'], 
                'east': doors['south'], 
                'west': doors['north']
            }
        
        # Rotation 2: 180°
        elif self.rotation == 2: 
            return {
                'north': doors['south'], 
                'south': doors['north'], 
                'east': doors['west'], 
                'west': doors['east']
            }
        
        # Rotation 3: 270° anti-horaire
        elif self.rotation == 3: 
            return {
                'north': doors['west'], 
                'south': doors['east'], 
                'east': doors['north'], 
                'west': doors['south']
            }
        
        return doors # Sécurité
    
    # Le player servira à verifier l'inventaire du joueur pour dans certain cas
    # ajouter des effets en fonction de l'objet
    # Sert à ajouter des objets dans la salle

    def add_objects(self, player):
        """
        Ajoute des objets aléatoires à la pièce lors de sa création.
        C'est ici que tu gères "Aléatoire dans les objets disponibles dans les pièces".
        """
        # Par défaut, une pièce ne contient rien 
        self.objects_in_room = []
        
        # Exemple pour une pièce spécifique (à surcharger dans les sous-classes)
        # if self.name == "Den":
        #    self.objects_in_room.append(Gem(1)) 
        #    # Gérer la probabilité de trouver un coffre 
        #    # Tu devras vérifier si le joueur a la Patte de Lapin 
        #    probability = 0.3 
        #    if player.has_item("Lucky Rabbit's Foot"):
        #        probability += 0.1 # Augmenter la chance
        #    
        #    if random.random() < probability:
        #        self.objects_in_room.append(Chest())

    #Sert à appliquer un effet à la première entrée dans la salle
    def apply_entry_effect(self, player, grid):
        """
        Applique un effet spécial la première fois que le joueur entre.
        Par défaut, la plupart des pièces n'ont pas d'effet.
        """
        None

    # Sert à appliquer un effet à chaque entrée dans la salle
    def apply_every_entry_effect(self, player, grid):
        """Applique un effet *à chaque fois* que le joueur entre."""
        if self.dig_spot:
            return "Vous remarquez un endroit dans la pièce qui semble parfait pour creuser (Touche C)!"
        return None


    def generation_objet(self, taux_drop : float = 0.5):
        """
        Tente de génerer un objet aléatoire
        """
        pass # génération dans room_manager

class Midas_vault(Room):
    def __init__(self):
        # Appelle le constructeur de la classe mère (Room)
        super().__init__(name="Vault", rarity=2, gem_cost=3, color="blue", image_path="NouvelleSalleThèmeHorreur/Midas_Vault_Icon.webp")
        self.set_doors()

    def set_doors(self):
        # La "Vault" n'a qu'une seule porte 
        # On suppose que c'est la porte Sud (celle par laquelle on entre)
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            nb_pieces = 50 # Ajoute 50 pièces au joueur
            if player and player.detecteur_métaux :
                if r.random() > 0.5 :
                    nb_pieces += 4

            player.pieces += nb_pieces
            self.First_time = False
            return f"Jackpot, vous trouvez {nb_pieces} pièces d'or."
        return None 


class Gallery(Room):
    def __init__(self):
        super().__init__(name="Gallery", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Gallery_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': False, 'west': False}

    
class Dracula_tomb(Room):
    def __init__(self):
        super().__init__(name="Dracula's Tomb", rarity=1, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Dracula_Tomb_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            player.gemmes += 4 # Ajoute 4 gemmes
            self.First_time = False
            return "Vous trouvez 4 gemmes dans la tombe de Dracula"
        return None
        

class Garage(Room):
    def __init__(self):
        super().__init__(name="Garage", rarity=1, gem_cost=1, color="blue", image_path="NouvelleSalleThèmeHorreur/Garage_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': False}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            nb_cles = 2
            if player and player.detecteur_métaux :
                if r.random() > 0.5 :
                    nb_cles += 1

            player.cles += nb_cles
            self.First_time = False
            return f"Vous trouvez {nb_cles} clé(s) caché(es) dans la boite à gant !"
        return None 


class Horror_Hall(Room):
    def __init__(self):
        super().__init__(name="Horror Hall", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Horror_Hall_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}

class Exit(Room):
    def __init__(self):
        super().__init__(name="Exit", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Exit_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}


class Joker_Office(Room):
    def __init__(self):
        super().__init__(name="Joker's Office", rarity=1, gem_cost=0, color="Red", image_path="NouvelleSalleThèmeHorreur/Joker_Office_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            val = r.randint(0,1)
            if val == 0:
                player.pas += 10 

                self.First_time = False 
                return " La chance vous sourit! Vous gagnez 10 pas." 
            elif val == 1:
                if player.pas >= 10:
                    player.pas -= 10
                else:
                    player.pas = 0

                self.First_time = False 
                return " Pas de chance! Vous perdez 10 pas" 
            

        return None # Ne fait rien les fois suivantes


class Locksmith(Room):
    def __init__(self):
        super().__init__(name="Locksmith", rarity=1, gem_cost=1, color="yellow", image_path="NouvelleSalleThèmeHorreur/Locksmith_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player, grid):
        # Renvoie le signal à la première entrée
        if self.First_time:
            self.First_time = False
            return "open_shop_locksmith"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        if self.First_time == False:
        # Cette fonction est appelée à chaque entrée.
        # Elle retourne un signal à affichage.py pour ouvrir le menu.
            return "open_shop_locksmith"
        return None


class Maze(Room):

    def __init__(self):
        super().__init__(name="Maze", rarity=1, gem_cost=0, color="Orange", image_path="NouvelleSalleThèmeHorreur/Maze_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}
    """
    def add_objects(self, player):
        pass

    def exit():
        val = r.randint(0,3)
        if val == 0:
            #next_room = south
        elif val == 1:
            #next_room = west
        elif val == 2:
            #next_room = north
        elif val == 3:
            #next_room = east
        return next_room
    """
    
class Bedroom(Room):
    def __init__(self):
        super().__init__(name="Bedroom", rarity=0, gem_cost=0, color="purple", image_path="NouvelleSalleThèmeHorreur/Bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            player.pas += 2 
            self.First_time = False
            return "Vous vous reposez un instant. Vous gagnez 2 pas"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        
        player.pas += 2
        return "Vous vous reposez un instant. Vous gagnez 2 pas"

class Closet(Room):
    def __init__(self):
        super().__init__(name="Closet", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Closet_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            self.First_time = False

            # Prépare les listes pour le tirage pondéré depuis le dict
            classes_possibles = list(proba_objets.keys())
            poids = list(proba_objets.values())
            items_found_names = []
            
            # Boucle pour donner 2 objets
            for _ in range(2):
                # Tire UNE classe d'objet en respectant les poids
                # r.choices renvoie une liste, on prend le premier élément [0]
                choix_classe = r.choices(classes_possibles, weights=poids, k=1)[0]
                
                # Crée une instance de cet objet (ex: objet.Pomme())
                item_instance = choix_classe() 

                # Gère l'ajout à l'inventaire en fonction du type
                if isinstance(item_instance, objet.Permanent):
                    # La méthode 'utiliser' des objets permanents les active
                    # (ex: player.pelle = True)
                    item_instance.utiliser(player)
                    items_found_names.append(item_instance.nom)
                    
                elif isinstance(item_instance, objet.Nourriture):
                    # La nourriture est ajoutée au dictionnaire 'objets'
                    nom = item_instance.nom
                    if nom in player.objets:
                        player.objets[nom] += 1
                    else:
                        player.objets[nom] = 1
                    items_found_names.append(nom)

            # Retourner le message de feedback
            if items_found_names:
                return f"Vous trouvez : {', '.join(items_found_names)} !"
            else:
                return "Le placard est vide..." # Si jamais le tirage échoue

        return None 
    
class Courtyard(Room):
    def __init__(self):
        super().__init__(name="Courtyard", rarity=1, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Courtyard_Icon.webp")
        self.set_doors()
        self.dig_spot = True

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    """
    def add_objects(self, player):
        #  self.objects_in_room.append(Digspot(1))
        # self.permanent_object.append(Shovel)
    """
        
        
class Corridor(Room):
    def __init__(self):
        super().__init__(name="Corridor", rarity=1, gem_cost=0, color="orange", image_path="NouvelleSalleThèmeHorreur/Corridor_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': False, 'west': False}
    """
    def apply_entry_effect(self, player):
        # porte toujours ouverte
        self.doors_statut = {'north': 0, 'south': 0, 'east': -1 , 'west': -1}
        pass 
    """

class Pantry(Room):
    def __init__(self):
        super().__init__(name="Pantry", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Pantry_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            nb_pieces = 4   # Ajoute 4 pièces
            if player and player.detecteur_métaux :
                if r.random() > 0.5 :
                    nb_pieces += 4

            player.pieces += nb_pieces
            self.First_time = False
            return f"Vous trouvez {nb_pieces} pièces d'or."
        return None        


class Thief_Storage(Room):
    def __init__(self):
        super().__init__(name="Thief's Storage", rarity=2, gem_cost=0, color="red", image_path="NouvelleSalleThèmeHorreur/Thief_Storage_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    """
    def apply_entry_effect(self, player):
        # Fais disparaitre l'entiereté d'un type d'objet ( toute les clés ou toutes les pièces ou tout les gemmes ...)
        pass 
    """


class Billiard_Room(Room):
    def __init__(self):
        super().__init__(name="Billiard Room", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Billard_Room_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}


class Devil_Church(Room):
    def __init__(self):
        super().__init__(name="Devil's Church", rarity=2, gem_cost=0, color="red", image_path="NouvelleSalleThèmeHorreur/Devil_Church_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            if not player.pieces == 0:
                player.pieces -= 1
            self.First_time = False
            return "Les adeptes du diables vous obligent à faire un don. Vous perdez 1 pièces"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        if not player.pieces == 0 :
            player.pieces -= 1
        return "Les adeptes du diables vous obligent à faire un don. Vous perdez 1 pièces"
        


class Haunted_Gym(Room):
    def __init__(self):
        super().__init__(name="Haunted Gym", rarity=1, gem_cost=0, color="red", image_path="NouvelleSalleThèmeHorreur/Haunted_Gym_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            player.pas -= 2
            self.First_time = False
            return "Un basket avec des fantomes ? mauvaise idée. Vous perdez 2 pas"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        player.pas -= 2
        return "Un basket avec des fantomes ? mauvaise idée. Vous perdez 2 pas"
        return None
        


class Loot_Stash(Room):
    def __init__(self):
        super().__init__(name="Loot Stash", rarity=1, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Loot_Stash_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            nb_pieces = 1
            nb_cles = 1
            nb_gemmes = 1
            
            if player and player.detecteur_métaux :
                if r.random() > 0.5 :
                    nb_pieces += 1
                    nb_cles += 1

            player.pieces += nb_pieces
            player.cles += nb_cles
            player.gemmes += nb_gemmes
            self.First_time = False
            return f"En fouyant dans ce bordel, vous trouvez {nb_cles} clé(s), {nb_gemmes} gemme et {nb_pieces} pièce(s)."
        return None        




class Master_Bedroom(Room):
    def __init__(self):
        super().__init__(name="Master Bedroom", rarity=2, gem_cost=1, color="purple", image_path="NouvelleSalleThèmeHorreur/Master_Bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player, grid):

        if self.First_time:
            salles_ouverte = 0
            for salles in grid:
                for salle in salles:
                    if salle is not None:
                        salles_ouverte += 1

            # On enlève 1 pour la salle master bedroom qui vient d'être ouverte
            if salles_ouverte != 0:
                salles_ouverte -= 1

            if salles_ouverte > 0:
                player.pas += salles_ouverte
                self.First_time = False
                return f"Vous gagnez {salles_ouverte} pas (1 par salle découverte)!"
        return None 


class Passageway(Room):
    def __init__(self):
        super().__init__(name="Passageway", rarity=1, gem_cost=1, color="orange", image_path="NouvelleSalleThèmeHorreur/Passageway_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}


class Patio(Room):
    def __init__(self):
        super().__init__(name="Patio", rarity=2, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Patio_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}

    def apply_entry_effect(self, player, grid):
        
        if self.First_time:
            salles_ouverte = 0
            for salles in grid:
                for salle in salles:
                    if salle is not None and salle.color == "green":
                        salles_ouverte += 1

            # On enlève 1 pour la salle patio qui vient d'être ouverte
            if salles_ouverte != 0 :
                salles_ouverte -= 1

            if salles_ouverte > 0:
                player.gemmes += salles_ouverte
                self.First_time = False
                return f"Vous gagnez {salles_ouverte} gemmes (1 par salle verte découverte)!"
        return None 

class Pawn_Shop(Room):
    def __init__(self):
        super().__init__(name="Pawn Shop", rarity=2, gem_cost=1, color="yellow", image_path="NouvelleSalleThèmeHorreur/Pawn_Shop_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}

    def apply_entry_effect(self, player, grid):
        # Renvoie le signal à la première entrée
        if self.First_time:
            self.First_time = False
            return "open_shop_pawnshop"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        if self.First_time == False:
        # Cette fonction est appelée à chaque entrée.
        # Elle retourne un signal à affichage.py pour ouvrir le menu.
            return "open_shop_pawnshop"
        return None
    

class Pumpkin_Field(Room):
    def __init__(self):
        super().__init__(name="Pumpkin Field", rarity=1, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Pumpkin_Field_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            self.First_time = False

            # Prépare les listes pour le tirage pondéré depuis le dict
            classes_possibles = list(proba_objets.keys())
            poids = list(proba_objets.values())
            items_found_names = []
            
            # Boucle pour donner 2 objets
            for _ in range(2):
                # Tire UNE classe d'objet en respectant les poids
                # r.choices renvoie une liste, on prend le premier élément [0]
                choix_classe = r.choices(classes_possibles, weights=poids, k=1)[0]
                
                # Crée une instance de cet objet (ex: objet.Pomme())
                item_instance = choix_classe() 

                # Gère l'ajout à l'inventaire en fonction du type
                if isinstance(item_instance, objet.Permanent):
                    # La méthode 'utiliser' des objets permanents les active
                    # (ex: player.pelle = True)
                    item_instance.utiliser(player)
                    items_found_names.append(item_instance.nom)
                    
                elif isinstance(item_instance, objet.Nourriture):
                    # La nourriture est ajoutée au dictionnaire 'objets'
                    nom = item_instance.nom
                    if nom in player.objets:
                        player.objets[nom] += 1
                    else:
                        player.objets[nom] = 1
                    items_found_names.append(nom)

            # Retourner le message de feedback
            if items_found_names:
                return f"Vous trouvez : {', '.join(items_found_names)} !"
            else:
                return "Le placard est vide..." # Si jamais le tirage échoue

        return None 

class Statue_Hall(Room):
    def __init__(self):
        super().__init__(name="Statue Hall", rarity=1, gem_cost=0, color="orange", image_path="NouvelleSalleThèmeHorreur/Statue_Hall_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}

    def apply_entry_effect(self, player, grid):
        if self.First_time:
            nb_cles = 1
            if player and player.detecteur_métaux :
                if r.random() > 0.5 :
                    nb_cles += 1

            player.cles += nb_cles
            self.First_time = False
            return f"Vous trouvez {nb_cles} clé(s) caché(es) derrière une statue."
        return None

class Chucky_Bedroom(Room):
    def __init__(self):
        super().__init__(name="Chucky's Bedroom", rarity=2, gem_cost=0, color="purple", image_path="NouvelleSalleThèmeHorreur/Chucky_bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            player.pas += 10
            self.First_time = False
            return "Vous entrez dans la chambre de Chucky. En la voyant, vous vous enfuyez en courant! Vous gagnez 10 pas"
        return None





