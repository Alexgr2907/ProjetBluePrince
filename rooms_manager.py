# Ce fichier servira à mettre tout les fonctions en lien avec la logique et la gestion des salles
import random
# Importe toutes les classes de ton fichier rooms.py
from rooms import *
import inspect
import objet


MANOR_WIDTH = 5
MANOR_HEIGHT = 9

def get_entry_direction(from_x, from_y, to_x, to_y):
    """Détermine de quelle direction le joueur ARRIVE."""
    # from_y et from_x correspondent aux coordonnées de la salle où on est actuellement.
    # on compare ici de manière logique si la coordonnées de la où on est, 
    # est plus grande que celle où on va pour déterminer d'où l'on arrive
    if from_y > to_y: return 'south'
    if from_y < to_y: return 'north'
    if from_x > to_x: return 'east'
    if from_x < to_x: return 'west'

    return None

def check_walls(rotated_doors, x, y):
    """Vérifie que les portes ne mènent pas hors de la grille."""
    if rotated_doors['north'] and y == 0: return False
    if rotated_doors['south'] and y == MANOR_HEIGHT - 1: return False
    if rotated_doors['west'] and x == 0: return False
    if rotated_doors['east'] and x == MANOR_WIDTH - 1: return False
    return True

def check_neighbors(rotated_doors, grid, x, y):
    """Vérifie la compatibilité avec les pièces voisines DÉJÀ en place."""
    # Voisin du NORD (s'il existe)
    if y > 0 and grid[y-1][x] is not None:
        neighbor_doors = grid[y-1][x].get_rotated_doors()
        # Si j'ai une porte Nord, il doit avoir une porte Sud (et inversement)
        if rotated_doors['north'] != neighbor_doors['south']: return False
            
    # Voisin du SUD (s'il existe)
    if y < MANOR_HEIGHT - 1 and grid[y+1][x] is not None:
        neighbor_doors = grid[y+1][x].get_rotated_doors()
        if rotated_doors['south'] != neighbor_doors['north']: return False

    # Voisin de l'OUEST (s'il existe)
    if x > 0 and grid[y][x-1] is not None:
        neighbor_doors = grid[y][x-1].get_rotated_doors()
        if rotated_doors['west'] != neighbor_doors['east']: return False
        
    # Voisin de l'EST (s'il existe)
    if x < MANOR_WIDTH - 1 and grid[y][x+1] is not None:
        neighbor_doors = grid[y][x+1].get_rotated_doors()
        if rotated_doors['east'] != neighbor_doors['west']: return False
        
    return True


def find_valid_rotations(room, grid, target_x, target_y, from_x, from_y):
    """
    Teste les 4 rotations pour une pièce et retourne la liste des rotations valides.
    """
    valid_rotations = []
    entry_direction = get_entry_direction(from_x, from_y, target_x, target_y)
    
    # Si on ne sait pas d'où on vient (cas de départ ?), on ne peut rien faire
    if entry_direction is None: 
        return []

    for r in range(4): # Teste les 4 rotations (0, 1, 2, 3)
        room.rotation = r
        rotated_doors = room.get_rotated_doors()
        
        # 1. La porte d'entrée doit exister
        if not rotated_doors[entry_direction]:
            continue # Cette rotation est invalide, on passe à la suivante
            
        # 2. Les portes ne doivent pas donner sur un mur extérieur
        if not check_walls(rotated_doors, target_x, target_y):
            continue
            
        # 3. Les portes doivent correspondre aux voisins
        # (Cette fonction ignore la case d'où on vient, c'est géré au-dessus)
        if not check_neighbors(rotated_doors, grid, target_x, target_y):
            continue

        valid_rotations.append(r)
        
    # Réinitialise la rotation pour ne pas affecter la pioche
    room.rotation = 0 
    return valid_rotations


def create_initial_deck():
    """
    Crée la liste d'instances de pièces pour la pioche.
    """
    # Ne pas ajouter Horror_Hall, elle est déjà placée
    # si il y a 4 fois le nom d'une salle, 
    # cela signifie que l'on peut tirer quatre fois cette salle
    deck = [
        Midas_vault(),
        Gallery(),Gallery(),
        Dracula_tomb(),
        Garage(),Garage(),
        Joker_Office(),
        Locksmith(),
        Maze(),
        Bedroom(),
        Closet(),Closet(),
        Courtyard(),
        Corridor(),Corridor(),
        Pantry(),Pantry(),
        Thief_Storage(),
        Billiard_Room(),Billiard_Room(),
        Chucky_Bedroom(),Chucky_Bedroom(),
        Statue_Hall(),Statue_Hall(),
        Pumpkin_Field(),
        Pawn_Shop(),
        Patio(),
        Passageway(),Passageway(),
        Master_Bedroom(),
        Loot_Stash(),Loot_Stash(),
        Haunted_Gym(),
        Devil_Church()
    ]
    return deck


