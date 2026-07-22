"""
Point d'entrée du programme.

C'est ce fichier qu'on lance pour démarrer l'application :

    python main.py

Il ne contient volontairement presque rien : tout le travail est fait
dans menu/interface.py. Ce fichier sert uniquement de "porte d'entrée".
"""

from menu.interface import menu_principal

if __name__ == "__main__":
    menu_principal()
