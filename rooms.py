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
    # Ici les valeurs représente le poids d'un objet. Plus le poids est élevé plus l'objets a de chance d'être pioché
    # Consommable
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
        self.dig_spot = False # Endroit à creuser
        self.doors_statut = {} # Statut des portes
        self.First_time = True  # logique d'effet de 1er entrée
        self.rotation = 0 # rotation de la salle
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
        """Méthode abstraite pour définir les portes de la pièce ."""
        pass

    def get_rotated_doors(self):
        """
        Retourne le dictionnaire des portes (le "plan") en tenant 
        compte de la rotation actuelle de la pièce.
        """
        doors = self.door_location # Le 'plan' original
        
        # Rotation 0: 0 degrés 
        if self.rotation == 0:
            return doors
        
        # Rotation 1: 90 degrés anti-horaire
        elif self.rotation == 1: 
            return {
                'north': doors['east'], 
                'south': doors['west'], 
                'east': doors['south'], 
                'west': doors['north']
            }
        
        # Rotation 2: 180 degrés anti-horaire
        elif self.rotation == 2: 
            return {
                'north': doors['south'], 
                'south': doors['north'], 
                'east': doors['west'], 
                'west': doors['east']
            }
        
        # Rotation 3: 270 degrés anti-horaire
        elif self.rotation == 3: 
            return {
                'north': doors['west'], 
                'south': doors['east'], 
                'east': doors['north'], 
                'west': doors['south']
            }
        
        return doors 
    
    #Sert à appliquer un effet à la première entrée dans la salle
    def apply_entry_effect(self, player, grid):
        """
        Applique un effet spécial la première fois que le joueur entre.
        """
        return None

    # Sert à appliquer un effet à chaque entrée dans la salle
    def apply_every_entry_effect(self, player, grid):
        """
        Applique un effet à chaque fois que le joueur entre.
        """
        if self.dig_spot:
            return "Vous remarquez un endroit dans la pièce qui semble parfait pour creuser (Touche C)!"
        return None

      
class Midas_vault(Room):
    def __init__(self):
        super().__init__(name="Vault", rarity=2, gem_cost=3, color="blue", image_path="NouvelleSalleThèmeHorreur/Midas_Vault_Icon.webp")
        self.set_doors()

    def set_doors(self):
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
            
        return None 


class Locksmith(Room):
    def __init__(self):
        super().__init__(name="Locksmith", rarity=2, gem_cost=1, color="yellow", image_path="NouvelleSalleThèmeHorreur/Locksmith_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': False}

    def apply_entry_effect(self, player, grid):
        
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
    
class Bedroom(Room):
    def __init__(self):
        super().__init__(name="Bedroom", rarity=0, gem_cost=0, color="purple", image_path="NouvelleSalleThèmeHorreur/Bedroom_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': False, 'west': True}

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
            items = []
            
            # Boucle pour donner 2 objets
            for _ in range(2):
                # Tire une classe d'objet en respectant les poids
                # r.choices renvoie une liste, on prend le premier élément [0]
                choix_classe = r.choices(classes_possibles, weights=poids, k=1)[0]
                
                # Crée une instance de cet objet
                item_instance = choix_classe() 

                # Gère l'ajout à l'inventaire en fonction du type
                if isinstance(item_instance, objet.Permanent):
                    # La méthode 'utiliser' des objets permanents les active
                    # (ex: player.pelle = True)
                    item_instance.utiliser(player)
                    items.append(item_instance.nom)
                    
                elif isinstance(item_instance, objet.Nourriture):
                    # La nourriture est ajoutée au dictionnaire 'objets'
                    nom = item_instance.nom
                    if nom in player.objets:
                        player.objets[nom] += 1
                    else:
                        player.objets[nom] = 1
                    items.append(nom)

            # Retourner le message de feedback
            if items:
                return f"Vous trouvez : {', '.join(items)} !"
            else:
                return "Le placard est vide..." 

        return None 


class Courtyard(Room):
    def __init__(self):
        super().__init__(name="Courtyard", rarity=1, gem_cost=1, color="green", image_path="NouvelleSalleThèmeHorreur/Courtyard_Icon.webp")
        self.set_doors()
        self.dig_spot = True

    def set_doors(self):
        self.door_location = {'north': False, 'south': True, 'east': True, 'west': True}
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            self.First_time = False

            # On vérifie si le joueur a déjà une pelle 
            if not player.pelle:
                player.ramasser_objet(objet.Pelle())
                return "Vous avez trouvé une Pelle abandonnée !"

        return None 
        
    
class Corridor(Room):
    def __init__(self):
        super().__init__(name="Corridor", rarity=1, gem_cost=0, color="orange", image_path="NouvelleSalleThèmeHorreur/Corridor_Icon.webp")
        self.set_doors()

    def set_doors(self):
        self.door_location = {'north': True, 'south': True, 'east': False, 'west': False}
    

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
    
    def apply_entry_effect(self, player, grid):
        if self.First_time:
            self.First_time = False
            
            val = r.randint(0,3)

            if val == 0 :
                if player.pieces > 0:
                    player.pieces = 0
                    return f"Un voleur surgit et dérobe toutes vos pièces !"
                else:
                    return f"Le voleur essaie de prendre vos pièces, mais vous n'en avez pas. Ouf !"

            if val == 1 :
                if player.gemmes > 0:
                    player.gemmes = 0
                    return f"Un voleur surgit et dérobe toutes vos gemmes !"
                else:
                    return f"Le voleur essaie de prendre vos gemmes, mais vous n'en avez pas. Ouf !"
                
            if val == 2 :
                if player.cles > 0:
                    player.cles = 0
                    return f"Un voleur surgit et dérobe toutes vos clés !"
                else:
                    return f"Le voleur essaie de prendre vos clés, mais vous n'en avez pas. Ouf !"

            if val == 3 :
                if player.des > 0:
                    player.des = 0
                    return f"Un voleur surgit et dérobe toutes vos dés !"
                else:
                    return f"Le voleur essaie de prendre vos dés, mais vous n'en avez pas. Ouf !"
               
        return None


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
    
    
    def apply_every_entry_effect(self, player, grid):
        player.pas -= 2
        return "Un basket avec des fantomes ? mauvaise idée. Vous perdez 2 pas"
        


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
        
        if self.First_time:
            self.First_time = False
            return "open_shop_pawnshop"
        return None
    
    def apply_every_entry_effect(self, player, grid):
        if self.First_time == False:
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
            items = []
            
            # Boucle pour donner 2 objets
            for _ in range(2):
                # Tire une classe d'objet en respectant les poids
                # r.choices renvoie une liste, on prend le premier élément [0]
                choix_classe = r.choices(classes_possibles, weights=poids, k=1)[0]
                
                # Crée une instance de cet objet
                item_instance = choix_classe() 

                # Gère l'ajout à l'inventaire en fonction du type
                if isinstance(item_instance, objet.Permanent):
                    # La méthode 'utiliser' des objets permanents les active
                    # (ex: player.pelle = True)
                    item_instance.utiliser(player)
                    items.append(item_instance.nom)
                    
                elif isinstance(item_instance, objet.Nourriture):
                    # La nourriture est ajoutée au dictionnaire 'objets'
                    nom = item_instance.nom
                    if nom in player.objets:
                        player.objets[nom] += 1
                    else:
                        player.objets[nom] = 1
                    items.append(nom)

            # Retourner le message de feedback
            if items:
                return f"Vous trouvez : {', '.join(items)} !"
            else:
                return "Le placard est vide..." 

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





