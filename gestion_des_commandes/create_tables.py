
from database.connexion import ConnexionBD


def creer_les_tables():
    print("Création des tables en cours...")
    with open("sql/create_tables.sql", "r", encoding="utf-8") as fichier:
        script_sql = fichier.read()

    bd = ConnexionBD()
    connexion = bd.obtenir_connexion()
    curseur = connexion.cursor()
    try:
        for requete in script_sql.split(";"):
            if requete.strip():
                curseur.execute(requete)
        connexion.commit()
        print("Les tables ont été créées avec succès (ou existaient déjà).")
    except Exception as erreur:
        connexion.rollback()
        print("Une erreur est survenue pendant la création des tables :", erreur)
    finally:
        curseur.close()


if __name__ == "__main__":
    creer_les_tables()
