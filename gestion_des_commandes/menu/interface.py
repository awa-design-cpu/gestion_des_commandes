
from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit
from models.commande import Commande, STATUT_VALIDEE, STATUT_LIVREE, STATUT_ANNULEE

fournisseur_dao = FournisseurDAO()
produit_dao = ProduitDAO()
commande_dao = CommandeDAO()

def demander_entier(message, minimum=None):

    while True:
        saisie = input(message)
        try:
            valeur = int(saisie)
            if minimum is not None and valeur < minimum:
                print(f"Merci de saisir un nombre supérieur ou égal à {minimum}.")
                continue
            return valeur
        except ValueError:
            print("Ce n'est pas un nombre entier valide, réessayez.")


def demander_decimal(message, minimum=None):
    """Même principe que demander_entier(), mais pour les nombres décimaux (prix)."""
    while True:
        saisie = input(message)
        try:
            valeur = float(saisie)
            if minimum is not None and valeur <= minimum:
                print(f"Merci de saisir un nombre strictement supérieur à {minimum}.")
                continue
            return valeur
        except ValueError:
            print("Ce n'est pas un nombre valide, réessayez.")


def demander_texte_obligatoire(message):
    while True:
        saisie = input(message).strip()
        if saisie:
            return saisie
        print("Ce champ est obligatoire, il ne peut pas être vide.")


def pause():
    input("\nAppuyez sur Entrée pour continuer...")


def menu_fournisseurs():
    while True:
        print("\n--- GESTION DES FOURNISSEURS ---")
        print("1. Ajouter un fournisseur")
        print("2. Lister tous les fournisseurs")
        print("3. Voir le détail d'un fournisseur")
        print("4. Modifier un fournisseur")
        print("5. Supprimer un fournisseur")
        print("6. Rechercher un fournisseur")
        print("0. Retour au menu principal")
        choix = input("Tapez votre choix : ")

        if choix == "1":
            ajouter_fournisseur()
        elif choix == "2":
            lister_fournisseurs()
        elif choix == "3":
            voir_detail_fournisseur()
        elif choix == "4":
            modifier_fournisseur()
        elif choix == "5":
            supprimer_fournisseur()
        elif choix == "6":
            rechercher_fournisseur()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


def ajouter_fournisseur():
    print("\n-- Ajout d'un fournisseur --")
    code = demander_texte_obligatoire("Code (ex: F004) : ")
    if fournisseur_dao.rechercher_par_code(code) is not None:
        print("Ce code fournisseur existe déjà.")
        return

    raison_sociale = demander_texte_obligatoire("Raison sociale : ")
    email = input("Email : ").strip()
    telephone = input("Téléphone : ").strip()
    adresse = input("Adresse : ").strip()

    fournisseur = Fournisseur(code=code, raison_sociale=raison_sociale,
                               email=email, telephone=telephone, adresse=adresse)
    nouvel_id = fournisseur_dao.ajouter(fournisseur)
    if nouvel_id:
        print(f"Fournisseur ajouté avec succès (id {nouvel_id}).")


def lister_fournisseurs():
    print("\n-- Liste des fournisseurs --")
    fournisseurs = fournisseur_dao.get_all()
    if not fournisseurs:
        print("Aucun fournisseur enregistré pour le moment.")
        return
    for f in fournisseurs:
        print(f"{f.id} - {f}")


def voir_detail_fournisseur():
    identifiant = demander_texte_obligatoire("ID ou code du fournisseur : ")
    fournisseur = _trouver_fournisseur(identifiant)
    if fournisseur is None:
        print("Fournisseur introuvable.")
        return
    print("\n-- Détail du fournisseur --")
    print("ID            :", fournisseur.id)
    print("Code          :", fournisseur.code)
    print("Raison sociale:", fournisseur.raison_sociale)
    print("Email         :", fournisseur.email)
    print("Téléphone     :", fournisseur.telephone)
    print("Adresse       :", fournisseur.adresse)
    print("Créé le       :", fournisseur.date_creation)


def modifier_fournisseur():
    identifiant = demander_texte_obligatoire("ID ou code du fournisseur à modifier : ")
    fournisseur = _trouver_fournisseur(identifiant)
    if fournisseur is None:
        print("Fournisseur introuvable.")
        return

    print("Laissez vide pour ne pas changer une information.")
    raison_sociale = input(f"Raison sociale [{fournisseur.raison_sociale}] : ").strip()
    email = input(f"Email [{fournisseur.email}] : ").strip()
    telephone = input(f"Téléphone [{fournisseur.telephone}] : ").strip()
    adresse = input(f"Adresse [{fournisseur.adresse}] : ").strip()

    if raison_sociale:
        fournisseur.raison_sociale = raison_sociale
    if email:
        fournisseur.email = email
    if telephone:
        fournisseur.telephone = telephone
    if adresse:
        fournisseur.adresse = adresse

    if fournisseur_dao.modifier(fournisseur):
        print("Fournisseur modifié avec succès.")


