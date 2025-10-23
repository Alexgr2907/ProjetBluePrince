#test push pull et clonage
import pygame

# --- Initialisation de Pygame ---
pygame.init()

# --- Constantes pour la configuration de la fenêtre et de la grille ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 50  # Taille de chaque case de la grille en pixels
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# --- Couleurs ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PLAYER_COLOR = (255, 0, 0)  # Rouge pour le curseur du joueur

# --- Configuration de la fenêtre ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mon Jeu en Pygame")

# --- Variables pour la position du joueur ---
player_x = 0
player_y = 0

# --- Boucle de jeu principale ---
running = True
while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Logique de jeu (à développer) ---
    # Pour l'instant, nous ne gérons que l'affichage

    # --- Affichage ---
    screen.fill(WHITE)  # Fond blanc

    # Dessiner la grille
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    # Dessiner les pièces (exemple simple avec des rectangles)
    # Vous remplacerez ceci par vos images
    # Exemple : une pièce en position (3, 4) de la grille
    piece_rect = pygame.Rect(3 * GRID_SIZE, 4 * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, BLACK, piece_rect)

    # Dessiner le curseur du joueur
    player_cursor = pygame.Rect(player_x * GRID_SIZE, player_y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_cursor, 5)  # Le 5 est l'épaisseur du trait

    # Afficher l'inventaire (texte simple)
    font = pygame.font.Font(None, 36)  # Utilise la police par défaut, taille 36
    inventory_text = font.render("Inventaire: Clé x1", True, BLACK)
    screen.blit(inventory_text, (10, 10)) # Position du texte

    # --- Mettre à jour l'affichage ---
    pygame.display.flip()

# --- Quitter Pygame ---
pygame.quit()