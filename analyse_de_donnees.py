import numpy as np
import matplotlib.pyplot as plt
import time
import moteur


# ---- Fonctions principales ---- #


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

def evolution_cellules(grille_initiale, steps, regles):
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
        grille = moteur.appliquer_regles(grille, regles)

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

def temps_de_calcul_par_taille(max_taille, steps, regles):
    """Calcule le temps de calcul pour différentes tailles de grille."""
    tailles = range(10, max_taille + 1, 10)
    temps = []

    for taille in tailles:
        grille = np.random.randint(2, size=(taille, taille))
        debut = time.time()

        for _ in range(steps):
            grille = moteur.appliquer_regles(grille, regles)

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


