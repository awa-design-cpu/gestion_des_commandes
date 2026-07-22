-- Script de création des tables de la base "gestion_commandes"
-- Moteur : MySQL
-- On peut exécuter ce fichier directement dans MySQL Workbench, ou
-- laisser le script Python create_tables.py le faire automatiquement.

CREATE TABLE IF NOT EXISTS fournisseur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    raison_sociale VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    telephone VARCHAR(30),
    adresse VARCHAR(255),
    date_creation DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS produit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(20) NOT NULL UNIQUE,
    designation VARCHAR(150) NOT NULL,
    prix_unitaire DECIMAL(12, 2) NOT NULL CHECK (prix_unitaire > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    date_creation DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL UNIQUE,
    date_commande DATE NOT NULL,
    fournisseur_id INT NOT NULL,
    montant_total DECIMAL(14, 2) NOT NULL DEFAULT 0,
    statut ENUM('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE') NOT NULL DEFAULT 'EN_ATTENTE',
    date_creation DATE NOT NULL,
    CONSTRAINT fk_commande_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id)
);

CREATE TABLE IF NOT EXISTS ligne_commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL CHECK (quantite > 0),
    prix_unitaire DECIMAL(12, 2) NOT NULL,
    CONSTRAINT fk_ligne_commande FOREIGN KEY (commande_id) REFERENCES commande(id),
    CONSTRAINT fk_ligne_produit FOREIGN KEY (produit_id) REFERENCES produit(id)
);
