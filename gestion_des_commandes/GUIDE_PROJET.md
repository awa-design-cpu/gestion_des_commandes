# Guide du projet - à quoi sert chaque fichier

Ce document explique, dossier par dossier et fichier par fichier, ce
que fait chaque partie du projet. L'objectif est de pouvoir répondre
sans hésiter aux questions du jury pendant la présentation orale.

---

## Vue d'ensemble : pourquoi cette organisation en couches ?

Le projet est découpé en 4 couches qui ont chacune un rôle précis et
ne se mélangent pas :

| Couche | Dossier | Rôle | Analogie |
|---|---|---|---|
| Données | `database/` | Ouvrir/fermer la connexion à MySQL | Le "câble" qui relie l'appli à la BD |
| Modèle | `models/` | Décrire les objets métier (Fournisseur, Produit...) | La "fiche d'identité" d'un objet |
| Accès aux données | `dao/` | Écrire les requêtes SQL (CRUD) | Le "traducteur" entre objets Python et lignes SQL |
| Présentation | `menu/` | Afficher les menus, lire ce que tape l'utilisateur | Le "guichet" avec lequel l'utilisateur interagit |

Cette séparation s'appelle une **architecture en couches**. L'intérêt :
si demain on veut remplacer MySQL par une autre base, on ne touche qu'à
`database/`. Si on veut une interface graphique au lieu de la console,
on ne touche qu'à `menu/`. Le reste ne bouge pas.

---

## Dossier `database/`

### `config.py`
Contient uniquement les informations de connexion (hôte, port, nom de
la base, utilisateur, mot de passe) sous forme d'un dictionnaire
Python. Centraliser ces informations ici évite de les répéter (et de
devoir les changer à plusieurs endroits) dans le reste du code.

### `connexion.py`
Définit la classe `ConnexionBD`, qui implémente le **pattern
Singleton** : quel que soit le nombre de fois où on écrit
`ConnexionBD()` dans le code, on obtient toujours le même objet, donc
la même connexion ouverte à la base de données. C'est la méthode
spéciale `__new__` qui réalise cette astuce, en gardant l'instance déjà
créée dans une variable de classe (`_instance`).

---

## Dossier `models/`

Chaque fichier contient une classe "simple" : elle ne fait que stocker
des données (des attributs), sans logique de sauvegarde en base. C'est
volontaire : un modèle représente un fournisseur/produit/commande *en
mémoire*, pas dans la base.

- `fournisseur.py` → classe `Fournisseur`
- `produit.py` → classe `Produit`
- `commande.py` → classes `Commande` et `LigneCommande`, plus les
  constantes de statut (`STATUT_EN_ATTENTE`, `STATUT_VALIDEE`, etc.)
  pour éviter les fautes de frappe ailleurs dans le code.

---

## Dossier `dao/`

DAO signifie **Data Access Object** (objet d'accès aux données).
Chaque DAO est responsable de TOUTES les requêtes SQL concernant une
table.

### `base_dao.py`
Classe **abstraite** `BaseDAO` (on ne peut jamais l'utiliser
directement, seulement en hériter). Elle regroupe les 3 opérations
communes à toutes les tables : `get_all()`, `get_by_id()` et
`delete_by_id()`. C'est ici qu'intervient l'**héritage**, une des
contraintes obligatoires du sujet : plutôt que de réécrire 3 fois le
même code, on l'écrit une fois dans `BaseDAO`, et les 3 DAO enfants en
héritent.

### `fournisseur_dao.py`, `produit_dao.py`, `commande_dao.py`
Chacun hérite de `BaseDAO` et ajoute ses propres méthodes spécifiques :
recherche, ajout, modification, règles métier (ex : impossible de
supprimer un fournisseur qui a des commandes).

`commande_dao.py` est le plus complexe car une commande touche
plusieurs tables à la fois (`commande` + `ligne_commande` +
mise à jour du `stock` dans `produit`). Toutes ces opérations sont
regroupées dans **une seule transaction** (`creer_commande`) : soit
tout réussit, soit rien n'est enregistré (`rollback`).

---

## Dossier `menu/`

### `interface.py`
Seul fichier du projet qui contient des `print()` et des `input()`.
Il est organisé en 5 parties :
1. Fonctions utilitaires de saisie (`demander_entier`, `demander_decimal`...)
   qui empêchent le programme de planter si l'utilisateur tape autre
   chose que ce qui est attendu.
2. Menu et actions "Fournisseurs"
3. Menu et actions "Produits"
4. Menu et actions "Commandes"
5. Menu et actions "Rapports"
6. Le menu principal, qui appelle les sous-menus ci-dessus.

---

## Dossier `sql/`

### `create_tables.sql`
Le script SQL "brut" de création des 4 tables (`fournisseur`,
`produit`, `commande`, `ligne_commande`), avec les clés primaires,
clés étrangères et contraintes (ex : `CHECK (stock >= 0)`).

---

## Fichiers à la racine

- **`create_tables.py`** : lit `sql/create_tables.sql` et l'exécute
  automatiquement, pour ne pas avoir à ouvrir pgAdmin à la main.
- **`insert_test_data.py`** : remplit la base avec quelques
  fournisseurs, produits et une commande d'exemple, pour pouvoir tester
  l'application tout de suite.
- **`main.py`** : point d'entrée du programme. Ne contient presque
  rien : il se contente d'appeler `menu_principal()`.
- **`requirements.txt`** : liste des bibliothèques Python nécessaires
  (ici, uniquement `mysql-connector-python` pour parler à MySQL).
- **`README.md`** : présentation générale du projet et instructions
  d'installation.

---

## Comment répondre si on vous demande "expliquez l'architecture POO" ?

Vous pouvez répondre en résumant ce document :
1. On a séparé le projet en 4 couches (données, modèle, DAO, menu).
2. Le **Singleton** garantit une seule connexion à la base.
3. L'**héritage** (`BaseDAO` → les 3 DAO) évite de dupliquer le code.
4. Toutes les requêtes sont **paramétrées** (protection contre les
   injections SQL).
5. Les opérations sensibles (création de commande, suppression) sont
   protégées par des **transactions** (`commit`/`rollback`) et des
   **try/except**.

## Comment répondre si on vous demande "quelles difficultés avez-vous
rencontrées" ?

Quelques pistes réalistes à adapter avec vos propres mots :
- Gérer une commande qui touche plusieurs tables en même temps sans
  laisser la base dans un état incohérent en cas d'erreur en cours de
  route (→ solution : tout regrouper dans une seule transaction).
- Empêcher qu'un statut de commande "recule" (ex: LIVREE → EN_ATTENTE).
- Valider les saisies de l'utilisateur (nombres, champs obligatoires)
  sans faire planter le programme.
