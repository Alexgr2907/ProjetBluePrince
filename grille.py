import pygame
# Importe toutes les classes de ton fichier rooms.py
from rooms import *
import random
from rooms_manager import create_initial_deck, draw_three_rooms
#  Initialisation de Pygame 
pygame.init()

#  Constantes du jeu 
MANOR_WIDTH = 5   # 5 colonnes
MANOR_HEIGHT = 9  # 9 rangées
GRID_SIZE = 80    # Taille de chaque case de la grille en pixels

# Couleurs 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PLAYER_COLOR = (255, 0, 0)  # Rouge pour le curseur du joueur
RED = (255, 0, 0)
SELECTION_COLOR = (255, 255, 255)

# constante pour l'affichage 
ROOM_FONT = pygame.font.Font(None, 18) # Police pour le nom de la pièce
MENU_TITLE_FONT = pygame.font.Font(None, 60) # Police pour le titre
MENU_CARD_FONT = pygame.font.Font(None, 24)  # Police pour le nom/coût
MENU_KEY_FONT = pygame.font.Font(None, 40)   # Police pour les touches (Q, S, D)
CARD_IMAGE_SIZE = 200 # Taille de l'image de la carte (ex: 200x200 pixels)
CARD_PADDING = 60     # Espace entre chaque carte

# Créer la grille du manoir (9 rangées, 5 colonnes)
# Remplie de 'None' (vide) au début
manor_grid = [[None for _ in range(MANOR_WIDTH)] for _ in range(MANOR_HEIGHT)]

# Configuration de la fenêtre (Plein écran)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption("Projet Blue Prince (simplifié)")

# Variables pour la position du joueur (en cases de grille)
player_x = 2
player_y = 8

# Place la salle de départ 
start_room = Horror_Hall() # Crée une instance de ta salle
manor_grid[player_y][player_x] = start_room # Place-la dans la grille logique

# Variables pour la SÉLECTION de la cible
# 'target' représente la case que le joueur vise
target_x = player_x
target_y = player_y
selected_direction = None # Reste à None si aucune direction n'est choisie

# Variables de l'inventaire du joueur
player_steps = 70 
player_gems = 2
player_keys = 0
player_dice = 0

# creer le deck avec toute les pièces qui vont pouvoir être piocher
main_deck = create_initial_deck()


# GESTION D'ÉTAT 
game_state = "moving" # "moving" ou "selecting_room"
current_room_selection = [] # Stocke les 3 pièces piochées

# Variables pour les messages feedback 
feedback_message = ""
feedback_message_time = 0

