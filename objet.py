
#---------- DEFINITION DES OBJETS DU JEU ----------#
#---------- CLASSE MERE : OBJET ----------#
class Objet :
    def __init__(self, nom: str, description: str, type_objet: str, rarete: int):
        self.nom = nom
        self.description = description
        self.type_objet = type_objet  # "permanent" ou "consommable"
        self.rarete = rarete  # 0 (commun) à 3 (légendaire)
    
    def __str__(self):
        return f"{self.nom} ({self.type_objet}, Rareté: {self.rarete})"



#---------- CLASSE FILLE D'OBJET: CONSOMMABLE ----------#
class Consommable(Objet):
    def __init__(self, nom: str, description: str, rarete: int):
        super().__init__(nom, description, "consommable", rarete)


#---------- CLASSE FILLE DE CONSOMMABLE: NOURRITURE ----------#
class Nourriture(Consommable):
    def __init__(self, nom: str, pas_rendus: int, rarete: int):
        description = f"Redonne {pas_rendus} pas."
        super().__init__(nom, description, rarete)
        self.pas_rendus = pas_rendus

    def utiliser(self, inventaire):
        """
        Utilise la nourriture pour rendre des pas.
        """
        inventaire.pas += self.pas_rendus
        print(f"{self.nom} consommé : +{self.pas_rendus} pas.")
        return True

#---------- CLASSE FILLE DE NOURRITURE : POMME ----------#
class Pomme(Nourriture):
    def __init__(self):
        super().__init__("Pomme", pas_rendus=2, rarete=0)

#---------- CLASSE FILLE DE NOURRITURE : BANANE ----------#
class Banane(Nourriture):
    def __init__(self):
        super().__init__("Banane", pas_rendus=3, rarete=0)

#---------- CLASSE FILLE DE NOURRITURE : GÂTEAU ----------#
class Gateau(Nourriture):
    def __init__(self):
        super().__init__("Gâteau", pas_rendus=10, rarete=1)

#---------- CLASSE FILLE DE NOURRITURE : SANDWICH ----------#
class Sandwich(Nourriture):
    def __init__(self):
        super().__init__("Sandwich", pas_rendus=15, rarete=2)

#---------- CLASSE FILLE DE NOURRITURE : REPAS ----------#
class Repas(Nourriture):
    def __init__(self):
        super().__init__("Repas", pas_rendus=25, rarete=3)


#---------- CLASSE FILLE DE CONSOMMABLE : RESSOURCE ----------#
class Ressource(Consommable):
    def __init__(self, nom: str, quantite: int, rarete: int):
        description = f"Donne {quantite} {nom}."
        super().__init__(nom, description, rarete)
        self.quantite = quantite

    def utiliser(self, inventaire):
        attribut_inventaire = self.nom.lower().replace("é", "e") # Crée le nom d'attribut correspondant
        if hasattr(inventaire, attribut_inventaire): #  Vérification de l'existence de l'attribut
            valeur_actuelle = getattr(inventaire, attribut_inventaire)  # Récupere la valeur actuelle
            nouvelle_valeur = valeur_actuelle + self.quantite   # Calcule la nouvelle valeur
            setattr(inventaire, attribut_inventaire, nouvelle_valeur) # Met à jour l'attribut dans l'inventaire
            print(f"Objet consommable obtenu : + {self.quantite} {self.nom}.")
            return True
        else:
            print(f"Erreur: L'inventaire ne supporte pas l'objet consommable {self.nom}.")
            return False

#---------- CLASSE FILLE DE RESSOURCE : PIECES ----------#
class Pieces(Ressource):
    def __init__(self, quantite: int):
        super().__init__("Pièces", quantite, rarete=0)

#---------- CLASSE FILLE DE RESSOURCE : GEMMES ----------#
class Gemmes(Ressource):
    def __init__(self, quantite: int):
        super().__init__("Gemmes", quantite, rarete=1)

#---------- CLASSE FILLE DE RESSOURCE : DES ----------#
class Des(Ressource):
    def __init__(self, quantite: int):
        super().__init__("Dés", quantite, rarete=1)

#---------- CLASSE FILLE DE RESSOURCE : CLES ----------#
class Cles(Ressource):
    def __init__(self, quantite: int):
        super().__init__("Clés", quantite, rarete=2)



#---------- CLASSE FILLE D'OBJET: PERMANENT ----------#
class Permanent(Objet):
    def __init__(self, nom: str, description: str, rarete: int):
        super().__init__(nom, description, "permanent", rarete)

    def utiliser(self, inventaire):
        """
        Utilise l'objet permanent dans l'inventaire.
        """
        attribut_inventaire = self.nom.lower().replace(' ', '_')  # Crée le nom d'attribut correspondant
        if hasattr(inventaire, attribut_inventaire):  # Vérification de l'existence de l'attribut
            setattr(inventaire, attribut_inventaire, True)  # Active l'attribut permanent dans l'inventaire
            print(f"Objet permanent obtenu : {self.nom}.")
            return True
        else:
            print(f"Erreur: L'inventaire ne supporte pas l'objet permanent {self.nom}.")
            return False

#---------- CLASSE FILLE DE PERMANENT: PELLE  ----------#
class Pelle(Permanent):
    def __init__(self):
        super().__init__("Pelle", "Permet de creuser des trous à certains endroits.", rarete=1)

#---------- CLASSE FILLE DE PERMANENT: MARTEAU  ----------#
class Marteau(Permanent):
    def __init__(self):
        super().__init__("Marteau", "Permet de briser les cadenas des coffres   .", rarete=2)

#---------- CLASSE FILLE DE PERMANENT: KIT DE CROCHETAGE  ----------#
class KitCrochetage(Permanent):
    def __init__(self):
        super().__init__("Kit de Crochetage", "Permet d'ouvrir les portes verrouillées.", rarete=2)

#---------- CLASSE FILLE DE PERMANENT: DETECTEUR DE METEAUX  ----------#
class DetecteurMetaux(Permanent):
    def __init__(self):
        super().__init__("Détecteur de Métaux", "Augmente la chance de trouver des clés et des pièces.", rarete=3)

#---------- CLASSE FILLE DE PERMANENT: PATE DE LAPIN  ----------#
class PatteLapin(Permanent):
    def __init__(self):
        super().__init__("Patte de Lapin", "Augmente la chance de trouver des objets.", rarete=3)