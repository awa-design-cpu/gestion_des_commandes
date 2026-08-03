
import mysql.connector
from database.config import PARAMETRES_BD


class ConnexionBD:
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
        return self.obtenir_connexion().cursor()

    def fermer_connexion(self):
        if self._connexion is not None and self._connexion.is_connected():
            self._connexion.close()
            self._connexion = None
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
