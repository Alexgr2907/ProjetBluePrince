# Ce fichier servira à mettre tout les fonctions en lien avec la logique et la gestion des salles
import random
# Importe toutes les classes de ton fichier rooms.py
from rooms import *

def create_initial_deck():
    """
    Crée la liste d'instances de pièces pour la pioche.
    """
    # Ne pas ajouter Horror_Hall, elle est déjà placée
    # si il y a 4 fois le nom d'une salle, 
    # cela signifie que l'on peut tirer quatre fois cette salle
    deck = [
        Midas_vault(),
        Gallery(),Gallery(),Gallery(),Gallery(),
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
        Billiard_Room(),Billiard_Room(),Billiard_Room(),Billiard_Room(),
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
    
    # [cite_start]Ajoute des exemplaires supplémentaires si tu le souhaites [cite: 95]
    # deck.append(Pantry())
    # deck.append(Corridor())
    
    return deck


def draw_three_rooms(deck, player_gems):
    """
    Pioche 3 pièces en respectant la rareté et la contrainte de gemmes.
    """
    if not deck:
        return [] # Pioche vide

    # [cite_start]Calcule les poids en fonction de la rareté [cite: 90]
    # Rareté 0: Poids 3^3=27 | Rareté 1: Poids 3^2=9 | ...
    weights = []
    for room in deck:
        # Poids = 3^(3 - rareté)
        # (Si rareté 0, poids=27. Si rareté 3, poids=1)
        weight = 3**(3 - room.rarity) 
        weights.append(weight)

    # Pioche 3 pièces
    # Assure-toi de ne pas piocher plus de pièces qu'il n'en reste
    k_value = min(3, len(deck))
    drawn_rooms = random.choices(deck, weights=weights, k=k_value)

    # [cite_start]Assure qu'au moins une pièce coûte 0 gemme [cite: 130]
    if not any(room.gem_cost == 0 for room in drawn_rooms):
        # Trouve les pièces à 0 gemme disponibles dans la pioche
        zero_cost_rooms = [room for room in deck if room.gem_cost == 0]
        if zero_cost_rooms:
            # Remplace une des pièces piochées par une pièce à 0 gemme
            drawn_rooms[random.randint(0, k_value - 1)] = random.choice(zero_cost_rooms)
            
    return drawn_rooms
