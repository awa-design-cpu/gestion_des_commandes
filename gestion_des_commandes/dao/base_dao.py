"""
Ce fichier définit BaseDAO, une classe ABSTRAITE (on ne peut jamais
créer directement un objet BaseDAO, elle sert uniquement de "modèle"
pour les autres DAO : FournisseurDAO, ProduitDAO, CommandeDAO).

L'intérêt : les 3 opérations get_all(), get_by_id() et delete_by_id()
sont quasiment identiques d'une table à l'autre (seul le nom de la
table change). Plutôt que de réécrire 3 fois le même code, on l'écrit
une seule fois ici, et chaque DAO enfant en hérite (héritage = un des
piliers de la POO demandés dans le sujet).

Chaque DAO enfant doit simplement dire :
- quel est le nom de sa table (self.nom_table)
- comment transformer une ligne de résultat SQL en objet Python
  (méthode ligne_vers_objet, propre à chaque DAO).
"""

from abc import ABC, abstractmethod
from database.connexion import ConnexionBD


class BaseDAO(ABC):
    """Classe abstraite regroupant les opérations CRUD communes."""

    def __init__(self, nom_table):
        self.nom_table = nom_table
        self.bd = ConnexionBD()

    @abstractmethod
    def ligne_vers_objet(self, ligne):
        """
        Chaque DAO enfant DOIT fournir sa propre version de cette
        méthode : elle transforme une ligne (un tuple renvoyé par le
        connecteur MySQL) en objet du bon type (Fournisseur, Produit...).
        """
        raise NotImplementedError

    def get_all(self):
        """Renvoie la liste de TOUS les enregistrements de la table."""
        curseur = self.bd.obtenir_curseur()
        try:
            curseur.execute(f"SELECT * FROM {self.nom_table} ORDER BY id")
            lignes = curseur.fetchall()
            return [self.ligne_vers_objet(ligne) for ligne in lignes]
        finally:
            curseur.close()

    def get_by_id(self, id_recherche):
        """Renvoie un seul enregistrement à partir de son id, ou None."""
        curseur = self.bd.obtenir_curseur()
        try:
            # Requête paramétrée (le %s) : on ne construit JAMAIS la
            # requête en collant directement la valeur avec un +,
            # pour se protéger des injections SQL.
            curseur.execute(
                f"SELECT * FROM {self.nom_table} WHERE id = %s",
                (id_recherche,)
            )
            ligne = curseur.fetchone()
            return self.ligne_vers_objet(ligne) if ligne else None
        finally:
            curseur.close()

    def delete_by_id(self, id_recherche):
        """Supprime un enregistrement à partir de son id."""
        connexion = self.bd.obtenir_connexion()
        curseur = connexion.cursor()
        try:
            curseur.execute(
                f"DELETE FROM {self.nom_table} WHERE id = %s",
                (id_recherche,)
            )
            connexion.commit()
            return True
        except Exception as erreur:
            connexion.rollback()
            print("Erreur lors de la suppression :", erreur)
            return False
        finally:
            curseur.close()
