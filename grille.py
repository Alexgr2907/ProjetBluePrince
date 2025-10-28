import pygame

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

# Configuration de la fenêtre (Plein écran)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption("Projet Blue Prince (simplifié)")

# Variables pour la position du joueur (en cases de grille)
player_x = 2
player_y = 8

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


# Boucle de jeu principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Logique de SÉLECTION (ZQSD)
            # ZQSD ne fait que changer la 'target'
            
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
            # C'est ICI qu'on bouge et qu'on perd un pas
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                
                # On vérifie qu'une direction est bien sélectionnée
                # ET que la cible n'est pas la case où on est déjà
                if selected_direction is not None and (target_x != player_x or target_y != player_y):
                    
                    # (Plus tard, vous ajouterez ici la vérification des portes, 
                    # des clés, etc.)
                    
                    # Mouvement validé !
                    player_x = target_x # Le joueur prend la position de la cible
                    player_y = target_y
                    player_steps -= 1 # On perd 1 pas
                    
                    # print(f"Mouvement validé ! Pas restants: {player_steps}")
                    
                    # On réinitialise la sélection
                    selected_direction = None
                    target_x = player_x
                    target_y = player_y
                
                # Si la sélection est invalide (même case)
                else:
                    selected_direction = None
                    target_x = player_x
                    target_y = player_y
            
            # Si on appuie sur une autre touche, on annule la sélection
            else:
                 selected_direction = None
                 target_x = player_x
                 target_y = player_y


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

    # Dessiner les pièces (Exemple: "Entrance Hall")
    piece_rect = pygame.Rect(start_x + 2 * GRID_SIZE, start_y + 8 * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, (50, 50, 50), piece_rect) 

    # 1. Dessiner le curseur du JOUEUR (sa position ACTUELLE)
    player_pixel_x = start_x + player_x * GRID_SIZE
    player_pixel_y = start_y + player_y * GRID_SIZE
    player_cursor = pygame.Rect(player_pixel_x, player_pixel_y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_cursor, 5)  # Trait rouge épais

    # 2. Dessiner le curseur de SÉLECTION (la CIBLE)
    if selected_direction is not None:
        target_pixel_x = start_x + target_x * GRID_SIZE
        target_pixel_y = start_y + target_y * GRID_SIZE
        target_cursor = pygame.Rect(target_pixel_x, target_pixel_y, GRID_SIZE, GRID_SIZE)
        # On le dessine en blanc, avec un trait plus fin
        pygame.draw.rect(screen, SELECTION_COLOR, target_cursor, 2) 

    # Afficher l'inventaire
    font = pygame.font.Font(None, 36)
    inventory_text_str = f"Pas: {player_steps} | Gemmes: {player_gems} | Clés: {player_keys} | Dés: {player_dice}"
    inventory_text = font.render(inventory_text_str, True, WHITE)
    screen.blit(inventory_text, (10, 10)) 

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()