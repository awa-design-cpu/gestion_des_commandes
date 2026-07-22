"""
DAO (Data Access Object) pour la table "fournisseur".
Toutes les requêtes SQL concernant les fournisseurs passent par ici.
Les opérations get_all / get_by_id / delete_by_id viennent déjà de
BaseDAO (héritage), on n'a besoin d'écrire que ce qui est spécifique
aux fournisseurs.
"""

from dao.base_dao import BaseDAO
from models.fournisseur import Fournisseur


class FournisseurDAO(BaseDAO):

    def __init__(self):
        # On indique à la classe parente le nom de la table à utiliser.
        super().__init__("fournisseur")

    def ligne_vers_objet(self, ligne):
        # L'ordre des colonnes correspond à l'ordre défini dans la table SQL :
        # id, code, raison_sociale, email, telephone, adresse, date_creation
        return Fournisseur(
            id=ligne[0],
            code=ligne[1],
            raison_sociale=ligne[2],
            email=ligne[3],
            telephone=ligne[4],
            adresse=ligne[5],
            date_creation=ligne[6],
        )

    def ajouter(self, fournisseur):
        """Insère un nouveau fournisseur et renvoie son id généré."""
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                """
                INSERT INTO fournisseur (code, raison_sociale, email, telephone, adresse, date_creation)
                VALUES (%s, %s, %s, %s, %s, CURDATE())
                """,
                (fournisseur.code, fournisseur.raison_sociale, fournisseur.email,
                 fournisseur.telephone, fournisseur.adresse)
            )
            # Avec MySQL, on récupère l'id auto-généré via lastrowid
            # (il n'y a pas de clause RETURNING comme sous PostgreSQL).
            nouvel_id = curseur.lastrowid
            connexion.commit()
            return nouvel_id
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de l'ajout du fournisseur :", erreur)
            return None
        finally:
            curseur.close()

    def modifier(self, fournisseur):
        """Met à jour les informations d'un fournisseur existant."""
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                """
                UPDATE fournisseur
                SET raison_sociale = %s, email = %s, telephone = %s, adresse = %s
                WHERE id = %s
                """,
                (fournisseur.raison_sociale, fournisseur.email,
                 fournisseur.telephone, fournisseur.adresse, fournisseur.id)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la modification du fournisseur :", erreur)
            return False
        finally:
            curseur.close()

    def rechercher_par_code(self, code):
        """Cherche un fournisseur par son code exact (ex: F001)."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute("SELECT * FROM fournisseur WHERE code = %s", (code,))
            ligne = curseur.fetchone()
            return self.ligne_vers_objet(ligne) if ligne else None
        finally:
            curseur.close()

    def rechercher_par_nom(self, mot_cle):
        """
        Cherche les fournisseurs dont la raison sociale contient le mot-clé
        (recherche partielle). Avec la collation par défaut de MySQL,
        LIKE ignore déjà la casse, inutile d'utiliser LOWER().
        """
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT * FROM fournisseur WHERE raison_sociale LIKE %s ORDER BY id",
                (f"%{mot_cle}%",)
            )
            lignes = curseur.fetchall()
            return [self.ligne_vers_objet(l) for l in lignes]
        finally:
            curseur.close()

    def a_des_commandes(self, fournisseur_id):
        """
        Vérifie si un fournisseur possède au moins une commande.
        Utile avant une suppression : un fournisseur avec des commandes
        ne doit pas pouvoir être supprimé (contrainte du sujet).
        """
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(
                "SELECT COUNT(*) FROM commande WHERE fournisseur_id = %s",
                (fournisseur_id,)
            )
            nombre = curseur.fetchone()[0]
            return nombre > 0
        finally:
            curseur.close()
