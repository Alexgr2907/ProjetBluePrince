import pygame
from rooms import *
import random
from rooms_manager import create_initial_deck, draw_three_rooms
from inventaire import Inventaire
import objet
#  Initialisation de Pygame 
pygame.init()

#  Constantes du jeu 
MANOR_WIDTH = 5
MANOR_HEIGHT = 9
GRID_SIZE = 80

# Couleurs 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PLAYER_COLOR = (255, 0, 0)
RED = (255, 0, 0)
SELECTION_COLOR = (255, 255, 255)
UI_BLUE_DARK = (10, 20, 40)
UI_BLUE_LIGHT = (30, 50, 80)
UI_HIGHLIGHT = (255, 255, 0)

# constante pour l'affichage 
ROOM_FONT = pygame.font.Font(None, 18)
MENU_TITLE_FONT = pygame.font.Font(None, 60)
MENU_CARD_FONT = pygame.font.Font(None, 24)
MENU_KEY_FONT = pygame.font.Font(None, 40)
INV_TITLE_FONT = pygame.font.Font(None, 48)
INV_ITEM_FONT = pygame.font.Font(None, 32)
INV_CONFIRM_FONT = pygame.font.Font(None, 28)
INV_TAB_FONT = pygame.font.Font(None, 24)

# On crée un "catalogue" pour lier les noms d'objets à leurs descriptions
# (qui viennent de objet.py)
ITEM_CATALOG = {
    # Consommables (Nourriture)
    # (Pas de changement ici, objet.py a déjà les bonnes infos)
    "Pomme": objet.Pomme(),         # "Redonne 2 pas."
    "Banane": objet.Banane(),       # "Redonne 3 pas."
    "Gâteau": objet.Gateau(),     # "Redonne 10 pas."
    "Sandwich": objet.Sandwich(),   # "Redonne 15 pas."
    "Repas": objet.Repas(),         # "Redonne 25 pas."
    
    # Permanents
    # (Pas de changement ici, objet.py a déjà les bonnes infos)
    "Pelle": objet.Pelle(),
    "Marteau": objet.Marteau(),
    "Kit de Crochetage": objet.KitCrochetage(),
    "Détecteur de Métaux": objet.DetecteurMetaux(),
    "Patte de Lapin": objet.PatteLapin(),
    
    # --- MODIFICATION ICI ---
    # Autres (on met à jour avec les descriptions officielles)
    "Pas": objet.Objet("Pas", 
                       "Votre énergie. Vous perdez 1 pas à chaque déplacement.", "autre", 0),
    "Pièces": objet.Objet("Pièces", 
                         "Peut être dépensé dans certaines salles en échange d'autres objets.", "autre", 0),
    "Gemmes": objet.Objet("Gemmes", 
                         "Peut être dépensé pour choisir certaines salles lors du tirage au sort.", "autre", 1),
    "Clés": objet.Objet("Clés", 
                       "Ouvre les portes fermées à clé, ou des coffres.", "autre", 2),
    "Dés": objet.Objet("Dés", 
                      "Permet de tirer à nouveau au sort les pièces proposées.", "autre", 1),
}


CARD_IMAGE_SIZE = 200
CARD_PADDING = 60
# Fonction pour dessiner du texte sur plusieurs lignes
def draw_text_wrapped(surface, text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    y = rect.top
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.left, y))
        y += font.get_linesize()
