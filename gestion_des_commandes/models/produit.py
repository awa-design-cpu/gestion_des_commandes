"""
Ce fichier définit la classe Produit, qui représente un article
du catalogue de matériel informatique (imprimante, clavier, écran...).
"""


class Produit:
    """Représente un produit vendu/acheté par l'entreprise."""

    def __init__(self, id=None, reference="", designation="",
                 prix_unitaire=0, stock=0, date_creation=None):
        self.id = id
        self.reference = reference
        self.designation = designation
        self.prix_unitaire = prix_unitaire
        self.stock = stock
        self.date_creation = date_creation

    def __str__(self):
        return (f"[{self.reference}] {self.designation} - "
                f"{self.prix_unitaire} FCFA - stock: {self.stock}")
