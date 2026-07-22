"""
DAO pour la table "produit".
Même logique que FournisseurDAO : on hérite de BaseDAO pour les
opérations communes, et on ajoute ici tout ce qui est spécifique
aux produits (recherche, alerte de stock, mise à jour du stock...).
"""

from dao.base_dao import BaseDAO
from models.produit import Produit


class ProduitDAO(BaseDAO):

    def __init__(self):
        super().__init__("produit")

    def ligne_vers_objet(self, ligne):
        # Ordre des colonnes : id, reference, designation, prix_unitaire, stock, date_creation
        return Produit(
            id=ligne[0],
            reference=ligne[1],
            designation=ligne[2],
            prix_unitaire=ligne[3],
            stock=ligne[4],
            date_creation=ligne[5],
        )

    def ajouter(self, produit):
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                """
                INSERT INTO produit (reference, designation, prix_unitaire, stock, date_creation)
                VALUES (%s, %s, %s, %s, CURDATE())
                """,
                (produit.reference, produit.designation, produit.prix_unitaire, produit.stock)
            )
            nouvel_id = curseur.lastrowid
            connexion.commit()
            return nouvel_id
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de l'ajout du produit :", erreur)
            return None
        finally:
            curseur.close()

    def modifier(self, produit):
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                """
                UPDATE produit
                SET designation = %s, prix_unitaire = %s, stock = %s
                WHERE id = %s
                """,
                (produit.designation, produit.prix_unitaire, produit.stock, produit.id)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la modification du produit :", erreur)
            return False
        finally:
            curseur.close()

    def rechercher_par_reference(self, reference):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute("SELECT * FROM produit WHERE reference = %s", (reference,))
            ligne = curseur.fetchone()
            return self.ligne_vers_objet(ligne) if ligne else None
        finally:
            curseur.close()

    def rechercher_par_designation(self, mot_cle):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT * FROM produit WHERE designation LIKE %s ORDER BY id",
                (f"%{mot_cle}%",)
            )
            lignes = curseur.fetchall()
            return [self.ligne_vers_objet(l) for l in lignes]
        finally:
            curseur.close()

    def produits_sous_le_seuil(self, seuil):
        """Renvoie les produits dont le stock est inférieur au seuil donné
        (utile pour l'alerte de réapprovisionnement)."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT * FROM produit WHERE stock < %s ORDER BY stock ASC",
                (seuil,)
            )
            lignes = curseur.fetchall()
            return [self.ligne_vers_objet(l) for l in lignes]
        finally:
            curseur.close()

    def est_utilise_dans_une_commande(self, produit_id):
        """Vérifie si un produit apparaît dans au moins une ligne de commande."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT COUNT(*) FROM ligne_commande WHERE produit_id = %s",
                (produit_id,)
            )
            return curseur.fetchone()[0] > 0
        finally:
            curseur.close()

    def ajuster_stock(self, produit_id, variation, connexion=None, curseur=None):
        """
        Modifie le stock d'un produit d'une certaine quantité (positive
        pour réapprovisionner, négative pour retirer suite à une commande).

        On accepte en paramètre une connexion/curseur déjà ouverts, afin
        de pouvoir appeler cette méthode DEPUIS une transaction plus large
        (par exemple : créer une commande ET diminuer le stock d'un coup,
        sans faire de commit intermédiaire). Si rien n'est fourni, on gère
        notre propre transaction.
        """
        gere_sa_propre_transaction = connexion is None
        if gere_sa_propre_transaction:
            connexion = self.bd.obtenir_connexion()
            curseur = connexion.cursor()
        try:
            curseur.execute(
                "UPDATE produit SET stock = stock + %s WHERE id = %s",
                (variation, produit_id)
            )
            if gere_sa_propre_transaction:
                connexion.commit()
            return True
        except Exception as erreur:
            if gere_sa_propre_transaction:
                connexion.rollback()
            print("Erreur lors de l'ajustement du stock :", erreur)
            return False
        finally:
            if gere_sa_propre_transaction:
                curseur.close()

    def valeur_totale_stock(self):
        """Calcule la valeur totale du stock : somme(prix_unitaire * stock)."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute("SELECT COALESCE(SUM(prix_unitaire * stock), 0) FROM produit")
            return curseur.fetchone()[0]
        finally:
            curseur.close()

    def top_produits_commandes(self, limite=5):
        """
        Renvoie les produits les plus commandés (en quantité totale
        cumulée sur toutes les commandes), du plus commandé au moins commandé.
        """
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                """
                SELECT p.designation, p.reference, SUM(lc.quantite) AS quantite_totale
                FROM ligne_commande lc
                JOIN produit p ON p.id = lc.produit_id
                GROUP BY p.id, p.designation, p.reference
                ORDER BY quantite_totale DESC
                LIMIT %s
                """,
                (limite,)
            )
            return curseur.fetchall()
        finally:
            curseur.close()
