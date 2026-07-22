"""
Ce module gère la connexion à la base de données MySQL.

On utilise le pattern de conception "Singleton" : il ne doit exister
qu'UNE SEULE connexion ouverte pendant toute la durée de vie du
programme. Cela évite d'ouvrir plusieurs connexions inutilement et
permet à toutes les parties de l'application (fournisseurs, produits,
commandes...) de partager la même connexion.

Comment fonctionne le Singleton ici :
- La classe garde en mémoire (dans une variable de classe) sa seule
  instance déjà créée.
- Quand on essaie de créer une nouvelle instance, on vérifie d'abord
  si une instance existe déjà. Si oui, on la retourne au lieu d'en
  créer une nouvelle.
"""

import mysql.connector
from database.config import PARAMETRES_BD


class ConnexionBD:
    """Classe Singleton responsable de la connexion à MySQL."""

    # Cette variable de classe va contenir l'unique instance de ConnexionBD.
    # Tant qu'aucune instance n'a été créée, elle vaut None.
    _instance = None

    def __new__(cls):
        # __new__ est appelée avant __init__, c'est ici qu'on décide
        # si on crée un nouvel objet ou si on renvoie celui qui existe déjà.
        if cls._instance is None:
            # Aucune instance n'existe encore : on la crée.
            cls._instance = super().__new__(cls)
            cls._instance._connexion = None
        return cls._instance

    def obtenir_connexion(self):
        """
        Retourne la connexion active à la base de données.
        Si aucune connexion n'a encore été ouverte (ou si elle a été
        coupée), on en ouvre une nouvelle.
        """
        if self._connexion is None or not self._connexion.is_connected():
            try:
                self._connexion = mysql.connector.connect(
                    host=PARAMETRES_BD["host"],
                    port=PARAMETRES_BD["port"],
                    database=PARAMETRES_BD["database"],
                    user=PARAMETRES_BD["user"],
                    password=PARAMETRES_BD["password"],
                )
            except mysql.connector.Error as erreur:
                print("Erreur de connexion à la base de données :", erreur)
                raise
        return self._connexion

    def obtenir_curseur(self):
        """
        Petit raccourci pratique : renvoie directement un curseur
        (objet qui permet d'exécuter des requêtes SQL) prêt à l'emploi.
        """
        return self.obtenir_connexion().cursor()

    def fermer_connexion(self):
        """Ferme proprement la connexion à la base de données."""
        if self._connexion is not None and self._connexion.is_connected():
            self._connexion.close()
            self._connexion = None


# Petit test manuel : si on exécute ce fichier directement
# (python database/connexion.py), on vérifie que la connexion fonctionne.
if __name__ == "__main__":
    bd = ConnexionBD()
    bd2 = ConnexionBD()
    print("Est-ce bien le même objet (Singleton) ?", bd is bd2)
    try:
        connexion = bd.obtenir_connexion()
        print("Connexion réussie à la base de données !")
        bd.fermer_connexion()
    except Exception:
        print("Impossible de se connecter, vérifiez database/config.py")