def supprimer_fournisseur():
    identifiant = demander_texte_obligatoire("ID ou code du fournisseur à supprimer : ")
    fournisseur = _trouver_fournisseur(identifiant)
    if fournisseur is None:
        print("Fournisseur introuvable.")
        return

    if fournisseur_dao.a_des_commandes(fournisseur.id):
        print("Impossible de supprimer ce fournisseur : il a des commandes associées.")
        return

    confirmation = input(f"Confirmer la suppression de {fournisseur.raison_sociale} ? (o/n) : ")
    if confirmation.lower() == "o":
        if fournisseur_dao.delete_by_id(fournisseur.id):
            print("Fournisseur supprimé.")


def rechercher_fournisseur():
    mot_cle = demander_texte_obligatoire("Recherche par raison sociale (mot-clé) : ")
    resultats = fournisseur_dao.rechercher_par_nom(mot_cle)
    if not resultats:
        print("Aucun fournisseur ne correspond à cette recherche.")
        return
    for f in resultats:
        print(f"{f.id} - {f}")


def _trouver_fournisseur(identifiant):
    if identifiant.isdigit():
        fournisseur = fournisseur_dao.get_by_id(int(identifiant))
        if fournisseur:
            return fournisseur
    return fournisseur_dao.rechercher_par_code(identifiant)


# ---------------------------------------------------------------------------
# 3. Gestion des produits
# ---------------------------------------------------------------------------

def menu_produits():
    while True:
        print("\n--- GESTION DES PRODUITS ---")
        print("1. Ajouter un produit")
        print("2. Lister tous les produits")
        print("3. Voir le détail d'un produit")
        print("4. Modifier un produit")
        print("5. Supprimer un produit")
        print("6. Rechercher un produit par désignation")
        print("7. Alerte de réapprovisionnement (stock sous un seuil)")
        print("0. Retour au menu principal")
        choix = input("Tapez votre choix : ")

        if choix == "1":
            ajouter_produit()
        elif choix == "2":
            lister_produits()
        elif choix == "3":
            voir_detail_produit()
        elif choix == "4":
            modifier_produit()
        elif choix == "5":
            supprimer_produit()
        elif choix == "6":
            rechercher_produit()
        elif choix == "7":
            alerte_reapprovisionnement()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


def ajouter_produit():
    print("\n-- Ajout d'un produit --")
    reference = demander_texte_obligatoire("Référence (ex: REF006) : ")
    if produit_dao.rechercher_par_reference(reference) is not None:
        print("Cette référence existe déjà.")
        return
    designation = demander_texte_obligatoire("Désignation : ")
    prix = demander_decimal("Prix unitaire (FCFA) : ", minimum=0)
    stock = demander_entier("Stock initial : ", minimum=0)

    produit = Produit(reference=reference, designation=designation,
                       prix_unitaire=prix, stock=stock)
    nouvel_id = produit_dao.ajouter(produit)
    if nouvel_id:
        print(f"Produit ajouté avec succès (id {nouvel_id}).")


def lister_produits():
    print("\n-- Liste des produits --")
    produits = produit_dao.get_all()
    if not produits:
        print("Aucun produit enregistré pour le moment.")
        return
    for p in produits:
        print(f"{p.id} - {p}")


def voir_detail_produit():
    identifiant = demander_texte_obligatoire("ID ou référence du produit : ")
    produit = _trouver_produit(identifiant)
    if produit is None:
        print("Produit introuvable.")
        return
    print("\n-- Détail du produit --")
    print("ID          :", produit.id)
    print("Référence   :", produit.reference)
    print("Désignation :", produit.designation)
    print("Prix unit.  :", produit.prix_unitaire, "FCFA")
    print("Stock       :", produit.stock)
    print("Créé le     :", produit.date_creation)


def modifier_produit():
    identifiant = demander_texte_obligatoire("ID ou référence du produit à modifier : ")
    produit = _trouver_produit(identifiant)
    if produit is None:
        print("Produit introuvable.")
        return

    print("Laissez vide pour ne pas changer une information.")
    designation = input(f"Désignation [{produit.designation}] : ").strip()
    prix = input(f"Prix unitaire [{produit.prix_unitaire}] : ").strip()
    stock = input(f"Stock [{produit.stock}] : ").strip()

    if designation:
        produit.designation = designation
    if prix:
        produit.prix_unitaire = float(prix)
    if stock:
        produit.stock = int(stock)

    if produit_dao.modifier(produit):
        print("Produit modifié avec succès.")


