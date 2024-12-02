import numpy as np
import matplotlib.pyplot as plt
import time


def initialiser_grille(taille):
    """Initialise une grille aléatoire de taille donnée."""
    return np.random.choice([0, 1], (taille, taille))


def compter_voisins(grille, x, y):
    """Compte les voisins vivants d'une cellule avec des bords périodiques."""
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    taille = grille.shape[0]
    total = 0
    for dx, dy in voisins:
        voisin_x = (x + dx) % taille  # Bords périodiques pour la ligne
        voisin_y = (y + dy) % taille  # Bords périodiques pour la colonne
        total += grille[voisin_x, voisin_y]
    return total


def appliquer_regles(grille, regles):
    """
    Applique les règles du jeu pour générer une nouvelle grille.
    """
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:  # Cellule vivante
                if voisins_vivants < regles['min_vivants'] or voisins_vivants > regles['max_vivants']:
                    nouvelle_grille[x, y] = 0  # Meurt par isolement ou surpopulation
            else:  # Cellule morte
                if voisins_vivants == regles['revient_a_la_vie']:
                    nouvelle_grille[x, y] = 1  # Revient à la vie
    return nouvelle_grille


def afficher_grille(grille):
    """Affiche la grille sous forme graphique."""
    plt.imshow(grille, cmap='binary')
    plt.title("Jeu de la vie de Conway (Grille infinie)")
    plt.grid(color='gray', linestyle='-', linewidth=0.5)
    plt.xticks(np.arange(-0.5, grille.shape[1], 1), [])
    plt.yticks(np.arange(-0.5, grille.shape[0], 1), [])
    plt.show()


def demander_regles():
    """Demande à l'utilisateur de modifier les règles ou utilise les valeurs par défaut."""
    print("Voulez-vous changer les règles du jeu ? (o/n)")
    choix = input("> ").lower()
    if choix == 'o':
        try:
            min_vivants = int(input("Nombre minimum de voisins pour survivre : "))
            max_vivants = int(input("Nombre maximum de voisins pour survivre : "))
            revient_a_la_vie = int(input("Nombre exact de voisins pour revenir à la vie : "))
            return {
                'min_vivants': min_vivants,
                'max_vivants': max_vivants,
                'revient_a_la_vie': revient_a_la_vie
            }
        except ValueError:
            print("Entrée invalide. Les règles par défaut seront utilisées.")
    else:
        return {
            'min_vivants': 2,  # Par défaut
            'max_vivants': 3,  # Par défaut
            'revient_a_la_vie': 3  # Par défaut
        }


#J'AI COPIE LA SUITE DU CODE DANS LE MAIN. SEVIM
