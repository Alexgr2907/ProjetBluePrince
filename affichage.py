import pygame
from rooms import *
import random
from rooms_manager import create_initial_deck, draw_three_rooms
from inventaire import Inventaire
import objet
import rooms_manager
#  Initialisation de Pygame 
pygame.init()

#  Constantes du jeu 
MANOR_WIDTH = 5
MANOR_HEIGHT = 9

# --- MODIFIÉ : Configuration de la fenêtre et Tailles Dynamiques ---
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
pygame.display.set_caption("Projet Blue Prince (simplifié)")

# NOUVEAU: GRID_SIZE est maintenant calculé !
GRID_SIZE = (SCREEN_HEIGHT - 20) // MANOR_HEIGHT 
SIDEBAR_WIDTH = SCREEN_WIDTH // 4 

# NOUVEAU: Ajout d'une barre à droite pour équilibrer
RIGHT_BAR_WIDTH = SIDEBAR_WIDTH

# Couleurs 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40) 
PLAYER_COLOR = (255, 0, 0)
RED = (255, 0, 0)
SELECTION_COLOR = (255, 255, 255)
UI_BLUE_DARK = (10, 20, 40)
UI_BLUE_LIGHT = (30, 50, 80)
UI_HIGHLIGHT = (255, 255, 0)


# MODIFIÉ: Polices dynamiques (basées sur GRID_SIZE)
ROOM_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.22)) 
MENU_TITLE_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.75)) 
MENU_CARD_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.3))  
MENU_KEY_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.5))   

INV_TITLE_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.6)) 
INV_ITEM_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.4)) 
INV_CONFIRM_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.35)) 
INV_TAB_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.3)) 

HUD_TITLE_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.5)) 
HUD_SUBTITLE_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.375)) 
HUD_ITEM_FONT = pygame.font.Font(None, int(GRID_SIZE * 0.325)) 


