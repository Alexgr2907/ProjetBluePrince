import objet

class Inventaire:
    def __init__(self, pas = 70 , pieces = 0 ,gemmes = 2 , cles = 0, des = 0):
        # Ressources de base
        self.pas = pas
        self.pieces = pieces
        self.gemmes = gemmes
        self.cles = cles
        self.des = des

        # Objets consommables (nourriture)
        self.objets = {}
        
        # Objets permanents 
        self.pelle = True
        self.patte_lapin = True
        self.kit_crochetage = True
        self.marteau = False
        self.detecteur_métaux = False
        

    def depenser_piece(self, montant):
        """
        Dépense des pièces si possible.
        """
        if self.pieces >= montant :
            self.pieces -= montant
            return True
        else :
            return False  

    def depenser_gemmes(self, montant):
        """
        Dépense des gemmes si possible.
        """
        if self.gemmes >= montant :
            self.gemmes -= montant
            return True
        else :
            return False   

    def depenser_cles(self, montant):
        """
        Dépense des clés si possible.
        """
        if self.cles >= montant :
            self.cles -= montant
            return True
        else :
            return False

    def depenser_des(self, montant):
        """
        Dépense des dés si possible.
        """
        if self.des >= montant :
            self.des -= montant
            return True
        else :
            return False


    def ramasser_objet(self, nouvel_objet):
        """
        Rammasse un objet et met à jour dans l'inventaire.
        """

        if isinstance(nouvel_objet, objet.Consommable): 

            if isinstance(nouvel_objet, objet.Ressource):  # 1er cas : Ressource
                return nouvel_objet.utiliser(self)
                    
            else:  # 2e cas : Nourriture
                nom = nouvel_objet.nom
                if nom in self.objets:  # Si on a déjà cet objet, incrémentation du stack
                    self.objets[nom] += 1
                    print(f"Nourriture ramassée : {nom} (Total: {self.objets[nom]}).")
                else:
                    self.objets[nom] = 1
                    print(f"Nourriture ramassée : {nom}.")
                return True
        
        elif isinstance(nouvel_objet, objet.Permanent): # 3e cas : Objet permanent
            attribut_inventaire = nouvel_objet.nom.lower().replace(" ", "_")  # Crée le nom d'attribut correspondant
            if hasattr(self, attribut_inventaire):  # Vérification de l'existence de l'attribut
                if not getattr(self, attribut_inventaire):  # Si l'objet n'est pas déjà possédé
                    if nouvel_objet.utiliser(self):  # Ajoute l'objet à l'inventaire
                        return True
                    else :
                        return False
            else:
                print(f"Erreur : L'objet permanent {nouvel_objet.nom} n'existe pas dans l'inventaire.")
                return False

        else:
            print(f"Erreur : Type d'objet inconnu {nouvel_objet.nom} .")
            return False


    
    def utiliser_objet_consommable(self, nom_objet :str):
        """
        Utilise un objet consommable (nourriture) de l'inventaire.
        """

        if nom_objet in self.objets and self.objets[nom_objet] > 0:
            # On crée un catalogue qui stocke les classes des objets consommables
            catalogue = {
                "Oeuf d'araignée": objet.Pomme,
                "Araignée": objet.Banane,
                "Punaise": objet.Gateau,
                "Coléoptère adulte": objet.Sandwich,
                "Nid de sauterelle": objet.Repas
            }
    
            if nom_objet in catalogue:
                item_class = catalogue[nom_objet] 
                item_instance = item_class()  # Crée une instance temporaire de la classe

                if item_instance.utiliser(self):
                    self.objets[nom_objet] -= 1
                    if self.objets[nom_objet] <= 0:
                        del self.objets[nom_objet]  # Supprime l'entrée si la quantité est nulle
                        print(f" Vous n'avez plus de {nom_objet} dans votre inventaire. ")
                    return True
        else:
            print(f" Vous n'avez pas de {nom_objet} à utiliser. ")
            return False