# La fonction est déplacée AVANT la boucle de jeu
def draw_inventory_ui(screen, inventory, category_index, selected_index, sub_state, selected_item_name, context_menu_index, confirm_index):
    # Dimensions de l'interface
    ui_width = SCREEN_WIDTH * 0.7
    ui_height = SCREEN_HEIGHT * 0.8
    ui_x = (SCREEN_WIDTH - ui_width) / 2
    ui_y = (SCREEN_HEIGHT - ui_height) / 2
    ui_rect = pygame.Rect(ui_x, ui_y, ui_width, ui_height)
    
    # Dessine le fond
    pygame.draw.rect(screen, UI_BLUE_DARK, ui_rect, border_radius=15)
    pygame.draw.rect(screen, UI_BLUE_LIGHT, ui_rect, width=5, border_radius=15)
    
    # Dessine le titre
    title_text = INV_TITLE_FONT.render("Inventaire", True, WHITE)
    title_rect = title_text.get_rect(center=(ui_rect.centerx, ui_y + 40))
    screen.blit(title_text, title_rect)
    
    # Dessiner les onglets de catégorie
    categories = ["Consommables", "Permanents", "Autres"]
    tab_width = ui_width / len(categories)
    tab_y = ui_y + 80
    
    for i, tab_name in enumerate(categories):
        tab_rect = pygame.Rect(ui_x + i * tab_width, tab_y, tab_width, 40)
        
        if i == category_index:
            pygame.draw.rect(screen, UI_BLUE_LIGHT, tab_rect, border_top_left_radius=8, border_top_right_radius=8)
            color = UI_HIGHLIGHT
        else:
            color = GRAY
            pygame.draw.line(screen, UI_BLUE_LIGHT, (tab_rect.left, tab_rect.bottom - 1), (tab_rect.right, tab_rect.bottom - 1), 2)

        tab_text = INV_TAB_FONT.render(tab_name, True, color)
        tab_text_rect = tab_text.get_rect(center=tab_rect.center)
        screen.blit(tab_text, tab_text_rect)
    
    item_y_start = tab_y + 60

    # --- ONGLET 0: CONSOMMABLES ---
    if category_index == 0:
        consumable_list = list(inventory.objets.items())
        
        if not consumable_list:
            empty_text = INV_ITEM_FONT.render("Aucun objet consommable.", True, GRAY)
            empty_rect = empty_text.get_rect(center=(ui_rect.centerx, ui_rect.centery))
            screen.blit(empty_text, empty_rect)
        else:
            for i, (item_name, quantity) in enumerate(consumable_list):
                item_text_str = f"{item_name} x{quantity}"
                color = UI_HIGHLIGHT if i == selected_index else WHITE
                item_text = INV_ITEM_FONT.render(item_text_str, True, color)
                item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * 40))
                screen.blit(item_text, item_rect)
                
                # MODIFICATION: Curseur visible si sélectionné (même dans sous-menu)
                if i == selected_index:
                    color_cercle = UI_HIGHLIGHT if sub_state == "browsing" else WHITE # Moins visible si sous-menu
                    pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- ONGLET 1: PERMANENTS ---
    elif category_index == 1:
        permanent_list = []
        if inventory.pelle: permanent_list.append("Pelle")
        if inventory.marteau: permanent_list.append("Marteau")
        if inventory.kit_crochetage: permanent_list.append("Kit de Crochetage")
        if inventory.detecteur_métaux: permanent_list.append("Détecteur de Métaux")
        if inventory.patte_lapin: permanent_list.append("Patte de Lapin")
        
        if not permanent_list:
            empty_text = INV_ITEM_FONT.render("Aucun objet permanent.", True, GRAY)
            empty_rect = empty_text.get_rect(center=(ui_rect.centerx, ui_rect.centery))
            screen.blit(empty_text, empty_rect)
        else:
            for i, item_name in enumerate(permanent_list):
                # MODIFICATION: Logique de sélection
                item_text_str = item_name
                color = UI_HIGHLIGHT if i == selected_index else WHITE
                item_text = INV_ITEM_FONT.render(item_text_str, True, color)
                item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * 40))
                screen.blit(item_text, item_rect)
                
                if i == selected_index:
                    color_cercle = UI_HIGHLIGHT if sub_state == "browsing" else WHITE
                    pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- ONGLET 2: AUTRES ---
    elif category_index == 2:
        # On utilise les noms de base pour la sélection, et l'affichage formaté
        autres_list_display = [
            f"Pas : {inventory.pas}",
            f"Pièces : {inventory.pieces}",
            f"Gemmes : {inventory.gemmes}",
            f"Clés : {inventory.cles}",
            f"Dés : {inventory.des}"
        ]
        
        for i, item_str in enumerate(autres_list_display):
            # MODIFICATION: Logique de sélection
            color = UI_HIGHLIGHT if i == selected_index else WHITE
            item_text = INV_ITEM_FONT.render(item_str, True, color)
            item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * 40))
            screen.blit(item_text, item_rect)

            if i == selected_index:
                color_cercle = UI_HIGHLIGHT if sub_state == "browsing" else WHITE
                pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- POP-UP : MENU CONTEXTUEL (Dynamique) ---
    if sub_state == "context_menu":
        # MODIFICATION: Options dynamiques
        if category_index == 0:
            options = ["Utiliser", "Infos", "Retour"]
            ctx_height = 120
        else: # Catégories 1 et 2
            options = ["Infos", "Retour"]
            ctx_height = 90
            
        selected_item_y = item_y_start + selected_index * 40
        ctx_width = 150
        
        ctx_x = ui_x + 300 
        ctx_y = max(ui_y + 120, min(selected_item_y, (ui_y + ui_height) - ctx_height - 20))
        
        ctx_rect = pygame.Rect(ctx_x, ctx_y, ctx_width, ctx_height)
        pygame.draw.rect(screen, BLACK, ctx_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, ctx_rect, width=2, border_radius=10)

        for i, option in enumerate(options):
            color = UI_HIGHLIGHT if i == context_menu_index else WHITE
            option_text = INV_ITEM_FONT.render(option, True, color)
            option_rect = option_text.get_rect(midleft=(ctx_x + 20, ctx_y + 30 + i * 30))
            screen.blit(option_text, option_rect)

    # --- POP-UP : CONFIRMATION D'UTILISATION ---
    elif sub_state == "confirming_use" and selected_item_name:
        # ... (Pas de changement ici) ...
        confirm_width = 400
        confirm_height = 150
        confirm_x = (SCREEN_WIDTH - confirm_width) / 2
        confirm_y = (SCREEN_HEIGHT - confirm_height) / 2
        confirm_rect = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)
        
        pygame.draw.rect(screen, BLACK, confirm_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, confirm_rect, width=3, border_radius=10)
        
        question_str = f"Voulez-vous utiliser 1 {selected_item_name} ?"
        question_text = INV_CONFIRM_FONT.render(question_str, True, WHITE)
        question_rect = question_text.get_rect(center=(confirm_rect.centerx, confirm_y + 30))
        screen.blit(question_text, question_rect)
        
        confirm_btn_text_str = "Confirmer (Entrée)"
        cancel_btn_text_str = "Annuler (Echap)"
        
        confirm_color = UI_HIGHLIGHT if confirm_index == 0 else GRAY
        cancel_color = UI_HIGHLIGHT if confirm_index == 1 else GRAY
        
        confirm_btn_text = INV_CONFIRM_FONT.render(confirm_btn_text_str, True, confirm_color)
        cancel_btn_text = INV_CONFIRM_FONT.render(cancel_btn_text_str, True, cancel_color)
        
        confirm_btn_rect = confirm_btn_text.get_rect(center=(confirm_rect.centerx - 80, confirm_y + 100))
        cancel_btn_rect = cancel_btn_text.get_rect(center=(confirm_rect.centerx + 80, confirm_y + 100))
        
        screen.blit(confirm_btn_text, confirm_btn_rect)
        screen.blit(cancel_btn_text, cancel_btn_rect)
    
    # --- POP-UP : INFO OBJET ---
    # --- POP-UP : INFO OBJET ---
    elif sub_state == "showing_info":
        info_width = 400
        info_height = 200 # Augmenté pour le texte
        info_x = (SCREEN_WIDTH - info_width) / 2
        info_y = (SCREEN_HEIGHT - info_height) / 2
        info_rect = pygame.Rect(info_x, info_y, info_width, info_height)
        
        pygame.draw.rect(screen, BLACK, info_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, info_rect, width=3, border_radius=10)
        
        # Titre (Nom de l'objet)
        title_str = selected_item_name
        title_text = INV_CONFIRM_FONT.render(title_str, True, UI_HIGHLIGHT)
        title_rect = title_text.get_rect(center=(info_rect.centerx, info_y + 30))
        screen.blit(title_text, title_rect)

        # MODIFICATION: On va chercher la description dans le CATALOGUE
        info_str = "Aucune info pour le moment." # Par défaut
        if selected_item_name in ITEM_CATALOG:
            info_str = ITEM_CATALOG[selected_item_name].description
        
        # On définit le rectangle pour le texte
        text_rect = pygame.Rect(info_x + 20, info_y + 60, info_width - 40, info_height - 90)
        # On dessine le texte avec la fonction "wrap"
        draw_text_wrapped(screen, info_str, INV_TAB_FONT, WHITE, text_rect)

        # Quitter
        close_str = "Appuyez sur Entrée ou Echap pour fermer"
        close_text = INV_TAB_FONT.render(close_str, True, GRAY) 
        close_rect = close_text.get_rect(center=(info_rect.centerx, info_y + info_height - 30))
        screen.blit(close_text, close_rect)


