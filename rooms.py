from abc import ABC, abstractmethod
import random as r
import pygame
import objet
import inventaire

# dans ce fichier python ai défini toute les classes des pièces dans le jeu
# les nom des classes, variables etc.. seront en anglais (pour une compréhension globale sur github)
# les docstrings en revanche seront en français pour faciliter la compréhension des codes 

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
    def apply_entry_effect(self, player):
        """
        Applique un effet spécial la première fois que le joueur entre.
        Par défaut, la plupart des pièces n'ont pas d'effet.
        """
        None

    # Sert à appliquer un effet à chaque entrée dans la salle
    def apply_every_entry_effect(self, player):
        """Applique un effet *à chaque fois* que le joueur entre."""
        None


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

    def apply_entry_effect(self, player):
        if self.First_time:
            player.pieces += 50 # Ajoute 50 pièces au joueur
            self.First_time = False # Baisse le drapeau
            # Retourne un message pour l'afficher à l'écran
            return "Jackpot, vous trouvez 50 pièces d'or !" 
        return None # Ne fait rien les fois suivantes

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
    
    def apply_entry_effect(self, player):
        if self.First_time:
            player.gemmes += 4 # Ajoute 4 pièces
            self.First_time = False
            return "Vous trouvez 4 gemmes dans la tombe de Dracula"
        return None
        

