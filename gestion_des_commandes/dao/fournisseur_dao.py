
from dao.base_dao import BaseDAO
from models.fournisseur import Fournisseur


class FournisseurDAO(BaseDAO):

    def __init__(self):

        super().__init__("fournisseur")

    def ligne_vers_objet(self, ligne):

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

            if curseur.rowcount == 0:
                print("Aucun fournisseur trouvé avec cet identifiant.")
                connexion.rollback()
                return False

            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la modification du fournisseur :", erreur)
            return False
        finally:
            curseur.close()

    def rechercher_par_code(self, code):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute("SELECT * FROM fournisseur WHERE code = %s", (code,))
            ligne = curseur.fetchone()
            return self.ligne_vers_objet(ligne) if ligne else None
        finally:
            curseur.close()

    def rechercher_par_nom(self, mot_cle):
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
