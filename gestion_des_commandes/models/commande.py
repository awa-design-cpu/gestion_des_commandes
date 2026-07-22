"""
Ce fichier définit deux classes :

- LigneCommande : une ligne à l'intérieur d'une commande
  (un produit, une quantité, un prix au moment de la commande).
- Commande : l'en-tête de la commande (numéro, fournisseur, statut...),
  qui contient une liste de LigneCommande.

Les statuts possibles d'une commande sont volontairement listés ici
sous forme de constantes, pour éviter les fautes de frappe ailleurs
dans le code (écrire "VALIDEE" au lieu de "VALIDE" par exemple).
"""

STATUT_EN_ATTENTE = "EN_ATTENTE"
STATUT_VALIDEE = "VALIDEE"
STATUT_LIVREE = "LIVREE"
STATUT_ANNULEE = "ANNULEE"

# Ordre "normal" de progression d'une commande. On s'en sert pour
# interdire à une commande de revenir en arrière (ex: LIVREE -> EN_ATTENTE).
ORDRE_STATUTS = [STATUT_EN_ATTENTE, STATUT_VALIDEE, STATUT_LIVREE]


class LigneCommande:
    """Une ligne de commande : un produit + une quantité commandée."""

    def __init__(self, id=None, commande_id=None, produit_id=None,
                 quantite=0, prix_unitaire=0, designation_produit=""):
        self.id = id
        self.commande_id = commande_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire
        # Champ pratique uniquement pour l'affichage (pas stocké tel quel
        # dans la table ligne_commande, il vient d'une jointure avec produit).
        self.designation_produit = designation_produit

    def sous_total(self):
        """Calcule le sous-total de la ligne (quantité x prix unitaire)."""
        return self.quantite * self.prix_unitaire


class Commande:
    """Représente une commande passée auprès d'un fournisseur."""

    def __init__(self, id=None, numero="", date_commande=None,
                 fournisseur_id=None, montant_total=0,
                 statut=STATUT_EN_ATTENTE, date_creation=None):
        self.id = id
        self.numero = numero
        self.date_commande = date_commande
        self.fournisseur_id = fournisseur_id
        self.montant_total = montant_total
        self.statut = statut
        self.date_creation = date_creation
        # Les lignes ne sont pas toujours chargées : seulement quand
        # on demande le détail complet d'une commande.
        self.lignes = []

    def __str__(self):
        return (f"Commande {self.numero} - {self.date_commande} - "
                f"{self.montant_total} FCFA - statut: {self.statut}")