def supprimer_produit():
    identifiant = demander_texte_obligatoire("ID ou référence du produit à supprimer : ")
    produit = _trouver_produit(identifiant)
    if produit is None:
        print("Produit introuvable.")
        return

    if produit_dao.est_utilise_dans_une_commande(produit.id):
        print("Impossible de supprimer ce produit : il apparaît dans une commande.")
        return

    confirmation = input(f"Confirmer la suppression de {produit.designation} ? (o/n) : ")
    if confirmation.lower() == "o":
        if produit_dao.delete_by_id(produit.id):
            print("Produit supprimé.")


def rechercher_produit():
    mot_cle = demander_texte_obligatoire("Recherche par désignation (mot-clé) : ")
    resultats = produit_dao.rechercher_par_designation(mot_cle)
    if not resultats:
        print("Aucun produit ne correspond à cette recherche.")
        return
    for p in resultats:
        print(f"{p.id} - {p}")


def alerte_reapprovisionnement():
    seuil = demander_entier("Seuil de stock à surveiller : ", minimum=0)
    produits = produit_dao.produits_sous_le_seuil(seuil)
    if not produits:
        print(f"Aucun produit avec un stock inférieur à {seuil}.")
        return
    print(f"\n-- Produits avec un stock inférieur à {seuil} --")
    for p in produits:
        print(f"{p.id} - {p}")


def _trouver_produit(identifiant):
    if identifiant.isdigit():
        produit = produit_dao.get_by_id(int(identifiant))
        if produit:
            return produit
    return produit_dao.rechercher_par_reference(identifiant)


# ---------------------------------------------------------------------------
# 4. Gestion des commandes
# ---------------------------------------------------------------------------

def menu_commandes():
    while True:
        print("\n--- GESTION DES COMMANDES ---")
        print("1. Créer une nouvelle commande")
        print("2. Lister toutes les commandes")
        print("3. Voir le détail d'une commande")
        print("4. Changer le statut d'une commande")
        print("5. Annuler une commande")
        print("6. Supprimer une commande")
        print("0. Retour au menu principal")
        choix = input("Tapez votre choix : ")

        if choix == "1":
            creer_commande()
        elif choix == "2":
            lister_commandes()
        elif choix == "3":
            voir_detail_commande()
        elif choix == "4":
            changer_statut_commande()
        elif choix == "5":
            annuler_commande()
        elif choix == "6":
            supprimer_commande()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


def creer_commande():
    print("\n-- Nouvelle commande --")
    numero = demander_texte_obligatoire("Numéro de commande (ex: CMD004) : ")

    code_fournisseur = demander_texte_obligatoire("Code du fournisseur : ")
    fournisseur = fournisseur_dao.rechercher_par_code(code_fournisseur)
    if fournisseur is None:
        print("Fournisseur introuvable, commande annulée.")
        return

    panier = []
    print("Ajoutez les produits de la commande (laissez la référence vide pour terminer).")
    while True:
        reference = input("Référence produit (vide pour arrêter) : ").strip()
        if reference == "":
            break
        produit = produit_dao.rechercher_par_reference(reference)
        if produit is None:
            print("Produit introuvable.")
            continue
        quantite = demander_entier(f"Quantité de '{produit.designation}' (stock dispo: {produit.stock}) : ", minimum=1)
        panier.append((produit, quantite))

    if not panier:
        print("Aucun produit ajouté, commande annulée.")
        return

    commande = Commande(numero=numero, fournisseur_id=fournisseur.id)
    commande_id = commande_dao.creer_commande(commande, panier)
    if commande_id:
        print(f"Commande créée avec succès (id {commande_id}).")


def lister_commandes():
    print("\n-- Liste des commandes --")
    commandes = commande_dao.get_all()
    if not commandes:
        print("Aucune commande enregistrée.")
        return
    for c in commandes:
        print(f"{c.id} - {c}")


def voir_detail_commande():
    commande_id = demander_entier("ID de la commande : ", minimum=1)
    commande = commande_dao.get_detail_avec_lignes(commande_id)
    if commande is None:
        print("Commande introuvable.")
        return

    fournisseur = fournisseur_dao.get_by_id(commande.fournisseur_id)
    print("\n-- Détail de la commande --")
    print("Numéro     :", commande.numero)
    print("Date       :", commande.date_commande)
    print("Fournisseur:", fournisseur.raison_sociale if fournisseur else "?")
    print("Statut     :", commande.statut)
    print("Produits commandés :")
    for ligne in commande.lignes:
        print(f"  - {ligne.designation_produit} x{ligne.quantite} "
              f"= {ligne.sous_total()} FCFA")
    print("Montant total :", commande.montant_total, "FCFA")


