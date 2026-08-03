
from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit
from models.commande import Commande


def inserer_donnees_de_test():
    fournisseur_dao = FournisseurDAO()
    produit_dao = ProduitDAO()
    commande_dao = CommandeDAO()

    print("Insertion des fournisseurs...")
    fournisseurs = [
        Fournisseur(code="F001", raison_sociale="Teranga Bureautique",
                    email="contact@terangabureautique.sn", telephone="338201122",
                    adresse="Sacré-Coeur 3, Dakar"),
        Fournisseur(code="F002", raison_sociale="Sahel Informatique",
                    email="ventes@sahelinfo.sn", telephone="338453377",
                    adresse="Zone industrielle, Dakar"),
        Fournisseur(code="F003", raison_sociale="Baobab Tech Distribution",
                    email="contact@baobabtech.sn", telephone="776543210",
                    adresse="Sicap Liberté 6, Dakar"),
    ]
    ids_fournisseurs = []
    for f in fournisseurs:
        # On évite de créer un doublon si le script est relancé plusieurs fois.
        if fournisseur_dao.rechercher_par_code(f.code) is None:
            ids_fournisseurs.append(fournisseur_dao.ajouter(f))
        else:
            ids_fournisseurs.append(fournisseur_dao.rechercher_par_code(f.code).id)

    print("Insertion des produits...")
    produits = [
        Produit(reference="REF001", designation="Ordinateur portable HP 15 pouces",
                prix_unitaire=285000, stock=12),
        Produit(reference="REF002", designation="Imprimante laser Canon", prix_unitaire=95000, stock=8),
        Produit(reference="REF003", designation="Clavier + souris sans fil", prix_unitaire=12000, stock=30),
        Produit(reference="REF004", designation="Ecran 24 pouces Dell", prix_unitaire=110000, stock=5),
        Produit(reference="REF005", designation="Disque dur externe 1 To", prix_unitaire=35000, stock=20),
    ]
    ids_produits = []
    for p in produits:
        if produit_dao.rechercher_par_reference(p.reference) is None:
            ids_produits.append(produit_dao.ajouter(p))
        else:
            ids_produits.append(produit_dao.rechercher_par_reference(p.reference).id)

    print("Insertion d'une commande d'exemple...")
    if commande_dao.get_by_id(1) is None:
        produit_a = produit_dao.get_by_id(ids_produits[0])
        produit_b = produit_dao.get_by_id(ids_produits[2])

        commande = Commande(numero="CMD001", fournisseur_id=ids_fournisseurs[0])
        panier = [(produit_a, 2), (produit_b, 5)]
        commande_dao.creer_commande(commande, panier)

    print("Données de test insérées avec succès.")


if __name__ == "__main__":
    inserer_donnees_de_test()
