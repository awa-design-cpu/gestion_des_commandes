"""
Ce fichier regroupe les informations de connexion à la base de données.
On les met ici, dans un seul endroit, pour ne pas avoir à les répéter
(et les modifier) dans plusieurs fichiers du projet.

Si la base de données est installée sur un autre ordinateur (ou sur un
serveur), ou si le mot de passe change, il suffit de modifier ce fichier.
"""

# Paramètres de connexion à MySQL.
# A adapter selon l'installation/le serveur de chacun.
PARAMETRES_BD = {
    "host": "localhost",
    "port": "3306",
    "database": "gestion_commandes",
    "user": "root",
    "password": "",
}