# Créer la grille du manoir
manor_grid = [[None for _ in range(MANOR_WIDTH)] for _ in range(MANOR_HEIGHT)]

# Configuration de la fenêtre
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption("Projet Blue Prince (simplifié)")

# Position du joueur
player_x = 2
player_y = 8

# Place la salle de départ 
start_room = Horror_Hall() 
manor_grid[player_y][player_x] = start_room 

# Sélection de la cible
target_x = player_x
target_y = player_y
selected_direction = None

# Instance de l'inventaire
player_inventory = Inventaire()
# Ligne de triche pour tester (à enlever plus tard)
# (Décommentez-les pour tester l'inventaire !)
# player_inventory.objets["Pomme"] = 3 
# player_inventory.objets["Banane"] = 1 


# Deck de pièces
main_deck = create_initial_deck()

# GESTION D'ÉTAT 
game_state = "moving" # "moving", "selecting_room", ou "inventory"
current_room_selection = [] 

# Variables pour l'état de l'inventaire
inventory_selected_index = 0
inventory_category_index = 0 
inventory_sub_state = "browsing" 
selected_item_name = None 
context_menu_index = 0 
confirm_selected_index = 0 

# Variables pour les messages feedback 
feedback_message = ""
feedback_message_time = 0

# Boucle de jeu principale
running = True
while running:
    # --- Définir les listes actuelles pour la navigation ---
    # (On fait ça au début de la boucle pour y avoir accès partout)
    consumable_list = list(player_inventory.objets.keys())
    
    permanent_list = []
    if player_inventory.pelle: permanent_list.append("Pelle")
    if player_inventory.marteau: permanent_list.append("Marteau")
    if player_inventory.kit_crochetage: permanent_list.append("Kit de Crochetage")
    if player_inventory.detecteur_métaux: permanent_list.append("Détecteur de Métaux")
    if player_inventory.patte_lapin: permanent_list.append("Patte de Lapin")

    autres_list = ["Pas", "Pièces", "Gemmes", "Clés", "Dés"]

    # Déterminer la liste active et sa taille
    active_list = []
    if inventory_category_index == 0:
        active_list = consumable_list
    elif inventory_category_index == 1:
        active_list = permanent_list
    elif inventory_category_index == 2:
        active_list = autres_list
    
    active_list_len = len(active_list)


    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            
            # --- GESTION ECHAP ---
            if event.key == pygame.K_ESCAPE:
                if game_state == "selecting_room":
                    game_state = "moving"
                    current_room_selection = []
                    selected_direction = None
                
                elif game_state == "inventory":
                    if inventory_sub_state == "confirming_use":
                        inventory_sub_state = "context_menu" 
                    elif inventory_sub_state == "showing_info":
                        inventory_sub_state = "context_menu" 
                    elif inventory_sub_state == "context_menu":
                        inventory_sub_state = "browsing" 
                    else: # "browsing"
                        game_state = "moving" 
                
                else: # "moving"
                    running = False
            
            #  ÉTAT 1: LE JOUEUR SE DÉPLACE SUR LA GRILLE
            if game_state == "moving":
                
                if event.key == pygame.K_i:
                    game_state = "inventory"
                    inventory_selected_index = 0
                    inventory_category_index = 0 
                    inventory_sub_state = "browsing"
                    continue 

                # ... (logique ZQSD inchangée) ...
                if event.key == pygame.K_z: 
                    selected_direction = 'up'
                    target_x = player_x
                    target_y = max(0, player_y - 1) 
                elif event.key == pygame.K_s: 
                    selected_direction = 'down'
                    target_x = player_x
                    target_y = min(MANOR_HEIGHT - 1, player_y + 1)
                elif event.key == pygame.K_q: 
                    selected_direction = 'left'
                    target_x = max(0, player_x - 1)
                    target_y = player_y 
                elif event.key == pygame.K_d: 
                    selected_direction = 'right'
                    target_x = min(MANOR_WIDTH - 1, player_x + 1)
                    target_y = player_y
                
                # ... (logique Espace/Entrée inchangée) ...
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_direction is not None and (target_x != player_x or target_y != player_y):
                        
                        current_room = manor_grid[player_y][player_x]
                        current_doors = current_room.get_rotated_doors()
                        
                        has_exit = False
                        if selected_direction == 'up' and current_doors['north']: has_exit = True
                        elif selected_direction == 'down' and current_doors['south']: has_exit = True
                        elif selected_direction == 'left' and current_doors['west']: has_exit = True
                        elif selected_direction == 'right' and current_doors['east']: has_exit = True

                        if not has_exit:
                            feedback_message = "Il n'y a pas d'accès de ce côté"
                            feedback_message_time = pygame.time.get_ticks() + 2000
                            selected_direction = None 
                            target_x = player_x
                            target_y = player_y
                            continue 
                        
                        target_cell = manor_grid[target_y][target_x]
                        
                        if target_cell is None: 
                            current_room_selection = draw_three_rooms(main_deck, player_inventory.gemmes, manor_grid, target_x, target_y, player_x, player_y)
                            if current_room_selection: 
                                game_state = "selecting_room"
                            else:
                                feedback_message = "Aucune pièce ne peut aller ici !"
                                feedback_message_time = pygame.time.get_ticks() + 2000
                                selected_direction = None
                        
                        else:
                            target_doors = target_cell.get_rotated_doors()
                            has_entry = False
                            if selected_direction == 'up' and target_doors['south']: has_entry = True
                            elif selected_direction == 'down' and target_doors['north']: has_entry = True
                            elif selected_direction == 'left' and target_doors['east']: has_entry = True
                            elif selected_direction == 'right' and target_doors['west']: has_entry = True

                            if has_entry:
                                player_x = target_x
                                player_y = target_y
                                player_inventory.pas -= 1
                                target_cell.apply_every_entry_effect(None) 
                                selected_direction = None
                                target_x = player_x
                                target_y = player_y
                            else:
                                feedback_message = "Il n'y a pas d'accès de ce côté"
                                feedback_message_time = pygame.time.get_ticks() + 2000
                                selected_direction = None
                                target_x = player_x
                                target_y = player_y

                elif event.key not in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d, pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_i]:
                    selected_direction = None
                    target_x = player_x
                    target_y = player_y
            
            # ÉTAT 2: LE JOUEUR CHOISIT UNE PIÈCE
            elif game_state == "selecting_room":
                # ... (logique inchangée) ...
                choice = -1
                if event.key == pygame.K_q: choice = 0
                elif event.key == pygame.K_s: choice = 1
                elif event.key == pygame.K_d: choice = 2
                
                if 0 <= choice < len(current_room_selection):
                    chosen_room = current_room_selection[choice]
                    
                    if player_inventory.gemmes >= chosen_room.gem_cost:
                        player_inventory.gemmes -= chosen_room.gem_cost
                        chosen_room.rotation = chosen_room.valid_rotation[0]
                        manor_grid[target_y][target_x] = chosen_room
                        
                        if chosen_room in main_deck:
                            main_deck.remove(chosen_room)
                        
                        player_x = target_x
                        player_y = target_y
                        player_inventory.pas -= 1
                        chosen_room.apply_entry_effect(None) 
                        game_state = "moving"
                        current_room_selection = []
                        selected_direction = None
                        target_x = player_x
                        target_y = player_y
                    else:
                        feedback_message = "Pas assez de gemmes !"
                        feedback_message_time = pygame.time.get_ticks() + 2000
                
                elif event.key == pygame.K_BACKSPACE:
                    game_state = "moving"
                    current_room_selection = []
                    selected_direction = None

            # ÉTAT 3: LE JOUEUR EST DANS L'INVENTAIRE (Logique refaite)
            elif game_state == "inventory":
                
                if event.key == pygame.K_i:
                    game_state = "moving"
                    continue
                
                # SOUS-ÉTAT 1: Navigation principale
                if inventory_sub_state == "browsing":
                    if event.key == pygame.K_q: # Onglet gauche
                        inventory_category_index = (inventory_category_index - 1) % 3 
                        inventory_selected_index = 0 
                    elif event.key == pygame.K_d: # Onglet droit
                        inventory_category_index = (inventory_category_index + 1) % 3
                        inventory_selected_index = 0 
                    
                    # MODIFICATION: Navigation Z/S unifiée
                    elif event.key == pygame.K_z: # Haut
                        inventory_selected_index = (inventory_selected_index - 1) % active_list_len if active_list_len > 0 else 0
                    elif event.key == pygame.K_s: # Bas
                        inventory_selected_index = (inventory_selected_index + 1) % active_list_len if active_list_len > 0 else 0
                    
                    # MODIFICATION: Sélection (Entrée) unifiée
                    elif event.key == pygame.K_RETURN: 
                        if active_list_len > 0:
                            selected_item_name = active_list[inventory_selected_index]
                            inventory_sub_state = "context_menu"
                            context_menu_index = 0 # Toujours reset à 0
                
                # SOUS-ÉTAT 2: Menu contextuel (Utiliser, Infos, Retour)
                elif inventory_sub_state == "context_menu":
                    # Définir les options valides pour ce menu
                    if inventory_category_index == 0:
                        options = ["Utiliser", "Infos", "Retour"]
                    else:
                        options = ["Infos", "Retour"]
                    
                    max_index = len(options) - 1

                    if event.key == pygame.K_z: # Haut
                        context_menu_index = max(0, context_menu_index - 1)
                    elif event.key == pygame.K_s: # Bas
                        context_menu_index = min(max_index, context_menu_index + 1)
                    
                    elif event.key == pygame.K_RETURN:
                        selected_option = options[context_menu_index]
                        
                        if selected_option == "Utiliser":
                            inventory_sub_state = "confirming_use"
                            confirm_selected_index = 0 
                        elif selected_option == "Infos":
                            inventory_sub_state = "showing_info"
                        elif selected_option == "Retour":
                            inventory_sub_state = "browsing"

                # SOUS-ÉTAT 3: Confirmation d'utilisation
                elif inventory_sub_state == "confirming_use":
                    if event.key == pygame.K_z or event.key == pygame.K_q: 
                        confirm_selected_index = 0 
                    elif event.key == pygame.K_s or event.key == pygame.K_d: 
                        confirm_selected_index = 1 
                    
                    elif event.key == pygame.K_RETURN: 
                        if confirm_selected_index == 0: # "Confirmer"
                            player_inventory.utiliser_objet_consommable(selected_item_name)
                            inventory_sub_state = "browsing" # Retour à la liste
                            selected_item_name = None
                            # L'index sera recalculé au prochain tour de boucle
                        else: # "Annuler"
                            inventory_sub_state = "context_menu" 
                
                # SOUS-ÉTAT 4: Fenêtre d'infos
                elif inventory_sub_state == "showing_info":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        inventory_sub_state = "context_menu" 


    # Logique de fin de partie (défaite)
    if player_inventory.pas <= 0:
        # ... (inchangé) ...
        screen.fill(BLACK)
        font_large = pygame.font.Font(None, 100)
        perdu_text = font_large.render("Perdu !", True, RED)
        perdu_rect = perdu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(perdu_text, perdu_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        continue 

    # --- AFFICHAGE ---
    screen.fill(BLACK) 
    
    # ... (dessin grille, pièces, curseurs, hud, feedback, room_selection - tout inchangé) ...
    
    grid_total_width = MANOR_WIDTH * GRID_SIZE
    grid_total_height = MANOR_HEIGHT * GRID_SIZE
    start_x = (SCREEN_WIDTH - grid_total_width) // 2
    start_y = (SCREEN_HEIGHT - grid_total_height) // 2

    for x_idx in range(MANOR_WIDTH + 1):
        x_pos = start_x + x_idx * GRID_SIZE
        pygame.draw.line(screen, GRAY, (x_pos, start_y), (x_pos, start_y + grid_total_height))
    for y_idx in range(MANOR_HEIGHT + 1):
        y_pos = start_y + y_idx * GRID_SIZE
        pygame.draw.line(screen, GRAY, (start_x, y_pos), (start_x + grid_total_width, y_pos))

    for y_idx in range(MANOR_HEIGHT):
        for x_idx in range(MANOR_WIDTH):
            room = manor_grid[y_idx][x_idx]
            if room is not None:
                piece_rect = pygame.Rect(start_x + x_idx * GRID_SIZE, start_y + y_idx * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if room.image: 
                    scaled_image = pygame.transform.scale(room.image, (GRID_SIZE, GRID_SIZE))
                    rotated_image = pygame.transform.rotate(scaled_image, room.rotation * 90)
                    img_rect = rotated_image.get_rect(center = piece_rect.center)
                    screen.blit(rotated_image, img_rect)
                else: 
                    pygame.draw.rect(screen, (50, 50, 50), piece_rect)
                    room_name_text = ROOM_FONT.render(room.name, True, WHITE)
                    text_rect = room_name_text.get_rect(center=(piece_rect.centerx, piece_rect.centery))
                    screen.blit(room_name_text, text_rect)
    
    player_pixel_x = start_x + player_x * GRID_SIZE
    player_pixel_y = start_y + player_y * GRID_SIZE
    player_cursor = pygame.Rect(player_pixel_x, player_pixel_y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_cursor, 2)  

    if selected_direction is not None and game_state == "moving":
        target_pixel_x = start_x + target_x * GRID_SIZE
        target_pixel_y = start_y + target_y * GRID_SIZE
        target_cursor = pygame.Rect(target_pixel_x, target_pixel_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, SELECTION_COLOR, target_cursor, 2) 

    

    if feedback_message and pygame.time.get_ticks() < feedback_message_time:
        message_x = start_x + grid_total_width + 20 
        message_y = start_y + (grid_total_height // 2) 
        message_text = MENU_CARD_FONT.render(feedback_message, True, RED) 
        message_rect = message_text.get_rect(midleft=(message_x, message_y))
        screen.blit(message_text, message_rect)
    elif pygame.time.get_ticks() >= feedback_message_time:
        feedback_message = "" 

    if game_state == "selecting_room":
        num_cards = len(current_room_selection)
        total_cards_width = (num_cards * CARD_IMAGE_SIZE) + ((num_cards - 1) * CARD_PADDING)
        start_menu_x = (SCREEN_WIDTH - total_cards_width) // 2
        y_pos_image = (SCREEN_HEIGHT - CARD_IMAGE_SIZE) // 2
        keys_to_show = ['Q', 'S', 'D']
        for i, room in enumerate(current_room_selection):
            x_pos = start_menu_x + i * (CARD_IMAGE_SIZE + CARD_PADDING) 
            display_rotation = 0
            if room.valid_rotations: display_rotation = room.valid_rotations[0]
            if room.image:
                img = pygame.transform.scale(room.image, (CARD_IMAGE_SIZE, CARD_IMAGE_SIZE))
                rotated_img = pygame.transform.rotate(img, display_rotation * 90)
                img_rect = rotated_img.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE // 2))
                screen.blit(rotated_img, img_rect.topleft)
            else: 
                pygame.draw.rect(screen, GRAY, (x_pos, y_pos_image, CARD_IMAGE_SIZE, CARD_IMAGE_SIZE))
            name_text = MENU_CARD_FONT.render(room.name, True, WHITE)
            name_rect = name_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE + 30))
            screen.blit(name_text, name_rect)
            gem_color = WHITE if player_inventory.gemmes >= room.gem_cost else RED
            gem_text_str = f"Coût: {room.gem_cost} Gemmes"
            gem_text = MENU_CARD_FONT.render(gem_text_str, True, gem_color)
            gem_rect = gem_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image + CARD_IMAGE_SIZE + 55))
            screen.blit(gem_text, gem_rect)
            if i < len(keys_to_show):
                key_text = MENU_KEY_FONT.render(keys_to_show[i], True, BLACK)
                key_bg_rect = key_text.get_rect(center=(x_pos + CARD_IMAGE_SIZE // 2, y_pos_image - 40))
                key_bg_rect.inflate_ip(10, 10) 
                pygame.draw.rect(screen, WHITE, key_bg_rect, border_radius=5)
                screen.blit(key_text, key_text.get_rect(center=key_bg_rect.center))
    
    # MODIFICATION: L'appel envoie maintenant tous les nouveaux états
    if game_state == "inventory":
        draw_inventory_ui(screen, player_inventory, 
                          inventory_category_index, 
                          inventory_selected_index, 
                          inventory_sub_state, 
                          selected_item_name,
                          context_menu_index, 
                          confirm_selected_index)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()