def changer_statut_commande():
    commande_id = demander_entier("ID de la commande : ", minimum=1)
    print(f"Statuts possibles : {STATUT_VALIDEE}, {STATUT_LIVREE}")
    nouveau_statut = demander_texte_obligatoire("Nouveau statut : ").upper()
    if commande_dao.changer_statut(commande_id, nouveau_statut):
        print("Statut mis à jour avec succès.")


def annuler_commande():
    commande_id = demander_entier("ID de la commande à annuler : ", minimum=1)
    confirmation = input("Confirmer l'annulation (le stock sera restitué) ? (o/n) : ")
    if confirmation.lower() == "o":
        if commande_dao.annuler_commande(commande_id):
            print("Commande annulée, stock restitué.")


def supprimer_commande():
    commande_id = demander_entier("ID de la commande à supprimer : ", minimum=1)
    confirmation = input("Confirmer la suppression définitive ? (o/n) : ")
    if confirmation.lower() == "o":
        if commande_dao.delete_by_id(commande_id):
            print("Commande supprimée.")


# ---------------------------------------------------------------------------
# 5. Rapports et statistiques
# ---------------------------------------------------------------------------

def menu_rapports():
    while True:
        print("\n--- RAPPORTS ET STATISTIQUES ---")
        print("1. Commandes d'un fournisseur donné")
        print("2. Commandes en attente de validation")
        print("3. Valeur totale du stock")
        print("4. Top 5 des produits les plus commandés")
        print("5. Chiffre d'affaires total")
        print("0. Retour au menu principal")
        choix = input("Votre choix : ")

        if choix == "1":
            rapport_commandes_par_fournisseur()
        elif choix == "2":
            rapport_commandes_en_attente()
        elif choix == "3":
            rapport_valeur_stock()
        elif choix == "4":
            rapport_top_produits()
        elif choix == "5":
            rapport_chiffre_affaires()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")


def rapport_commandes_par_fournisseur():
    code = demander_texte_obligatoire("Code du fournisseur : ")
    fournisseur = fournisseur_dao.rechercher_par_code(code)
    if fournisseur is None:
        print("Fournisseur introuvable.")
        return
    commandes = commande_dao.commandes_par_fournisseur(fournisseur.id)
    if not commandes:
        print(f"Aucune commande pour {fournisseur.raison_sociale}.")
        return
    print(f"\n-- Commandes de {fournisseur.raison_sociale} --")
    for c in commandes:
        print(f"{c.id} - {c}")


def rapport_commandes_en_attente():
    commandes = commande_dao.commandes_en_attente()
    if not commandes:
        print("Aucune commande en attente.")
        return
    print("\n-- Commandes en attente de validation --")
    for c in commandes:
        print(f"{c.id} - {c}")


def rapport_valeur_stock():
    valeur = produit_dao.valeur_totale_stock()
    print(f"\nValeur totale du stock actuel : {valeur} FCFA")


def rapport_top_produits():
    resultats = produit_dao.top_produits_commandes(limite=5)
    if not resultats:
        print("Aucune commande enregistrée pour établir ce classement.")
        return
    print("\n-- Top 5 des produits les plus commandés --")
    for rang, (designation, reference, quantite_totale) in enumerate(resultats, start=1):
        print(f"{rang}. {designation} ({reference}) - {quantite_totale} unités commandées")


def rapport_chiffre_affaires():
    ca = commande_dao.chiffre_affaires_total()
    print(f"\nChiffre d'affaires total (commandes validées + livrées) : {ca} FCFA")


# ---------------------------------------------------------------------------
# 6. Menu principal
# ---------------------------------------------------------------------------

def menu_principal():
    print("=" * 55)
    print(" APPLICATION DE GESTION DES COMMANDES FOURNISSEURS")
    print("=" * 55)

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Gestion des fournisseurs")
        print("2. Gestion des produits")
        print("3. Gestion des commandes")
        print("4. Rapports et statistiques")
        print("0. Quitter")
        choix = input("Votre choix : ")

        if choix == "1":
            menu_fournisseurs()
        elif choix == "2":
            menu_produits()
        elif choix == "3":
            menu_commandes()
        elif choix == "4":
            menu_rapports()
        elif choix == "0":
            print("A bientôt !")
            break
        else:
            print("Choix invalide, veuillez réessayer.")
