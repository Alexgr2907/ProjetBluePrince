import objet

class Inventaire:
    def __init__(self, pas = 70 , pieces = 0 ,gemmes = 2 , cles = 0, des = 0):
        self.pas = pas
        self.pieces = pieces
        self.gemmes = gemmes
        self.cles = cles
        self.des = des

        self.objets = {}
        
        self.pelle = True
        self.patte_lapin = True
        self.kit_crochetage = True
        self.marteau = False
        self.detecteur_métaux = False
        

    def depenser_piece(self, montant):
        if self.pieces >= montant :
            self.pieces -= montant
            return True
        else :
            return False  

    def depenser_gemmes(self, montant):
        if self.gemmes >= montant :
            self.gemmes -= montant
            return True
        else :
            return False   

    def depenser_cles(self, montant):
        if self.cles >= montant :
            self.cles -= montant
            return True
        else :
            return False

    def depenser_des(self, montant):
        if self.des >= montant :
            self.des -= montant
            return True
        else :
            return False


    def ramasser_objet(self, nouvel_objet):

        if isinstance(nouvel_objet, objet.Consommable):

            if isinstance(nouvel_objet, objet.Ressource): 

                if nouvel_objet.nom == "Pièces":
                    self.pieces += nouvel_objet.quantite
                elif nouvel_objet.nom == "Gemmes":
                    self.gemmes += nouvel_objet.quantite
                elif nouvel_objet.nom == "Dés":
                    self.des += nouvel_objet.quantite
                elif nouvel_objet.nom == "Clés":
                    self.cles += nouvel_objet.quantite

                print(f" Ressource ramassée : + {nouvel_objet.quantite} {nouvel_objet.nom} .")
                return True
                    
            else:
                nom = nouvel_objet.nom
                if nom in self.objets:
                    self.objets[nom] += 1
                    print(f"Nourriture ramassée : {nom} (Total: {self.objets[nom]}).")
                else:
                    self.objets[nom] = 1
                    print(f"Nourriture ramassée : {nom}.")
                return True
        
        elif isinstance(nouvel_objet, objet.Permanent):
            attribut_inventaire = nouvel_objet.nom.lower().replace(" ", "_")
            if hasattr(self, attribut_inventaire):
                if not getattr(self, attribut_inventaire):
                    nouvel_objet.utiliser(self)
                    print(f" Vous avez trouvé l'objet permanent : {nouvel_objet.nom} ")
                    return True
                else:
                    print(f" Vous avez déjà l'objet permanent : {nouvel_objet.nom} ")
                    return False
            else:
                print(f"Erreur : L'objet permanent {nouvel_objet.nom} n'existe pas dans l'inventaire.")
                return False

        else:
            print(f"Erreur : Type d'objet inconnu {nouvel_objet.nom} .")
            return False


    
    def utiliser_objet_consommable(self, nom_objet :str):

        if nom_objet in self.objets and self.objets[nom_objet] > 0:
            catalogue = {
                "Pomme": objet.Pomme(),
                "Banane": objet.Banane(),
                "Gâteau": objet.Gateau(),
                "Sandwich": objet.Sandwich(),
                "Repas": objet.Repas()
            }
    
            if nom_objet in catalogue:
                item_class = catalogue[nom_objet]   
                item_instance = item_class()

                if item_instance.utiliser(self):
                    self.objets[nom_objet] -= 1
                    if self.objets[nom_objet] <= 0:
                        del self.objets[nom_objet]
                        print(f" Vous n'avez plus de {nom_objet} dans votre inventaire. ")
                    return True
        else:
            print(f" Vous n'avez pas de {nom_objet} à utiliser. ")
            return False








