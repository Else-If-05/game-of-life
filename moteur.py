import numpy as np
import matplotlib.pyplot as plt
import time

def initialiser_grille(taille):
    return np.random.choice([0, 1], (taille, taille))

def compter_voisins(grille, x, y):
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    total = sum(grille[(x + dx) % grille.shape[0], (y + dy) % grille.shape[1]] for dx, dy in voisins)
    return total

def appliquer_regles(grille):
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:
                if voisins_vivants < 2 or voisins_vivants > 3:
                    nouvelle_grille[x, y] = 0  # Meurt par isolement ou surpopulation
            else:
                if voisins_vivants == 3:
                    nouvelle_grille[x, y] = 1  # Revient à la vie
    return nouvelle_grille

def afficher_grille(grille):
    plt.imshow(grille, cmap='binary')
    plt.title("Jeu de la vie de Conway")
    plt.grid(color='gray', linestyle='-', linewidth=0.5)  # Ajout de la grille quadrillée
    plt.xticks(np.arange(-0.5, grille.shape[1], 1), [])  # Quadrillage sur l'axe x
    plt.yticks(np.arange(-0.5, grille.shape[0], 1), [])  # Quadrillage sur l'axe y
    plt.show()

# Demander à l'utilisateur la taille de la grille
try:
    taille = int(input("Veuillez entrer la taille de la grille (N pour une grille NxN) : "))
    if taille <= 0:
        raise ValueError("La taille doit être un entier positif.")
except ValueError as e:
    print("Entrée invalide. La taille doit être un entier positif.")
    taille = 10  # Valeur par défaut si l'entrée est invalide

# Initialisation de la grille
grille = initialiser_grille(taille)

# Nombre d'itérations
iterations = 5

# Affichage de l'évolution de la grille
for i in range(iterations):
    print(f"Étape {i + 1}:")
    afficher_grille(grille)
    grille = appliquer_regles(grille)
    time.sleep(0.5)  # Pause pour voir l'évolution

