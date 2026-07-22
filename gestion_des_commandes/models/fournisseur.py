"""
Ce fichier définit la classe Fournisseur.

Un objet Fournisseur ne contient QUE les données (les attributs).
Il ne sait pas comment se sauvegarder dans la base : c'est le rôle
du FournisseurDAO (voir dao/fournisseur_dao.py). Cette séparation
(modèle / DAO) rend le code plus clair : chaque classe a un seul rôle.
"""


class Fournisseur:
    """Représente un fournisseur de l'entreprise."""

    def __init__(self, id=None, code="", raison_sociale="", email="",
                 telephone="", adresse="", date_creation=None):
        self.id = id
        self.code = code
        self.raison_sociale = raison_sociale
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.date_creation = date_creation

    def __str__(self):
        # Cette méthode définit ce qui s'affiche quand on fait print(fournisseur).
        return f"[{self.code}] {self.raison_sociale} - {self.telephone}"