# Boucle de jeu principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                # Si on est en sélection, Esc annule la sélection
                if game_state == "selecting_room":
                    game_state = "moving"
                    current_room_selection = []
                    selected_direction = None
                else: # Sinon, Esc quitte le jeu
                    running = False
            
            #  ÉTAT 1: LE JOUEUR SE DÉPLACE SUR LA GRILLE
            if game_state == "moving":
                # Logique de SÉLECTION (ZQSD)
                if event.key == pygame.K_z:  # Haut
                    selected_direction = 'up'
                    target_x = player_x
                    target_y = max(0, player_y - 1) 
                elif event.key == pygame.K_s: # Bas
                    selected_direction = 'down'
                    target_x = player_x
                    target_y = min(MANOR_HEIGHT - 1, player_y + 1)
                elif event.key == pygame.K_q: # Gauche
                    selected_direction = 'left'
                    target_x = max(0, player_x - 1)
                    target_y = player_y 
                elif event.key == pygame.K_d: # Droite
                    selected_direction = 'right'
                    target_x = min(MANOR_WIDTH - 1, player_x + 1)
                    target_y = player_y
                
                # Logique de VALIDATION (Espace / Entrée)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_direction is not None and (target_x != player_x or target_y != player_y):
                        
                        #  LOGIQUE DE VÉRIFICATION DES PORTES 
                        current_room = manor_grid[player_y][player_x]
                        current_doors = current_room.get_rotated_doors()
                        
                        # 1. Vérifier si la PIÈCE ACTUELLE a une porte dans la direction visée
                        has_exit = False
                        if selected_direction == 'up' and current_doors['north']: has_exit = True
                        elif selected_direction == 'down' and current_doors['south']: has_exit = True
                        elif selected_direction == 'left' and current_doors['west']: has_exit = True
                        elif selected_direction == 'right' and current_doors['east']: has_exit = True

                        if not has_exit:
                            #  DÉCLENCHE LE MESSAGE D'ERREUR
                            feedback_message = "Il n'y a pas d'accès de ce côté"
                            feedback_message_time = pygame.time.get_ticks() + 2000 # Affiche 2 sec
                            selected_direction = None # Annule la sélection
                            target_x = player_x
                            target_y = player_y
                            continue 
                        
                        # SI LA PIÈCE ACTUELLE A UNE PORTE, on continue 
                        target_cell = manor_grid[target_y][target_x]
                        
                        # CAS 1: CASE VIDE (NOUVELLE PIÈCE) 
                        if target_cell is None:
                            # La porte existe (vérifié au-dessus), on peut ouvrir le menu
                            # (Ici, tu ajouteras la logique des portes verrouillées plus tard)
                            
                            current_room_selection = draw_three_rooms(main_deck, player_gems, manor_grid, target_x, target_y, player_x, player_y)
                            if current_room_selection: # S'il reste des pièces à piocher
                                game_state = "selecting_room"
                            else:
                                feedback_message = "Aucune pièce ne peut aller ici !"
                                feedback_message_time = pygame.time.get_ticks() + 2000
                                selected_direction = None
                        
                        # CAS 2: CASE DÉJÀ DÉCOUVERTE 
                        else:
                            # 2. Vérifier si la PIÈCE CIBLE a une porte correspondante
                            target_doors = target_cell.get_rotated_doors()
                            has_entry = False
                            if selected_direction == 'up' and target_doors['south']: has_entry = True
                            elif selected_direction == 'down' and target_doors['north']: has_entry = True
                            elif selected_direction == 'left' and target_doors['east']: has_entry = True
                            elif selected_direction == 'right' and target_doors['west']: has_entry = True

                            if has_entry:
                                # (Ici, tu ajouteras la logique des portes verrouillées)
                                # Mouvement normal
                                player_x = target_x
                                player_y = target_y
                                player_steps -= 1
                                target_cell.apply_every_entry_effect(None) 
                                selected_direction = None
                                target_x = player_x
                                target_y = player_y
                            else:
                                # DÉCLENCHE LE MESSAGE D'ERREUR 
                                feedback_message = "Il n'y a pas d'accès de ce côté"
                                feedback_message_time = pygame.time.get_ticks() + 2000 # Affiche 2 sec
                                selected_direction = None
                                target_x = player_x
                                target_y = player_y

                # Si on appuie sur une autre touche, on annule la sélection
                elif event.key not in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d, pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                    selected_direction = None
                    target_x = player_x
                    target_y = player_y
            
            # ÉTAT 2: LE JOUEUR CHOISIT UNE PIÈCE 
            elif game_state == "selecting_room":
                choice = -1
                # Utilise QSD pour la sélection
                if event.key == pygame.K_q: # Touche Q  pour 1er choix
                    choice = 0
                elif event.key == pygame.K_s: # Touche S pour 2e choix
                    choice = 1
                elif event.key == pygame.K_d: # Touche D pour 3e choix
                    choice = 2
                
                # Si un choix valide (Q, S ou D) est fait
                if 0 <= choice < len(current_room_selection):
                    chosen_room = current_room_selection[choice]
                    
                    # Vérifie si le joueur a assez de gemmes
                    if player_gems >= chosen_room.gem_cost:
                        # Paye le coût en gemmes
                        player_gems -= chosen_room.gem_cost
                        
                        # On prend la première rotation valide trouvée.
                        # (Tu pourrais implémenter la logique "préférer le nord" ici)
                        chosen_room.rotation = chosen_room.valid_rotations[0]

                        # Place la pièce dans la grille (sur la case cible)
                        manor_grid[target_y][target_x] = chosen_room
                        
                        # Retire la pièce de la pioche
                        if chosen_room in main_deck:
                            main_deck.remove(chosen_room)
                        
                        # Déplace le joueur dans la nouvelle pièce
                        player_x = target_x
                        player_y = target_y
                        player_steps -= 1
                        
                        # Applique l'effet "première entrée" (à implémenter)
                        chosen_room.apply_entry_effect(None) # (Passe l'objet 'player')
                        
                        # Réinitialise et revenir au mode "moving"
                        game_state = "moving"
                        current_room_selection = []
                        selected_direction = None
                        target_x = player_x
                        target_y = player_y
                        
                    else:
                        print("Pas assez de gemmes !") # (Tu pourras afficher ça à l'écran)
                
                # Permet d'annuler la sélection avec Backspace
                elif event.key == pygame.K_BACKSPACE:
                    game_state = "moving"
                    current_room_selection = []
                    selected_direction = None


    # Logique de fin de partie (défaite)
    if player_steps <= 0:
        screen.fill(BLACK)
        font_large = pygame.font.Font(None, 100)
        perdu_text = font_large.render("Perdu !", True, RED)
        perdu_rect = perdu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(perdu_text, perdu_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        continue 


    # Affichage (si le jeu n'est pas fini)
    screen.fill(BLACK) 

    # Calculer le décalage pour centrer la grille
    grid_total_width = MANOR_WIDTH * GRID_SIZE
    grid_total_height = MANOR_HEIGHT * GRID_SIZE
    start_x = (SCREEN_WIDTH - grid_total_width) // 2
    start_y = (SCREEN_HEIGHT - grid_total_height) // 2

    # Dessiner la grille 5x9
    for x_idx in range(MANOR_WIDTH + 1):
        x_pos = start_x + x_idx * GRID_SIZE
        pygame.draw.line(screen, GRAY, (x_pos, start_y), (x_pos, start_y + grid_total_height))
    for y_idx in range(MANOR_HEIGHT + 1):
        y_pos = start_y + y_idx * GRID_SIZE
        pygame.draw.line(screen, GRAY, (start_x, y_pos), (start_x + grid_total_width, y_pos))

    # Dessiner les pièces 

    for y_idx in range(MANOR_HEIGHT):
        for x_idx in range(MANOR_WIDTH):
            # Récupère la pièce (ou None) depuis la grille logique
            room = manor_grid[y_idx][x_idx]
            
            # S'il y a une pièce découverte à cet endroit
            if room is not None:
                # Calcule sa position en pixels
                room_pixel_x = start_x + x_idx * GRID_SIZE
                room_pixel_y = start_y + y_idx * GRID_SIZE
                piece_rect = pygame.Rect(room_pixel_x, room_pixel_y, GRID_SIZE, GRID_SIZE)

                if room.image: # Si la pièce a une image associée
                    # Redimensionne l'image pour qu'elle corresponde à la taille de la case
                    #  Gérer la rotation de l'image 
                    scaled_image = pygame.transform.scale(room.image, (GRID_SIZE, GRID_SIZE))
                    
                    # Fait pivoter l'image (rotation * 90 degrés anti-horaire)
                    rotated_image = pygame.transform.rotate(scaled_image, room.rotation * 90)
                    
                    # Recalcule le rectangle pour centrer l'image pivotée
                    img_rect = rotated_image.get_rect(center = piece_rect.center)
                    
                    screen.blit(rotated_image, img_rect) # Dessine l'image pivotée
                else: # Sinon (si pas d'image, ou si le chargement a échoué)
                    pygame.draw.rect(screen, (50, 50, 50), piece_rect) # Dessine un carré gris
                    # Tu peux toujours afficher le nom si tu veux, même sans image
                    room_name_text = ROOM_FONT.render(room.name, True, WHITE)
                    text_rect = room_name_text.get_rect(center=(room_pixel_x + GRID_SIZE // 2, room_pixel_y + GRID_SIZE // 2))
                    screen.blit(room_name_text, text_rect)
    
    # Dessine le curseur du JOUEUR (sa position ACTUELLE)
    player_pixel_x = start_x + player_x * GRID_SIZE
    player_pixel_y = start_y + player_y * GRID_SIZE
    player_cursor = pygame.Rect(player_pixel_x, player_pixel_y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_cursor, 2)  # Trait rouge épais 

    # Dessine le curseur de SÉLECTION (la CIBLE)
    if selected_direction is not None:
        target_pixel_x = start_x + target_x * GRID_SIZE
        target_pixel_y = start_y + target_y * GRID_SIZE
        target_cursor = pygame.Rect(target_pixel_x, target_pixel_y, GRID_SIZE, GRID_SIZE)
        # On le dessine en blanc, avec un trait plus fin
        pygame.draw.rect(screen, SELECTION_COLOR, target_cursor, 2) 

    # Affiche l'inventaire
    font = pygame.font.Font(None, 36)
    inventory_text_str = f"Pas: {player_steps} | Gemmes: {player_gems} | Clés: {player_keys} | Dés: {player_dice}"
    inventory_text = font.render(inventory_text_str, True, WHITE)
    screen.blit(inventory_text, (10, 10)) 

    #  AFFICHER LE MESSAGE FEEDBACK 
    if feedback_message and pygame.time.get_ticks() < feedback_message_time:
        # Calcule la position (à droite de la grille)
        message_x = start_x + grid_total_width + 20 # 20px à droite de la grille
        message_y = start_y + (grid_total_height // 2) # Centré verticalement
        
        # Utilise une police un peu plus grande pour le message
        message_text = MENU_CARD_FONT.render(feedback_message, True, RED) 
        message_rect = message_text.get_rect(midleft=(message_x, message_y))
        
        screen.blit(message_text, message_rect)
    elif pygame.time.get_ticks() >= feedback_message_time:
        feedback_message = "" # Efface le message après le délai

    # DESSINER LE MENU DE SÉLECTION 
    if game_state == "selecting_room":
        # ... (ton code pour le fond semi-transparent et le titre) ...

        # Calcul des positions des 3 cartes
        num_cards = len(current_room_selection)
        total_cards_width = (num_cards * CARD_IMAGE_SIZE) + ((num_cards - 1) * CARD_PADDING)
        start_menu_x = (SCREEN_WIDTH - total_cards_width) // 2
        
        # Position Y (centrée verticalement)
        y_pos_image = (SCREEN_HEIGHT - CARD_IMAGE_SIZE) // 2
        
        # Les touches de sélection (Q, S, D)
        keys_to_show = ['Q', 'S', 'D']

        for i, room in enumerate(current_room_selection):
            # Position X de la carte
            x_pos = start_menu_x + i * (CARD_IMAGE_SIZE + CARD_PADDING) 
            # Avant de dessiner, on définit la rotation pour l'affichage de cette vignette
            display_rotation = 0 # Par défaut
            if room.valid_rotations: # Si la pièce a des rotations valides
                display_rotation = room.valid_rotations[0] # On prend la première valide
            
            # Dessine l'image de la pièce (plus grande)
            if room.image:
                img = pygame.transform.scale(room.image, (CARD_IMAGE_SIZE, CARD_IMAGE_SIZE))
                
                # Fait pivoter l'image pour l'affichage dans le menu
                rotated_img = pygame.transform.rotate(img, display_rotation * 90)
                
                # Recalcule le rectangle pour centrer l'image pivotée
                img_rect = rotated_img.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE // 2))
                
                screen.blit(rotated_img, img_rect.topleft) # Dessine l'image
            else: # Fallback si pas d'image
                pygame.draw.rect(screen, GRAY, (x_pos, y_pos_image, CARD_IMAGE_SIZE, CARD_IMAGE_SIZE))

            # Affiche les textes SOUS l'image 

            # Dessine le nom
            name_text = MENU_CARD_FONT.render(room.name, True, WHITE)
            name_rect = name_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE + 30))
            screen.blit(name_text, name_rect)

            # Dessine le coût en gemmes
            gem_color = WHITE if player_gems >= room.gem_cost else RED
            gem_text_str = f"Coût: {room.gem_cost} Gemmes"
            gem_text = MENU_CARD_FONT.render(gem_text_str, True, gem_color)
            gem_rect = gem_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE + 55))
            screen.blit(gem_text, gem_rect)

            # Afficher la touche de sélection AU-DESSUS 
            if i < len(keys_to_show):
                key_text = MENU_KEY_FONT.render(keys_to_show[i], True, BLACK)
                key_bg_rect = key_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image - 40))
                key_bg_rect.inflate_ip(10, 10) 
                pygame.draw.rect(screen, WHITE, key_bg_rect, border_radius=5)
                screen.blit(key_text, key_text.get_rect(center=key_bg_rect.center))
                # Dessine le fond blanc
                pygame.draw.rect(screen, WHITE, key_bg_rect, border_radius=5)
                # Dessine le texte "Q", "S", ou "D" par-dessus
                screen.blit(key_text, key_text.get_rect(center=key_bg_rect.center))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()