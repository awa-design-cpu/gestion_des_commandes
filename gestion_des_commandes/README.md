# Gestion des Commandes Fournisseurs

Application console en Python permettant à une entreprise de gérer ses
fournisseurs, ses produits et ses commandes d'achat.

Projet réalisé dans le cadre du cours de Programmation Orientée Objet
et Base de données - Licence 2 Informatique de Gestion (IAGE).

## Fonctionnalités

- **Fournisseurs** : ajout, liste, détail, modification, suppression
  (protégée si des commandes existent), recherche par code ou nom.
- **Produits** : ajout, liste, détail, modification, suppression
  (protégée si le produit est déjà commandé), recherche par désignation,
  alerte de réapprovisionnement.
- **Commandes** : création avec plusieurs produits, vérification du
  stock disponible, mise à jour automatique du stock, calcul du montant
  total, changement de statut (EN_ATTENTE → VALIDEE → LIVREE),
  annulation avec remise en stock, suppression.
- **Rapports** : commandes par fournisseur, commandes en attente,
  valeur totale du stock, top 5 des produits les plus commandés,
  chiffre d'affaires total.

## Architecture du projet

```
gestion_commandes/
├── database/       # Connexion à la base (Singleton) et configuration
├── models/         # Classes métier (Fournisseur, Produit, Commande...)
├── dao/            # Accès aux données (une classe par table + BaseDAO)
├── menu/           # Interface utilisateur en console
├── sql/            # Script SQL de création des tables
├── create_tables.py
├── insert_test_data.py
├── main.py
└── requirements.txt
```

Voir le fichier **GUIDE_PROJET.md** pour une explication détaillée du
rôle de chaque fichier (utile pour la présentation orale).

## Choix techniques

- **Langage** : Python 3
- **Base de données** : MySQL
- **Connecteur** : mysql-connector-python
- **Pattern Singleton** : une seule connexion à la base pendant toute
  l'exécution du programme (`database/connexion.py`)
- **Héritage** : `BaseDAO` regroupe les opérations communes
  (`get_all`, `get_by_id`, `delete_by_id`), héritées par
  `FournisseurDAO`, `ProduitDAO` et `CommandeDAO`.
- **Sécurité** : toutes les requêtes SQL sont paramétrées (`%s`), ce
  qui protège contre les injections SQL.
- **Transactions** : `commit()` en cas de succès, `rollback()` en cas
  d'erreur, notamment lors de la création d'une commande (plusieurs
  tables sont modifiées en même temps).

## Installation

1. Sur votre serveur MySQL, créer une base nommée `gestion_commandes` :

```sql
CREATE DATABASE gestion_commandes;
```

2. Adapter les identifiants dans `database/config.py` (hôte, port,
   utilisateur, mot de passe) selon votre serveur MySQL.

3. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

4. Créer les tables :

```bash
python create_tables.py
```

5. (Optionnel) Insérer des données de test :

```bash
python insert_test_data.py
```

## Utilisation

```bash
python main.py
```

Un menu s'affiche dans la console. Il suffit de taper le numéro de
l'action souhaitée puis d'appuyer sur Entrée.

## Auteur

Projet réalisé par [Nom des membres du groupe] - Licence 2 IAGE.