# On crée un "catalogue" pour lier les noms d'objets à leurs descriptions
ITEM_CATALOG = {
    "Oeuf d'araignée": objet.Pomme(),
    "Araignée": objet.Banane(),
    "Coléoptère adulte": objet.Gateau(),
    "Punaise": objet.Sandwich(),
    "Nid de sauterelle": objet.Repas(),
    "Pelle": objet.Pelle(),
    "Marteau": objet.Marteau(),
    "Kit de Crochetage": objet.KitCrochetage(),
    "Détecteur de Métaux": objet.DetecteurMetaux(),
    "Patte de Lapin": objet.PatteLapin(),
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

# MODIFIÉ: Tailles dynamiques pour le menu de sélection
CARD_IMAGE_SIZE = int(GRID_SIZE * 2.5) 
CARD_PADDING = int(GRID_SIZE * 0.75)     

# --- Fonctions d'Affichage ---

def dessiner_texte_multi_lignes(surface, texte, police, couleur, rect):
    """
    Dessine une chaîne de caractères sur plusieurs lignes ("text wrapping")
    pour qu'elle s'adapte à la largeur d'un rectangle donné.
    """
    mots = texte.split(' ')
    lignes = []
    ligne_actuelle = ""
    for mot in mots:
        ligne_test = ligne_actuelle + mot + " "
        if police.size(ligne_test)[0] < rect.width:
            ligne_actuelle = ligne_test
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot + " "
    lignes.append(ligne_actuelle)
    
    y = rect.top
    for ligne in lignes:
        surface_ligne = police.render(ligne, True, couleur)
        surface.blit(surface_ligne, (rect.left, y))
        y += police.get_linesize()

def dessiner_interface_inventaire(screen, inventaire, index_categorie, index_selection, sous_etat, nom_objet_selectionne, index_menu_contextuel, index_confirmation):
    """
    Dessine l'interface complète de l'inventaire (touche 'I').
    """
    
    # Dimensions de l'interface
    ui_width = SCREEN_WIDTH * 0.7
    ui_height = SCREEN_HEIGHT * 0.8
    ui_x = (SCREEN_WIDTH - ui_width) / 2
    ui_y = (SCREEN_HEIGHT - ui_height) / 2
    ui_rect = pygame.Rect(ui_x, ui_y, ui_width, ui_height)
    
    pygame.draw.rect(screen, UI_BLUE_DARK, ui_rect, border_radius=15)
    pygame.draw.rect(screen, UI_BLUE_LIGHT, ui_rect, width=5, border_radius=15)
    
    title_text = INV_TITLE_FONT.render("Inventaire", True, WHITE)
    title_rect = title_text.get_rect(center=(ui_rect.centerx, ui_y + 40))
    screen.blit(title_text, title_rect)
    
    categories_onglets = ["Consommables", "Permanents", "Autres"]
    tab_width = ui_width / len(categories_onglets)
    tab_y = ui_y + 80
    
    for i, nom_onglet in enumerate(categories_onglets):
        tab_rect = pygame.Rect(ui_x + i * tab_width, tab_y, tab_width, 40)
        
        if i == index_categorie:
            pygame.draw.rect(screen, UI_BLUE_LIGHT, tab_rect, border_top_left_radius=8, border_top_right_radius=8)
            color = UI_HIGHLIGHT
        else:
            color = GRAY
            pygame.draw.line(screen, UI_BLUE_LIGHT, (tab_rect.left, tab_rect.bottom - 1), (tab_rect.right, tab_rect.bottom - 1), 2)

        tab_text = INV_TAB_FONT.render(nom_onglet, True, color)
        tab_text_rect = tab_text.get_rect(center=tab_rect.center)
        screen.blit(tab_text, tab_text_rect)
    
    item_y_start = tab_y + 60
    
    item_line_height = INV_ITEM_FONT.get_linesize() + int(GRID_SIZE * 0.1)

    # --- ONGLET 0: CONSOMMABLES ---
    if index_categorie == 0:
        liste_consommables = list(inventaire.objets.items())
        
        if not liste_consommables:
            empty_text = INV_ITEM_FONT.render("Aucun objet consommable.", True, GRAY)
            empty_rect = empty_text.get_rect(center=(ui_rect.centerx, ui_rect.centery))
            screen.blit(empty_text, empty_rect)
        else:
            for i, (item_name, quantity) in enumerate(liste_consommables):
                item_text_str = f"{item_name} x{quantity}"
                color = UI_HIGHLIGHT if i == index_selection else WHITE
                item_text = INV_ITEM_FONT.render(item_text_str, True, color)
                item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * item_line_height))
                screen.blit(item_text, item_rect)
                
                if i == index_selection:
                    color_cercle = UI_HIGHLIGHT if sous_etat == "navigation" else WHITE
                    pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- ONGLET 1: PERMANENTS ---
    elif index_categorie == 1:
        liste_permanents = []
        if inventaire.pelle: liste_permanents.append("Pelle")
        if inventaire.marteau: liste_permanents.append("Marteau")
        if inventaire.kit_crochetage: liste_permanents.append("Kit de Crochetage")
        if inventaire.detecteur_métaux: liste_permanents.append("Détecteur de Métaux")
        if inventaire.patte_lapin: liste_permanents.append("Patte de Lapin")
        
        if not liste_permanents:
            empty_text = INV_ITEM_FONT.render("Aucun objet permanent.", True, GRAY)
            empty_rect = empty_text.get_rect(center=(ui_rect.centerx, ui_rect.centery))
            screen.blit(empty_text, empty_rect)
        else:
            for i, item_name in enumerate(liste_permanents):
                item_text_str = item_name
                color = UI_HIGHLIGHT if i == index_selection else WHITE
                item_text = INV_ITEM_FONT.render(item_text_str, True, color)
                item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * item_line_height))
                screen.blit(item_text, item_rect)
                
                if i == index_selection:
                    color_cercle = UI_HIGHLIGHT if sous_etat == "navigation" else WHITE
                    pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- ONGLET 2: AUTRES ---
    elif index_categorie == 2:
        liste_autres_affichage = [
            f"Pas : {inventaire.pas}",
            f"Pièces : {inventaire.pieces}",
            f"Gemmes : {inventaire.gemmes}",
            f"Clés : {inventaire.cles}",
            f"Dés : {inventaire.des}"
        ]
        
        for i, item_str in enumerate(liste_autres_affichage):
            color = UI_HIGHLIGHT if i == index_selection else WHITE
            item_text = INV_ITEM_FONT.render(item_str, True, color)
            item_rect = item_text.get_rect(midleft=(ui_x + 40, item_y_start + i * item_line_height))
            screen.blit(item_text, item_rect)

            if i == index_selection:
                color_cercle = UI_HIGHLIGHT if sous_etat == "navigation" else WHITE
                pygame.draw.circle(screen, color_cercle, (ui_x + 25, item_rect.centery), 5)

    # --- POP-UP : MENU CONTEXTUEL (Dynamique) ---
    if sous_etat == "menu_contextuel":
        
        font_util = INV_CONFIRM_FONT
        padding = int(GRID_SIZE * 0.25) 
        line_height = font_util.get_linesize()

        if index_categorie == 0:
            options_menu = ["Utiliser", "Infos", "Retour"]
        else:
            options_menu = ["Infos", "Retour"]
        
        ctx_width = int(GRID_SIZE * 2.5) 
        ctx_height = (len(options_menu) * line_height) + (padding * 2)
            
        selected_item_y = item_y_start + index_selection * item_line_height
        
        # CORRECTION: Position X dynamique (40% de la largeur)
        ctx_x = ui_x + (ui_width * 0.4) 
        
        ctx_y = max(ui_y + 120, min(selected_item_y, (ui_y + ui_height) - ctx_height - 20))
        
        ctx_rect = pygame.Rect(ctx_x, ctx_y, ctx_width, ctx_height)
        pygame.draw.rect(screen, BLACK, ctx_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, ctx_rect, width=2, border_radius=10)

        for i, option in enumerate(options_menu):
            color = UI_HIGHLIGHT if i == index_menu_contextuel else WHITE
            option_text = font_util.render(option, True, color)
            # CORRECTION: Ajustement du padding
            option_rect = option_text.get_rect(midleft=(ctx_x + padding, ctx_y + (padding // 2) + (line_height // 2) + (i * line_height)))
            screen.blit(option_text, option_rect)

    # --- POP-UP : CONFIRMATION D'UTILISATION ---
    elif sous_etat == "confirmation_utilisation" and nom_objet_selectionne:
        
        # CORRECTION: Tailles et positions dynamiques
        confirm_width = int(GRID_SIZE * 6)
        confirm_height = int(GRID_SIZE * 2)
        confirm_x = (SCREEN_WIDTH - confirm_width) / 2
        confirm_y = (SCREEN_HEIGHT - confirm_height) / 2
        confirm_rect = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)
        
        pygame.draw.rect(screen, BLACK, confirm_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, confirm_rect, width=3, border_radius=10)
        
        question_str = f"Voulez-vous utiliser 1 {nom_objet_selectionne} ?"
        question_text = INV_CONFIRM_FONT.render(question_str, True, WHITE)
        # Position dynamique
        question_rect = question_text.get_rect(center=(confirm_rect.centerx, confirm_y + (confirm_height * 0.25)))
        screen.blit(question_text, question_rect)
        
        confirm_btn_text_str = "Confirmer (Entrée)"
        cancel_btn_text_str = "Annuler (Echap)"
        
        confirm_color = UI_HIGHLIGHT if index_confirmation == 0 else GRAY
        cancel_color = UI_HIGHLIGHT if index_confirmation == 1 else GRAY
        
        confirm_btn_text = INV_CONFIRM_FONT.render(confirm_btn_text_str, True, confirm_color)
        cancel_btn_text = INV_CONFIRM_FONT.render(cancel_btn_text_str, True, cancel_color)
        
        # Position dynamique
        btn_y_pos = confirm_y + (confirm_height * 0.7)
        btn_x_offset = confirm_width * 0.25 
        
        confirm_btn_rect = confirm_btn_text.get_rect(center=(confirm_rect.centerx - btn_x_offset, btn_y_pos))
        cancel_btn_rect = cancel_btn_text.get_rect(center=(confirm_rect.centerx + btn_x_offset, btn_y_pos))
        
        screen.blit(confirm_btn_text, confirm_btn_rect)
        screen.blit(cancel_btn_text, cancel_btn_rect)
    
    # --- POP-UP : INFO OBJET ---
    elif sous_etat == "affichage_info":
        # ... (inchangé) ...
        info_width = 400
        info_height = 200 
        info_x = (SCREEN_WIDTH - info_width) / 2
        info_y = (SCREEN_HEIGHT - info_height) / 2
        info_rect = pygame.Rect(info_x, info_y, info_width, info_height)
        
        pygame.draw.rect(screen, BLACK, info_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, info_rect, width=3, border_radius=10)
        
        title_str = nom_objet_selectionne
        title_text = INV_CONFIRM_FONT.render(title_str, True, UI_HIGHLIGHT)
        title_rect = title_text.get_rect(center=(info_rect.centerx, info_y + 30))
        screen.blit(title_text, title_rect)

        info_str = "Aucune info pour le moment." 
        if nom_objet_selectionne in ITEM_CATALOG:
            info_str = ITEM_CATALOG[nom_objet_selectionne].description
        
        text_rect = pygame.Rect(info_x + 20, info_y + 60, info_width - 40, info_height - 90)
        dessiner_texte_multi_lignes(screen, info_str, INV_TAB_FONT, WHITE, text_rect)

        close_str = "Appuyez sur Entrée ou Echap pour fermer"
        close_text = INV_TAB_FONT.render(close_str, True, GRAY) 
        close_rect = close_text.get_rect(center=(info_rect.centerx, info_y + info_height - 30))
        screen.blit(close_text, close_rect)


# --- INITIALISATION DU JEU ---

# Créer la grille du manoir
grille_manoir = [[None for _ in range(MANOR_WIDTH)] for _ in range(MANOR_HEIGHT)]

# Position du joueur
player_x = 2
player_y = 8

# Place la salle de départ 
salle_depart = Horror_Hall() 
grille_manoir[player_y][player_x] = salle_depart 

# Modif Alex Salle de fin (exit)
salle_final = Exit()
grille_manoir[0][2] = salle_final

# Sélection de la cible
target_x = player_x
target_y = player_y
selected_direction = None

# Instance de l'inventaire
inventaire_joueur = Inventaire()
# Ligne de triche pour tester
# inventaire_joueur.objets["Oeuf d'araignée"] = 3 
# inventaire_joueur.objets["Araignée"] = 1 


# Deck de pièces
pioche_principale = create_initial_deck()

# GESTION D'ÉTAT 
en_cours = True
etat_du_jeu = "deplacement" 
selection_salle_actuelle = [] 

# Variables pour l'état de l'inventaire
index_selection_inv = 0
index_categorie_inv = 0 
sous_etat_inv = "navigation" 
nom_objet_selectionne = None 
index_menu_contextuel = 0 
index_confirmation = 0 

# Variables pour les messages feedback 
message_feedback = ""
temps_message_feedback = 0
message_queue = []

# --- BOUCLE DE JEU PRINCIPALE ---
while en_cours:
    # --- Définir les listes actuelles pour la navigation ---
    liste_consommables = list(inventaire_joueur.objets.keys())
    
    liste_permanents = []
    if inventaire_joueur.pelle: liste_permanents.append("Pelle")
    if inventaire_joueur.marteau: liste_permanents.append("Marteau")
    if inventaire_joueur.kit_crochetage: liste_permanents.append("Kit de Crochetage")
    if inventaire_joueur.detecteur_métaux: liste_permanents.append("Détecteur de Métaux")
    if inventaire_joueur.patte_lapin: liste_permanents.append("Patte de Lapin")

    liste_autres = ["Pas", "Pièces", "Gemmes", "Clés", "Dés"]

    liste_active = []
    if index_categorie_inv == 0:
        liste_active = liste_consommables
    elif index_categorie_inv == 1:
        liste_active = liste_permanents
    elif index_categorie_inv == 2:
        liste_active = liste_autres
    
    longueur_liste_active = len(liste_active)


    # Gestion des événements
    for event in pygame.event.get():

        #---- GESTION FILE D'ATTENTE MESSAGE--------
        current_time = pygame.time.get_ticks()

        if current_time > temps_message_feedback and message_queue:
            message_feedback = message_queue.pop(0)
            temps_message_feedback = current_time + 3000

        if event.type == pygame.QUIT:
            en_cours = False
        
        if event.type == pygame.KEYDOWN:
            
            # --- GESTION ECHAP ---
            if event.key == pygame.K_ESCAPE:
                if etat_du_jeu == "selection_salle":
                    etat_du_jeu = "deplacement"
                    selection_salle_actuelle = []
                    selected_direction = None
                
                elif etat_du_jeu == "inventaire":
                    if sous_etat_inv == "confirmation_utilisation":
                        sous_etat_inv = "menu_contextuel" 
                    elif sous_etat_inv == "affichage_info":
                        sous_etat_inv = "menu_contextuel" 
                    elif sous_etat_inv == "menu_contextuel":
                        sous_etat_inv = "navigation" 
                    else: 
                        etat_du_jeu = "deplacement" 
                
                else: 
                    en_cours = False
            
            #  ÉTAT 1: LE JOUEUR SE DÉPLACE SUR LA GRILLE
            if etat_du_jeu == "deplacement":
                
                if event.key == pygame.K_i:
                    etat_du_jeu = "inventaire"
                    index_selection_inv = 0
                    index_categorie_inv = 0 
                    sous_etat_inv = "navigation"
                    continue 
                
                # Logique pour creuser (C)
                if event.key == pygame.K_c: 
                    current_room = grille_manoir[player_y][player_x] 
                    if current_room and current_room.dig_spot:
                        if inventaire_joueur.pelle:
                            butin = rooms_manager.pioche_butin_creuser()
                            current_room.dig_spot = False

                            if butin :
                                inventaire_joueur.ramasser_objet(butin)
                                message_feedback = f"Vous creusez et trouvez un {butin.nom}!"
                            else :
                                message_feedback = "Vous n'avez rien trouver"

                            temps_message_feedback = pygame.time.get_ticks() + 3000
                        
                        else :
                            message_feedback = "Il y a un endroit à creuser, mais il vous manque une Pelle ! "
                            temps_message_feedback = pygame.time.get_ticks() + 3000
                    
                    continue

                # ... (logique de sélection et validation ZQSD inchangée) ...
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
                
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if selected_direction is not None and (target_x != player_x or target_y != player_y):
                        
                        current_room = grille_manoir[player_y][player_x]
                        current_doors = current_room.get_rotated_doors()
                        
                        has_exit = False
                        if selected_direction == 'up' and current_doors['north']: has_exit = True
                        elif selected_direction == 'down' and current_doors['south']: has_exit = True
                        elif selected_direction == 'left' and current_doors['west']: has_exit = True
                        elif selected_direction == 'right' and current_doors['east']: has_exit = True

                        if not has_exit:
                            message_feedback = "Il n'y a pas d'accès de ce côté"
                            temps_message_feedback = pygame.time.get_ticks() + 2000
                            selected_direction = None 
                            target_x = player_x
                            target_y = player_y
                            continue 
                        
                        target_cell = grille_manoir[target_y][target_x]
                        
                        if target_cell is None: 
                            selection_salle_actuelle = draw_three_rooms(pioche_principale, inventaire_joueur.gemmes, grille_manoir, target_x, target_y, player_x, player_y)
                            if selection_salle_actuelle: 
                                etat_du_jeu = "selection_salle"
                            else:
                                message_feedback = "Aucune pièce ne peut aller ici !"
                                temps_message_feedback = pygame.time.get_ticks() + 2000
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
                                inventaire_joueur.pas -= 1

                                if target_cell is salle_final:
                                    etat_du_jeu = "gagne"
                                    continue # On saute le reste de la boucle

                                msg = target_cell.apply_every_entry_effect(inventaire_joueur, grille_manoir) 

                                if msg: 
                                    message_queue.append(msg)

                                    if not message_feedback: 
                                        message_feedback = message_queue.pop(0)
                                        temps_message_feedback = pygame.time.get_ticks() + 3000

                                selected_direction = None
                                target_x = player_x
                                target_y = player_y
                            else:
                                message_feedback = "Il n'y a pas d'accès de ce côté"
                                temps_message_feedback = pygame.time.get_ticks() + 2000
                                selected_direction = None
                                target_x = player_x
                                target_y = player_y

                elif event.key not in [pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d, pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_i, pygame.K_c]:
                    selected_direction = None
                    target_x = player_x
                    target_y = player_y
            
            # ÉTAT 2: LE JOUEUR CHOISIT UNE PIÈCE
            elif etat_du_jeu == "selection_salle":
                choice = -1
                if event.key == pygame.K_q: choice = 0
                elif event.key == pygame.K_s: choice = 1
                elif event.key == pygame.K_d: choice = 2
                
                if 0 <= choice < len(selection_salle_actuelle):
                    chosen_room = selection_salle_actuelle[choice]
                    
                    if inventaire_joueur.gemmes >= chosen_room.gem_cost:
                        inventaire_joueur.gemmes -= chosen_room.gem_cost
                        chosen_room.rotation = chosen_room.valid_rotations[0]
                        grille_manoir[target_y][target_x] = chosen_room

                        room_entry_messages = []
                        
                        if chosen_room.First_time:
                            if random.random() < 1.0 :  
                                chosen_room.dig_spot = True
                                print(f"Un endroit à creuser a été marqué dans la {chosen_room.name}.")

                            objet_rammase = rooms_manager.pioche_aleatoire_objet(taux_drop=1.0)
                            if objet_rammase:
                                if inventaire_joueur.ramasser_objet(objet_rammase):
                                    print(f"Un {objet_rammase.nom} a été ramassé et ajouté à l'inventaire. ")
                                    room_entry_messages.append(f"Un {objet_rammase.nom} est apparu et a été ramassé !")
                                    temps_message_feedback = pygame.time.get_ticks() + 3000

                        msg_entry = chosen_room.apply_entry_effect(inventaire_joueur, grille_manoir)
                        if msg_entry :
                            room_entry_messages.append(msg_entry)

                        msg_every= chosen_room.apply_every_entry_effect(inventaire_joueur, grille_manoir)
                        if msg_every:
                            room_entry_messages.append(msg_every)

                        if room_entry_messages :
                            message_feedback = room_entry_messages.pop(0)
                            temps_message_feedback = pygame.time.get_ticks() + 3000
                            message_queue.extend(room_entry_messages)
                        
                        if chosen_room in pioche_principale:
                            pioche_principale.remove(chosen_room)
                        
                        player_x = target_x
                        player_y = target_y
                        inventaire_joueur.pas -= 1
                        
                        etat_du_jeu = "deplacement"
                        selection_salle_actuelle = []
                        selected_direction = None
                        target_x = player_x
                        target_y = player_y
                    else:
                        message_feedback = "Pas assez de gemmes !"
                        temps_message_feedback = pygame.time.get_ticks() + 2000
                
                elif event.key == pygame.K_BACKSPACE:
                    etat_du_jeu = "deplacement"
                    selection_salle_actuelle = []
                    selected_direction = None

            # ÉTAT 3: LE JOUEUR EST DANS L'INVENTAIRE
            elif etat_du_jeu == "inventaire":
                if event.key == pygame.K_i:
                    etat_du_jeu = "deplacement"
                    continue
                
                if sous_etat_inv == "navigation":
                    if event.key == pygame.K_q: 
                        index_categorie_inv = (index_categorie_inv - 1) % 3 
                        index_selection_inv = 0 
                    elif event.key == pygame.K_d: 
                        index_categorie_inv = (index_categorie_inv + 1) % 3
                        index_selection_inv = 0 
                    
                    elif event.key == pygame.K_z: 
                        index_selection_inv = (index_selection_inv - 1) % longueur_liste_active if longueur_liste_active > 0 else 0
                    elif event.key == pygame.K_s: 
                        index_selection_inv = (index_selection_inv + 1) % longueur_liste_active if longueur_liste_active > 0 else 0
                    
                    elif event.key == pygame.K_RETURN: 
                        if longueur_liste_active > 0:
                            nom_objet_selectionne = liste_active[index_selection_inv]
                            sous_etat_inv = "menu_contextuel"
                            index_menu_contextuel = 0 
                
                elif sous_etat_inv == "menu_contextuel":
                    if index_categorie_inv == 0:
                        options_menu = ["Utiliser", "Infos", "Retour"]
                    else:
                        options_menu = ["Infos", "Retour"]
                    
                    max_index = len(options_menu) - 1

                    if event.key == pygame.K_z: 
                        index_menu_contextuel = max(0, index_menu_contextuel - 1)
                    elif event.key == pygame.K_s: 
                        index_menu_contextuel = min(max_index, index_menu_contextuel + 1)
                    
                    elif event.key == pygame.K_RETURN:
                        selected_option = options_menu[index_menu_contextuel]
                        
                        if selected_option == "Utiliser":
                            sous_etat_inv = "confirmation_utilisation"
                            index_confirmation = 0 
                        elif selected_option == "Infos":
                            sous_etat_inv = "affichage_info"
                        elif selected_option == "Retour":
                            sous_etat_inv = "navigation"

                elif sous_etat_inv == "confirmation_utilisation":
                    if event.key == pygame.K_z or event.key == pygame.K_q: 
                        index_confirmation = 0 
                    elif event.key == pygame.K_s or event.key == pygame.K_d: 
                        index_confirmation = 1 
                    
                    elif event.key == pygame.K_RETURN: 
                        if index_confirmation == 0: 
                            inventaire_joueur.utiliser_objet_consommable(nom_objet_selectionne)
                            sous_etat_inv = "navigation" 
                            nom_objet_selectionne = None
                        else: 
                            sous_etat_inv = "menu_contextuel" 
                
                elif sous_etat_inv == "affichage_info":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        sous_etat_inv = "menu_contextuel" 
                
    # Logique de fin de partie (défaite)
    if inventaire_joueur.pas <= 0:
        screen.fill(BLACK)
        font_large = pygame.font.Font(None, 100)
        perdu_text = font_large.render("Perdu !", True, RED)
        perdu_rect = perdu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(perdu_text, perdu_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        en_cours = False
        continue 
    # logique fin du jeu : victoire   
    if etat_du_jeu == "gagne":

        screen.fill(UI_BLUE_DARK) # Fond noir

        # On utilise une police de titre pour le message
        win_text = MENU_TITLE_FONT.render("Vous avez réussi à vous échapper !", True, WHITE)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(win_text, win_rect)

        pygame.display.flip()
        pygame.time.wait(5000) # Attend 3 secondes
        en_cours = False # Arrête le jeu
        continue # Saute le reste de l'affichage


    # --- AFFICHAGE ---
    screen.fill(BLACK) 

    # --- DESSIN DE LA BARRE LATERALE (HUD) ---
    sidebar_rect = pygame.Rect(0, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, sidebar_rect)
    
    current_y = 30 
    
    title_text = HUD_TITLE_FONT.render("Inventaire (I)", True, WHITE)
    title_rect = title_text.get_rect(center=(SIDEBAR_WIDTH // 2, current_y))
    screen.blit(title_text, title_rect)
    
    current_y += 50
    
    # --- Section Consommables ---
    subtitle_text = HUD_SUBTITLE_FONT.render("Consommables :", True, UI_HIGHLIGHT)
    screen.blit(subtitle_text, (20, current_y))
    current_y += 35
    
    if not inventaire_joueur.objets:
        item_text = HUD_ITEM_FONT.render("  (Vide)", True, GRAY)
        screen.blit(item_text, (30, current_y))
        current_y += 30
    else:
        for item_name in liste_consommables:
            quantity = inventaire_joueur.objets[item_name]
            item_str = f"  - {item_name} x{quantity}"
            item_text = HUD_ITEM_FONT.render(item_str, True, WHITE)
            screen.blit(item_text, (30, current_y))
            current_y += 30
    
    current_y += 20 
    
    # --- Section Permanents ---
    subtitle_text = HUD_SUBTITLE_FONT.render("Items permanents :", True, UI_HIGHLIGHT)
    screen.blit(subtitle_text, (20, current_y))
    current_y += 35
    
    if not liste_permanents:
        item_text = HUD_ITEM_FONT.render("  (Aucun)", True, GRAY)
        screen.blit(item_text, (30, current_y))
        current_y += 30
    else:
        for item_name in liste_permanents:
            item_str = f"  - {item_name}"
            item_text = HUD_ITEM_FONT.render(item_str, True, WHITE)
            screen.blit(item_text, (30, current_y))
            current_y += 30
            
    current_y += 20 
    
    # --- Section Autres ---
    subtitle_text = HUD_SUBTITLE_FONT.render("Autres :", True, UI_HIGHLIGHT)
    screen.blit(subtitle_text, (20, current_y))
    current_y += 35
    
    autres_items = [
        f"  - Pas : {inventaire_joueur.pas}",
        f"  - Pièces : {inventaire_joueur.pieces}",
        f"  - Gemmes : {inventaire_joueur.gemmes}",
        f"  - Clés : {inventaire_joueur.cles}",
        f"  - Dés : {inventaire_joueur.des}"
    ]
    
    for item_str in autres_items:
        item_text = HUD_ITEM_FONT.render(item_str, True, WHITE)
        screen.blit(item_text, (30, current_y))
        current_y += 30
        
    # --- FIN DE LA BARRE LATERALE ---

    
    # MODIFIÉ: Calcul du décalage pour centrer la grille
    game_area_width = SCREEN_WIDTH - SIDEBAR_WIDTH - RIGHT_BAR_WIDTH
    grid_total_width = MANOR_WIDTH * GRID_SIZE
    grid_total_height = MANOR_HEIGHT * GRID_SIZE
    
    start_x = SIDEBAR_WIDTH + (game_area_width - grid_total_width) // 2
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
            room = grille_manoir[y_idx][x_idx]
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
    
    # Dessine le curseur du JOUEUR
    player_pixel_x = start_x + player_x * GRID_SIZE
    player_pixel_y = start_y + player_y * GRID_SIZE
    player_cursor = pygame.Rect(player_pixel_x, player_pixel_y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_cursor, 2)  

    # Dessine le curseur de SÉLECTION
    if selected_direction is not None and etat_du_jeu == "deplacement":
        target_pixel_x = start_x + target_x * GRID_SIZE
        target_pixel_y = start_y + target_y * GRID_SIZE
        target_cursor = pygame.Rect(target_pixel_x, target_pixel_y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, SELECTION_COLOR, target_cursor, 2) 

    # --- CORRECTION: AFFICHER LE MESSAGE FEEDBACK ---
    if message_feedback and pygame.time.get_ticks() < temps_message_feedback:
        # Crée un rectangle AU-DESSUS de la grille pour le texte
        message_box_width = grid_total_width
        message_box_height = int(GRID_SIZE * 1.2) 
        message_rect_x = start_x
        message_rect_y = start_y - message_box_height - int(GRID_SIZE * 0.1) 
        
        if message_rect_y < 10:
            message_rect_y = 10
        
        message_rect = pygame.Rect(message_rect_x, message_rect_y, message_box_width, message_box_height)
        
        dessiner_texte_multi_lignes(screen, message_feedback, MENU_CARD_FONT, RED, message_rect)
        
    elif pygame.time.get_ticks() >= temps_message_feedback:
        message_feedback = "" 

    # --- CORRECTION: DESSINER LE MENU DE SÉLECTION DE PIÈCE ---
    if etat_du_jeu == "selection_salle":
        
        # Calcule la zone à droite
        right_area_x_start = SCREEN_WIDTH - RIGHT_BAR_WIDTH
        right_area_width = RIGHT_BAR_WIDTH
        
        x_pos_center = right_area_x_start + (right_area_width // 2)
        
        num_cards = len(selection_salle_actuelle)
        
        total_cards_height = (num_cards * CARD_IMAGE_SIZE) + ((num_cards - 1) * CARD_PADDING)
        
        # MODIFIÉ: Centre le bloc de cartes verticalement sur l'ÉCRAN
        start_menu_y = (SCREEN_HEIGHT - total_cards_height) // 2
        
        keys_to_show = ['Q', 'S', 'D']
        
        for i, room in enumerate(selection_salle_actuelle):
            y_pos = start_menu_y + i * (CARD_IMAGE_SIZE + CARD_PADDING) 
            
            display_rotation = 0
            if room.valid_rotations: display_rotation = room.valid_rotations[0]
            
            if room.image:
                img = pygame.transform.scale(room.image, (CARD_IMAGE_SIZE, CARD_IMAGE_SIZE))
                rotated_img = pygame.transform.rotate(img, display_rotation * 90)
                img_rect = rotated_img.get_rect(center=(x_pos_center, y_pos + CARD_IMAGE_SIZE // 2))
                screen.blit(rotated_img, img_rect.topleft)
            else: 
                fallback_rect = pygame.Rect(0, 0, CARD_IMAGE_SIZE, CARD_IMAGE_SIZE)
                fallback_rect.center = (x_pos_center, y_pos + CARD_IMAGE_SIZE // 2)
                pygame.draw.rect(screen, GRAY, fallback_rect)

            name_text = MENU_CARD_FONT.render(room.name, True, WHITE)
            name_rect = name_text.get_rect(center=(x_pos_center, y_pos + CARD_IMAGE_SIZE + 30))
            screen.blit(name_text, name_rect)

            gem_color = WHITE if inventaire_joueur.gemmes >= room.gem_cost else RED
            gem_text_str = f"Coût: {room.gem_cost} Gemmes"
            gem_text = MENU_CARD_FONT.render(gem_text_str, True, gem_color)
            gem_rect = gem_text.get_rect(center=(x_pos_center, y_pos + CARD_IMAGE_SIZE + 55))
            screen.blit(gem_text, gem_rect)

            if i < len(keys_to_show):
                key_text = MENU_KEY_FONT.render(keys_to_show[i], True, BLACK)
                key_bg_rect = key_text.get_rect(center=(x_pos_center - (CARD_IMAGE_SIZE // 2) - (GRID_SIZE * 0.5), y_pos + CARD_IMAGE_SIZE // 2)) 
                key_bg_rect.inflate_ip(10, 10) 
                pygame.draw.rect(screen, WHITE, key_bg_rect, border_radius=5)
                screen.blit(key_text, key_text.get_rect(center=key_bg_rect.center))
    
    # DESSINER L'INTERFACE DE L'INVENTAIRE (Plein écran 'I')
    if etat_du_jeu == "inventaire":
        dessiner_interface_inventaire(screen, inventaire_joueur, 
                                      index_categorie_inv, 
                                      index_selection_inv, 
                                      sous_etat_inv, 
                                      nom_objet_selectionne,
                                      index_menu_contextuel, 
                                      index_confirmation)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()