
class Inventaire:
    def __init__(self, pas = 70 , pieces = 0 ,gemmes = 2 , clés = 0, dés = 0):
        self.pas = pas
        self.pieces = pieces
        self.gemmes = gemmes
        self.clés = clés
        self.dés = dés

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

    def depenser_clés(self, montant):
        if self.clés >= montant :
            self.clés -= montant
            return True
        else :
            return False   
    
    def depenser_dés(self, montant):
        if self.dés >= montant :
            self.dés -= montant
            return True
        else :
            return False
        
    def ramasser_objet_permanent(self, nom_objet):
        #vérifie si l'objet (self) possede bien un attribut qui correspond à nom_objet
        if hasattr(self, nom_objet): 
            #récupere la valeur de l'attribut, ici si c'est False on va définir la valeur à True
            if not getattr(self, nom_objet):  
                setattr(self, nom_objet, True)
                print(f" Vous avez trouvé l'objet permanent : {nom_objet}")
                return True
            else :
                print(f"Vous possédez déjà l'objet :{nom_objet}")
                return False
        else :
            print(f"Erreur : L'objet permanent {nom_objet} n'existe pas.")
            return False


from abc import ABC, abstractmethod

class Consommables(ABC):
    def __init__(self, nom, gain_pas):
        self.nom = nom
        self.gain_pas = gain_pas
    
    @abstractmethod
    def utiliser(self, inventaire):
        inventaire.pas += self.gain_pas
        print(f"Vous avez gagné {self.gain_pas} pas en utilisant l'objet {self.nom}")

class Pomme(Consommables):
    def __init__(self):
        super().__init__("Pomme", gain_pas = 2)

    def utiliser(self, inventaire):
        return super().utiliser(inventaire)   

class Banane(Consommables):
    def __init__(self):
        super().__init__("Banane", gain_pas = 3)

    def utiliser(self, inventaire):
        return super().utiliser(inventaire) 

class Gâteau(Consommables):
    def __init__(self):
        super().__init__("Gâteau", gain_pas = 10)

    def utiliser(self, inventaire):
        return super().utiliser(inventaire)  

class Sandwich(Consommables):
    def __init__(self):
        super().__init__("Sandwich", gain_pas = 15)

    def utiliser(self, inventaire):
        return super().utiliser(inventaire)      

class Repas(Consommables):
    def __init__(self):
        super().__init__("Repas", gain_pas = 25)

    def utiliser(self, inventaire):
        return super().utiliser(inventaire)    



