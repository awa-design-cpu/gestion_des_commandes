
from abc import ABC, abstractmethod
from database.connexion import ConnexionBD


class BaseDAO(ABC):
    def __init__(self, nom_table):
        self.nom_table = nom_table
        self.bd = ConnexionBD()

    @abstractmethod
    def ligne_vers_objet(self, ligne):
        raise NotImplementedError

    def get_all(self):
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(f"SELECT * FROM {self.nom_table} ORDER BY id")
            lignes = curseur.fetchall()
            return [self.ligne_vers_objet(ligne) for ligne in lignes]
        finally:
            curseur.close()

    def get_by_id(self, id_recherche):
        curseur = self.bd.obtenir_curseur()
        try:

            curseur.execute(
                f"SELECT * FROM {self.nom_table} WHERE id = %s",
                (id_recherche,)
            )
            ligne = curseur.fetchone()
            return self.ligne_vers_objet(ligne) if ligne else None
        finally:
            curseur.close()

    def delete_by_id(self, id_recherche):
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                f"DELETE FROM {self.nom_table} WHERE id = %s",
                (id_recherche,)
            )

            if curseur.rowcount == 0:
                print("Aucun élément trouvé avec cet identifiant.")
                connexion.rollback()
                return False

            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la suppression :", erreur)
            return False
        finally:
            curseur.close()