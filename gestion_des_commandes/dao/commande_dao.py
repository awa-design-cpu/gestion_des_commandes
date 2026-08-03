
from dao.base_dao import BaseDAO
from models.commande import (
    Commande, LigneCommande,
    STATUT_EN_ATTENTE, STATUT_ANNULEE, ORDRE_STATUTS
)
from dao.produit_dao import ProduitDAO


class CommandeDAO(BaseDAO):

    def __init__(self):
        super().__init__("commande")
        self.produit_dao = ProduitDAO()

    def ligne_vers_objet(self, ligne):
        # Ordre : id, numero, date_commande, fournisseur_id, montant_total, statut, date_creation
        return Commande(
            id=ligne[0],
            numero=ligne[1],
            date_commande=ligne[2],
            fournisseur_id=ligne[3],
            montant_total=ligne[4],
            statut=ligne[5],
            date_creation=ligne[6],
        )

    def creer_commande(self, commande, panier):

        # Étape 1 : vérification du stock disponible pour chaque produit.
        for produit, quantite in panier:
            if quantite > produit.stock:
                print(f"Stock insuffisant pour {produit.designation} "
                      f"(demandé : {quantite}, disponible : {produit.stock})")
                return None

        montant_total = sum(p.prix_unitaire * qte for p, qte in panier)

        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            # Insertion de l'en-tête de la commande.
            curseur.execute(
                """
                INSERT INTO commande (numero, fournisseur_id, montant_total, statut, date_commande, date_creation)
                VALUES (%s, %s, %s, %s, CURDATE(), CURDATE())
                """,
                (commande.numero, commande.fournisseur_id, montant_total, STATUT_EN_ATTENTE)
            )
            # Pas de clause RETURNING en MySQL : on récupère l'id généré
            # avec lastrowid, juste après l'INSERT.
            commande_id = curseur.lastrowid

            # Insertion de chaque ligne, puis mise à jour du stock du produit concerné.
            for produit, quantite in panier:
                curseur.execute(
                    """
                    INSERT INTO ligne_commande (commande_id, produit_id, quantite, prix_unitaire)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (commande_id, produit.id, quantite, produit.prix_unitaire)
                )
                # On réutilise le même curseur/connexion pour rester dans
                # la même transaction (pas de commit intermédiaire ici).
                self.produit_dao.ajuster_stock(
                    produit.id, -quantite, connexion=connexion, curseur=curseur
                )

            connexion.commit()
            return commande_id
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la création de la commande :", erreur)
            return None
        finally:
            curseur.close()

    def get_detail_avec_lignes(self, commande_id):
        """
        Renvoie une commande avec la liste complète de ses lignes
        (avec le nom du produit, grâce à une jointure).
        """
        commande = self.get_by_id(commande_id)
        if commande is None:
            return None

        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                """
                SELECT lc.id, lc.commande_id, lc.produit_id, lc.quantite,
                       lc.prix_unitaire, p.designation
                FROM ligne_commande lc
                JOIN produit p ON p.id = lc.produit_id
                WHERE lc.commande_id = %s
                """,
                (commande_id,)
            )
            for ligne in curseur.fetchall():
                commande.lignes.append(LigneCommande(
                    id=ligne[0], commande_id=ligne[1], produit_id=ligne[2],
                    quantite=ligne[3], prix_unitaire=ligne[4], designation_produit=ligne[5]
                ))
            return commande
        finally:
            curseur.close()

    def changer_statut(self, commande_id, nouveau_statut):
        commande = self.get_by_id(commande_id)
        if commande is None:
            print("Commande introuvable.")
            return False

        if commande.statut == STATUT_ANNULEE:
            print("Impossible de modifier une commande annulée.")
            return False

        if nouveau_statut in ORDRE_STATUTS and commande.statut in ORDRE_STATUTS:
            rang_actuel = ORDRE_STATUTS.index(commande.statut)
            rang_nouveau = ORDRE_STATUTS.index(nouveau_statut)
            if rang_nouveau < rang_actuel:
                print("Le statut d'une commande ne peut pas reculer.")
                return False

        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                "UPDATE commande SET statut = %s WHERE id = %s",
                (nouveau_statut, commande_id)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors du changement de statut :", erreur)
            return False
        finally:
            curseur.close()

    def annuler_commande(self, commande_id):
        """
        Annule une commande : passe son statut à ANNULEE et restitue
        (remet) dans le stock les quantités qui avaient été commandées.
        """
        commande = self.get_detail_avec_lignes(commande_id)
        if commande is None:
            print("Commande introuvable.")
            return False
        if commande.statut == STATUT_ANNULEE:
            print("Cette commande est déjà annulée.")
            return False

        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            for ligne in commande.lignes:
                self.produit_dao.ajuster_stock(
                    ligne.produit_id, ligne.quantite, connexion=connexion, curseur=curseur
                )
            curseur.execute(
                "UPDATE commande SET statut = %s WHERE id = %s",
                (STATUT_ANNULEE, commande_id)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de l'annulation de la commande :", erreur)
            return False
        finally:
            curseur.close()

    def commandes_par_fournisseur(self, fournisseur_id):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT * FROM commande WHERE fournisseur_id = %s ORDER BY date_commande DESC",
                (fournisseur_id,)
            )
            return [self.ligne_vers_objet(l) for l in curseur.fetchall()]
        finally:
            curseur.close()

    def commandes_en_attente(self):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute("SELECT * FROM commande WHERE statut = 'EN_ATTENTE' ORDER BY date_commande")
            return [self.ligne_vers_objet(l) for l in curseur.fetchall()]
        finally:
            curseur.close()

    def chiffre_affaires_total(self):
        """Somme des montants des commandes VALIDEE ou LIVREE uniquement."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                """
                SELECT COALESCE(SUM(montant_total), 0) FROM commande
                WHERE statut IN ('VALIDEE', 'LIVREE')
                """
            )
            return curseur.fetchone()[0]
        finally:
            curseur.close()
