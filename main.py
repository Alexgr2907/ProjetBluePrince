import affichage  
import pygame

def main():
    """
    Fonction principale pour initialiser et lancer le jeu.
    C'est le point d'entrée du programme.
    """
    try:
        # On appelle la fonction principale (boucle de jeu) 
        # définie dans le fichier affichage.py
        affichage.lancer_jeu()
        
    except Exception as e:
        # En cas d'erreur majeure, l'afficher proprement
        print(f"Une erreur critique est survenue: {e}")
        pygame.quit() # S'assurer de fermer pygame en cas de crash

# Cette ligne vérifie si on exécute ce fichier directement
# (ex: "python main.py")
if __name__ == "__main__":
    main()