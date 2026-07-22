"""
Ce script sert à créer les tables de la base de données automatiquement,
sans avoir à ouvrir MySQL Workbench. Il suffit de lancer :

    python create_tables.py

Il lit le contenu du fichier sql/create_tables.sql et l'exécute.
On aurait pu réécrire les requêtes directement en Python, mais garder
le SQL dans un fichier .sql séparé est plus propre : on peut le
relire, le tester ou le modifier sans toucher au code Python.
"""

from database.connexion import ConnexionBD


def creer_les_tables():
    print("Création des tables en cours...")

    with open("sql/create_tables.sql", "r", encoding="utf-8") as fichier:
        script_sql = fichier.read()

    bd = ConnexionBD()
    connexion = bd.obtenir_connexion()
    curseur = connexion.cursor()
    try:
        # Le script contient plusieurs instructions CREATE TABLE séparées
        # par des points-virgules. Avec mysql-connector, on doit indiquer
        # multi=True pour pouvoir toutes les exécuter d'un coup, puis
        # "consommer" chaque résultat intermédiaire avec la boucle for.
        for requete in script_sql.split(";"):
            if requete.strip():
                curseur.execute(requete)1
        connexion.commit()
        print("Les tables ont été créées avec succès (ou existaient déjà).")
    except Exception as erreur:
        connexion.rollback()
        print("Une erreur est survenue pendant la création des tables :", erreur)
    finally:
        curseur.close()


if __name__ == "__main__":
    creer_les_tables()
