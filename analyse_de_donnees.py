import numpy as np
import matplotlib.pyplot as plt
import time

# ---- Fonctions principales ---- #

def compter_voisins(grille, x, y):
    """Compte le nombre de voisins vivants pour une cellule."""
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    total = sum(grille[(x + dx) % grille.shape[0], (y + dy) % grille.shape[1]] for dx, dy in voisins)
    return total

def appliquer_regles(grille):
    """Applique les règles de l'automate à la grille."""
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:
                if voisins_vivants < 2 or voisins_vivants > 3:
                    nouvelle_grille[x, y] = 0
            else:
                if voisins_vivants == 3:
                    nouvelle_grille[x, y] = 1
    return nouvelle_grille

def analyser_structures(grille):
    """Analyse les structures simples dans la grille."""
    blocs = 0
    oscillateurs = 0
    for x in range(grille.shape[0] - 1):
        for y in range(grille.shape[1] - 1):
            # Détecte un bloc 2x2
            if np.array_equal(grille[x:x+2, y:y+2], np.array([[1, 1], [1, 1]])):
                blocs += 1
            # Autres structures peuvent être ajoutées ici
    return blocs, oscillateurs

def evolution_cellules(grille_initiale, steps):
    """Simule l'évolution de la grille sur plusieurs étapes et trace l'évolution des cellules vivantes."""
    grille = grille_initiale.copy()
    cellules_vivantes = []
    blocs_temps = []

    for step in range(steps):
        # Compter les cellules vivantes
        cellules_vivantes.append(np.sum(grille))

        # Analyser les structures (optionnel)
        blocs, _ = analyser_structures(grille)
        blocs_temps.append(blocs)

        # Passer à l'état suivant
        grille = appliquer_regles(grille)

    # Tracer les graphes
    plt.figure(figsize=(10, 6))
    plt.plot(range(steps), cellules_vivantes, label="Cellules vivantes")
    plt.plot(range(steps), blocs_temps, label="Blocs détectés (structures 2x2)")
    plt.title("Évolution des cellules et des structures")
    plt.xlabel("Étapes")
    plt.ylabel("Nombre")
    plt.legend()
    plt.grid()
    plt.show()

def temps_de_calcul_par_taille(max_taille, steps):
    """Calcule le temps de calcul pour différentes tailles de grille."""
    tailles = range(10, max_taille + 1, 10)
    temps = []

    for taille in tailles:
        grille = np.random.randint(2, size=(taille, taille))
        debut = time.time()

        for _ in range(steps):
            grille = appliquer_regles(grille)

        temps.append(time.time() - debut)

    # Tracer le graphe
    plt.figure(figsize=(10, 6))
    plt.plot(tailles, temps, 'o-', label="Temps de calcul")
    plt.title("Temps de calcul en fonction de la taille de la grille")
    plt.xlabel("Taille de la grille")
    plt.ylabel("Temps (secondes)")
    plt.grid()
    plt.legend()
    plt.show()

# ---- Programme Principal ---- #

def main():
    # Paramètres
    taille_grille = 50  # Taille de la grille (50x50)
    steps = 100  # Nombre d'étapes pour la simulation

    # Grille initiale aléatoire
    grille_initiale = np.random.randint(2, size=(taille_grille, taille_grille))

    print("Simulation de l'évolution des cellules...")
    evolution_cellules(grille_initiale, steps)

    print("\nCalcul du temps de calcul en fonction de la taille de la grille...")
    temps_de_calcul_par_taille(100, steps)

if __name__ == "__main__":
    main()