class Garage(Room):
    def __init__(self):
        super().__init__(name="Garage", rarity=1, gem_cost=1, color="blue", image_path="NouvelleSalleThèmeHorreur/Garage_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': False}
    
    def apply_entry_effect(self, player):
        if self.First_time:
            player.cles += 2 
            self.First_time = False 
            return "Vous trouvez 2 clés dans la boite à gant !" 
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
    
    def apply_entry_effect(self, player):
        if self.First_time:
            val = r.randint(0,1)
            if val == 0:
                player.pieces += 10 

                self.First_time = False 
                return " La chance vous sourit! Vous gagnez 10 pièces." 
            elif val == 1:
                if player.pieces >= 10:
                    player.pieces -= 10
                else:
                    player.pieces = 0

                self.First_time = False 
                return " Pas de chance! Vous perdez 10 pièces" 
            

        return None # Ne fait rien les fois suivantes


class Locksmith(Room):
    def __init__(self):
        super().__init__(name="Locksmith", rarity=1, gem_cost=1, color="yellow", image_path="NouvelleSalleThèmeHorreur/Locksmith_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}
    """
    def add_objects(self, player):
        # Voir dans player combien de pièce sont présente et 
        price = int(input("Choose 1 key for 5 coins, 3 keys for 12 coins or lock picking kit for 15 coins"))
        if price == 5:
            # self.objects_in_room.append(Gold(-5))
            # self.objects_in_room.append(Key(1))  
        elif price == 12:
            # self.objects_in_room.append(Gold(-12))
            # self.objects_in_room.append(Key(3))  
        elif price == 15:
            # self.objects_in_room.append(Gold(-15))
            # self.objects_in_room.append(Lock_picking_kit)  
        else:
            pass
        pass
    """


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
    
    def apply_entry_effect(self, player):
        if self.First_time:
            player.pas += 2 # Ajoute 4 pièces
            self.First_time = False
            return "Vous vous reposez un instant. Vous gagnez 2 pas"
        return None
    
    def apply_every_entry_effect(self, player):
        
        player.pas += 2
        return "Vous vous reposez un instant. Vous gagnez 2 pas"

class Closet(Room):
    def __init__(self):
        super().__init__(name="Closet", rarity=0, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Closet_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}
    """
    def add_objects(self, player):
        #  self.objects_in_room.append(Item(2))
        pass
    """

class Courtyard(Room):
    def __init__(self):
        super().__init__(name="Courtyard", rarity=1, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Courtyard_Icon.webp")
        self.set_doors()

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

    def apply_entry_effect(self, player):
        if self.First_time:
            player.pieces += 4 # Ajoute 4 pièces
            self.First_time = False
            return "Vous trouvez 4 pièces d'or."
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

    def apply_entry_effect(self, player):
        if self.First_time:
            player.pieces -= 1
            self.First_time = False
            return "Les adeptes du diables vous obligent à faire un don. Vous perdez 1 pièces"
        return None
    
    def apply_every_entry_effect(self, player):
        player.pieces -= 1
        return "Les adeptes du diables vous obligent à faire un don. Vous perdez 1 pièces"
        


class Haunted_Gym(Room):
    def __init__(self):
        super().__init__(name="Haunted Gym", rarity=1, gem_cost=0, color="red", image_path="NouvelleSalleThèmeHorreur/Haunted_Gym_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    
    def apply_entry_effect(self, player):
        if self.First_time:
            player.pieces -= 2
            self.First_time = False
            return "Un basket avec des fantomes ? mauvaise idée. Vous perdez 2 pas"
        return None
    
    def apply_every_entry_effect(self, player):
        player.pas -= 2
        return "Un basket avec des fantomes ? mauvaise idée. Vous perdez 2 pas"


class Loot_Stash(Room):
    def __init__(self):
        super().__init__(name="Loot Stash", rarity=1, gem_cost=0, color="blue", image_path="NouvelleSalleThèmeHorreur/Loot_Stash_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player):
        if self.First_time:
            player.cles += 1 
            player.gemmes += 1 
            player.pieces += 1 
            self.First_time = False 
            return "En fouyant dans ce bordel, vous trouvez 1 Clé, 1 gemme et 1 pièce " 
        return None 



class Master_Bedroom(Room):
    def __init__(self):
        super().__init__(name="Master Bedroom", rarity=2, gem_cost=1, color="purple", image_path="NouvelleSalleThèmeHorreur/Master_Bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}


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


class Pawn_Shop(Room):
    def __init__(self):
        super().__init__(name="Pawn Shop", rarity=2, gem_cost=1, color="yellow", image_path="NouvelleSalleThèmeHorreur/Pawn_Shop_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}


class Pumpkin_Field(Room):
    def __init__(self):
        super().__init__(name="Pumpkin Field", rarity=1, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Pumpkin_Field_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}


class Statue_Hall(Room):
    def __init__(self):
        super().__init__(name="Statue Hall", rarity=1, gem_cost=0, color="orange", image_path="NouvelleSalleThèmeHorreur/Statue_Hall_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': True, 'west': True}

    def apply_entry_effect(self, player):
        if self.First_time:
            player.cles += 1 # Ajoute 4 pièces
            self.First_time = False
            return "Vous trouvez 1 Clé caché derrière une statue."
        return None

class Chucky_Bedroom(Room):
    def __init__(self):
        super().__init__(name="Chucky's Bedroom", rarity=2, gem_cost=0, color="purple", image_path="NouvelleSalleThèmeHorreur/Chucky_bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}
    
    def apply_entry_effect(self, player):
        if self.First_time:
            player.pas += 10
            self.First_time = False
            return "Vous entrez dans la chambre de Chucky. En la voyant, vous vous enfuyez en courant! Vous gagnez 10 pas"
        return None


    
#---------- CATALOGUE DES OBJETS ----------#

proba_objets = {
    # Ici 1 représente une rareté de 3 (légendaire) et 10 une rareté de 0 (commun), plus le poids est élevé plus l'objets a de chance d'être pioché
    # Ressource
    objet.Pieces : 15,
    objet.Gemmes : 5,
    objet.Cles : 3,
    objet.Des : 8,

    # Nourriture 
    objet.Pomme : 12,
    objet.Banane : 10,
    objet.Gateau : 8,
    objet.Sandwich : 5,
    objet.Repas : 3,

    # Permanent
    objet.DetecteurMetaux :1,
    objet.KitCrochetage :1,
    objet.Marteau :1,
    objet.PatteLapin:1,
    objet.Pelle :1
}