def draw_three_rooms(deck, player_gems, grid, target_x, target_y, from_x, from_y, reroll=False):
    """
    Pioche 3 pièces en respectant la rareté et la contrainte de gemmes.
    reroll = True indique que l'appel proveint d'un retirage avec un dé
    """
    if not deck:
        return [] # Pioche vide

    # Filtrer le deck 
    placeable_deck = []
    
    for room in deck:
        # Trouve toutes les rotations possibles pour cette pièce à cet endroit
        valid_rots = find_valid_rotations(room, grid, target_x, target_y, from_x, from_y)
        
        # Si au moins une rotation est possible
        if valid_rots:
            room.valid_rotations = valid_rots # Stocke les rotations valides
            placeable_deck.append(room)
            
    if not placeable_deck:
        return []
    
    # Calcule les poids en fonction de la rareté
    # Rareté 0: Poids 3^3=27 ; Rareté 1: Poids 3^2=9 ; ...
    weights = []
    for room in placeable_deck:
        # Poids = 3^(3 - rareté)
        # (Si rareté 0, poids=27. Si rareté 3, poids=1)
        weight = 3**(3 - room.rarity) 
        weights.append(weight)

    # Pioche 3 pièces
    # Assure-toi de ne pas piocher plus de pièces qu'il n'en reste
    k_value = min(3, len(deck))
    drawn_rooms = random.choices(placeable_deck, weights=weights, k=k_value)

    # Assure qu'au moins une pièce coûte 0 gemme 
    if not any(room.gem_cost == 0 for room in drawn_rooms):
        # Trouve les pièces à 0 gemme disponibles dans la pioche
        zero_cost_rooms = [room for room in placeable_deck if room.gem_cost == 0]
        if zero_cost_rooms:
            # Remplace une des pièces piochées par une pièce à 0 gemme
            drawn_rooms[random.randint(0, k_value - 1)] = random.choice(zero_cost_rooms)
            
    return drawn_rooms


#-------------------- Pioche aléatoire des consommables

def pioche_aleatoire_objet(taux_drop: float = 0.5):
    """
    Détermine si un objet doit être pioché et lequel
    """

    if random.random() > taux_drop :
        return None # Aucun objet est dropé
    
    classes = list(proba_objets.keys())
    poids = list(proba_objets.values())

    if not classes:
        print("Avertissement : Le catalogue 'proba_objets' est vide. Aucun objet n'a pu être pioché.")
        return None

    pioche_classe = random.choices(classes, weights=poids, k=1)[0]  
    
    return pioche_classe() # Pour tous les autres objets

#-------------------- Pioche aléatoire de l'endroit à creuser

def pioche_butin_creuser():
    """
    Détermine le butin apres avoir creusé : 50% rien, 50% des objets consommbales
    """

    if random.random() < 0.5 :

        consommable_classes = {
            cls : weight
            for cls, weight in proba_objets.items()
            if inspect.isclass(cls) and issubclass(cls, objet.Consommable) # Vérifie que c'est une classe consommable
        }

        if not consommable_classes:
            return None
    
        classes = list(consommable_classes.keys())
        poids = list(consommable_classes.values())

        pioche_classe = random.choices(classes, weights = poids, k=1)[0]
        return pioche_classe()
    
    else :
        return None
    

def determine_lock_level(row_index):
    """
    Détermine le niveau de verrouillage (0, 1, ou 2) en fonction de la rangée.
    """
    # row_index 0 est le HAUT (fin), row_index 8 est le BAS (début)
    
    # Première rangée (où on commence, y=8) : toujours niveau 0
    if row_index == MANOR_HEIGHT - 1: # 8
        return 0
    
    # Dernière rangée (Antichambre, y=0) : toujours niveau 2
    if row_index == 0:
        return 2
    
    # --- Rangs intermédiaires ---
    # Convertit la rangée (7 -> 1) en "progrès" (0.125 -> 0.875)
    # Plus on est haut (proche de 0), plus 'progress' est proche de 1.0
    progress = 1.0 - (row_index / (MANOR_HEIGHT - 1))
    
    rand_val = random.random()
    
    # Plus on progresse, plus la proba de Niv 2 est haute (max 30%)
    if rand_val < (progress * 0.2):
        return 2
    # Plus on progresse, plus la proba de Niv 1 est haute (max 50%)
    elif rand_val < (progress * 0.4):
        return 1
    else:
        return 0

def set_door_statuses(room, grid, x, y, previous_x, previous_y):
    """
    Initialise le dictionnaire 'doors_statut' pour une nouvelle pièce
    en se basant sur ses portes tournées, ses voisins et la rangée.
    """
    rotated_doors = room.get_rotated_doors()
    
    for direction, has_door in rotated_doors.items():
        if not has_door:
            room.doors_statut[direction] = -1 # Pas de porte
            continue

        # Vérifier les voisins pour assurer la cohérence
        if direction == 'north' and y > 0 and grid[y-1][x] is not None:
            room.doors_statut['north'] = grid[y-1][x].doors_statut['south']
        elif direction == 'south' and y < MANOR_HEIGHT - 1 and grid[y+1][x] is not None:
            room.doors_statut['south'] = grid[y+1][x].doors_statut['north']
        elif direction == 'west' and x > 0 and grid[y][x-1] is not None:
            room.doors_statut['west'] = grid[y][x-1].doors_statut['east']
        elif direction == 'east' and x < MANOR_WIDTH - 1 and grid[y][x+1] is not None:
            room.doors_statut['east'] = grid[y][x+1].doors_statut['west']
        else:
            # C'est une nouvelle porte qui mène au vide. On détermine son verrouillage.
            room.doors_statut[direction] = determine_lock_level(y)
            
    # La porte par laquelle on vient d'entrer est toujours déverrouillée (coût payé)
    entry_dir = get_entry_direction(previous_x, previous_y, x, y)
    if entry_dir:
        room.doors_statut[entry_dir] = 0