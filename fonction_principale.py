import matplotlib
import numpy as np
import pygame

import save

matplotlib.use("TkAgg")  # Utiliser un backend compatible
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import fonctions_base
import time





# Modèles pour les "Still lifes"
STILL_LIFES = {
    "Block": np.array([[1, 1],
                       [1, 1]]),
    "Beehive": np.array([[0, 1, 1, 0],
                         [1, 0, 0, 1],
                         [0, 1, 1, 0]]),
    "Loaf": np.array([[0, 1, 1, 0],
                      [1, 0, 0, 1],
                      [0, 1, 0, 1],
                      [0, 0, 1, 0]]),
    "Boat": np.array([[1, 1, 0],
                      [1, 0, 1],
                      [0, 1, 0]]),
    "Tub": np.array([[0, 1, 0],
                     [1, 0, 1],
                     [0, 1, 0]])
}


# Fonction pour compter les cellules vivantes dans la grille
def compter_cellules_vivantes(grille):
    return np.sum(grille)

# Fonction pour gérer le graphe évolutif dans un thread séparé
def afficher_graphe_evolutif(data):
    fig, ax = plt.subplots()
    ax.set_title("Évolution du nombre de cellules vivantes")
    ax.set_xlabel("Temps (itérations)")
    ax.set_ylabel("Cellules vivantes")
    line, = ax.plot([], [], label="Cellules vivantes")
    ax.legend()
    x_data, y_data = [], []

    def update(frame):
        if len(data) > 0:
            x_data.append(len(x_data))  # Ajoute le numéro de l'itération
            y_data.append(data[-1])    # Ajoute le dernier nombre de cellules vivantes
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view()

    ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
    plt.show()


# Fonction pour détecter une structure dans une sous-grille
def detect_structure(subgrid, structure):
    return np.array_equal(subgrid, structure)

# Fonction pour analyser la grille et compter les "Still lifes"
def analyser_still_lifes(grille):
    counts = {key: 0 for key in STILL_LIFES}
    taille_grille = grille.shape

    for name, pattern in STILL_LIFES.items():
        pattern_size = pattern.shape
        for x in range(taille_grille[0] - pattern_size[0] + 1):
            for y in range(taille_grille[1] - pattern_size[1] + 1):
                subgrid = grille[x:x + pattern_size[0], y:y + pattern_size[1]]
                if detect_structure(subgrid, pattern):
                    counts[name] += 1

    return counts

# Fonction pour afficher un histogramme
def afficher_histogramme_still_lifes(counts):
    names = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 6))
    plt.bar(names, values, color="skyblue")
    plt.xlabel("Structures")
    plt.ylabel("Occurrences")
    plt.title("Occurrences des Still Lifes dans la grille")
    plt.show()

def afficher_graphe_temps_calcul(tailles, temps):
    """
    Affiche un graphe des temps de calcul en fonction de la taille de la grille.
    """
    fig, ax = plt.subplots()
    ax.plot(tailles, temps, marker='o', label="Temps de calcul")
    ax.set_title("Temps de calcul en fonction de la taille de la grille")
    ax.set_xlabel("Taille de la grille")
    ax.set_ylabel("Temps de calcul (secondes)")
    ax.legend()
    plt.show()


# Fonction principale du jeu
# Fonction pour gérer les graphiques évolutifs
def afficher_graphes_evolutifs(cellules_vivantes, still_lifes_data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Graphique de l'évolution des cellules vivantes
    ax1.set_title("Évolution du nombre de cellules vivantes")
    ax1.set_xlabel("Temps (itérations)")
    ax1.set_ylabel("Cellules vivantes")
    line, = ax1.plot([], [], label="Cellules vivantes", color="blue")
    ax1.legend()
    x_data, y_data = [], []

    # Histogramme des still lifes
    ax2.set_title("Histogramme des Still Lifes")
    ax2.set_xlabel("Type de structure")
    ax2.set_ylabel("Nombre détecté")
    bars = ax2.bar(STILL_LIFES.keys(), [0] * len(STILL_LIFES), color="skyblue")
    plt.tight_layout()

    def update(frame):
        # Mettre à jour le graphe des cellules vivantes
        if len(cellules_vivantes) > 0:
            x_data.append(len(x_data))
            y_data.append(cellules_vivantes[-1])
            line.set_data(x_data, y_data)
            ax1.relim()
            ax1.autoscale_view()

        # Mettre à jour l'histogramme des still lifes
        if len(still_lifes_data) > 0:
            last_counts = still_lifes_data[-1]
            for bar, count in zip(bars, last_counts.values()):
                bar.set_height(count)

        ax2.set_ylim(0, max([bar.get_height() for bar in bars]) + 1)  # Ajuster la hauteur max

    ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
    plt.show()


# Fonction principale du jeu
def boucle_jeu(taille_grille, regles, cellules_vivantes=None, still_lifes_data=None):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Initialiser les données pour le graphe évolutif
    if cellules_vivantes is None:
        cellules_vivantes = []
    if still_lifes_data is None:
        still_lifes_data = []

    # Lancer le thread pour les graphiques évolutifs
    threading.Thread(target=afficher_graphes_evolutifs, args=(cellules_vivantes, still_lifes_data), daemon=True).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = [
            ("reset", pygame.Rect(850, 50, 140, 50)),
            ("step", pygame.Rect(850, 100, 140, 50)),
            ("auto", pygame.Rect(850, 150, 140, 50)),
            ("random", pygame.Rect(850, 200, 140, 50)),
            ("save", pygame.Rect(850, 250, 140, 50)),
            ("quit", pygame.Rect(850, 300, 140, 50)),
        ]

        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            fonctions_base.dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for nom, bouton in boutons:
                        if bouton.collidepoint(event.pos):
                            if nom == "reset":
                                grille.fill(0)
                                cellules_vivantes.clear()
                                still_lifes_data.clear()
                            elif nom == "step":
                                grille = fonctions_base.appliquer_regles(grille, regles)
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                                still_lifes_data.append(analyser_still_lifes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                                still_lifes_data.append(analyser_still_lifes(grille))
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(
                                        nom_fichier + ".json",
                                        grille,
                                        regles,
                                        cellules_vivantes=cellules_vivantes,
                                        still_lifes_data=still_lifes_data,
                                    )
                            elif nom == "quit":
                                return fonctions_base.afficher_accueil()

                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            cellules_vivantes.append(compter_cellules_vivantes(grille))
            still_lifes_data.append(analyser_still_lifes(grille))
            pygame.time.delay(300)

        clock.tick(60)



# Fonction principale du jeu avec sauvegarde chargée
def boucle_jeu_load(grille, regles, cellules_vivantes):
    taille_grille = grille.shape[0]
    taille_cellule = 800 // taille_grille
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Lancer le graphe évolutif dans un thread
    threading.Thread(target=afficher_graphe_evolutif, args=(cellules_vivantes,), daemon=True).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Boutons de contrôle
        boutons = [
            ("reset", pygame.Rect(850, 50, 140, 50)),
            ("step", pygame.Rect(850, 100, 140, 50)),
            ("auto", pygame.Rect(850, 150, 140, 50)),
            ("random", pygame.Rect(850, 200, 140, 50)),
            ("save", pygame.Rect(850, 250, 140, 50)),
            ("quit", pygame.Rect(850, 300, 140, 50)),
        ]

        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            fonctions_base.dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for nom, bouton in boutons:
                        if bouton.collidepoint(event.pos):
                            if nom == "reset":
                                grille.fill(0)
                                cellules_vivantes.clear()
                            elif nom == "step":
                                grille = fonctions_base.appliquer_regles(grille, regles)
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(
                                        nom_fichier + ".json",
                                        grille,
                                        regles,
                                        cellules_vivantes=cellules_vivantes
                                    )
                            elif nom == "quit":
                                return fonctions_base.afficher_accueil()

                # Basculer l'état de la cellule lors du clic sur la grille
                x, y = event.pos
                if x < 800 and y < 800:  # Clic à l'intérieur de la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]  # Basculer l'état de la cellule entre 0 et 1

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            cellules_vivantes.append(compter_cellules_vivantes(grille))
            pygame.time.delay(300)

        clock.tick(60)

# Programme principal
if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))  # Fenêtre plus large pour le panneau
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = fonctions_base.afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = fonctions_base.demander_taille(screen)
            REGLES = fonctions_base.demander_regles(screen)

            # Calculer les temps de calcul pour différentes tailles de grilles
            tailles = np.arange(50, 201, 10)  # Tailles de grilles de 50 à 200
            temps = []
            for taille in tailles:
                grille_test = np.random.randint(2, size=(taille, taille))
                start = time.time()
                fonctions_base.appliquer_regles(grille_test, REGLES)
                end = time.time()
                temps.append(end - start)

            # Afficher le graphe des temps de calcul
            afficher_graphe_temps_calcul(tailles, temps)

            # Initialisation pour une nouvelle partie
            cellules_vivantes = []  # Liste pour l'évolution des cellules vivantes
            still_lifes_data = []  # Liste pour l'évolution des structures still lifes
            boucle_jeu(TAILLE_GRILLE, REGLES, cellules_vivantes, still_lifes_data)

        elif action == "load_game":
            nom_fichier = save.demander_nom_fichier(screen)
            if nom_fichier:
                result = save.load_game(nom_fichier + ".json")
                if result:
                    grille, regles, cellules_vivantes, still_lifes_data = result
                    if cellules_vivantes is None:
                        cellules_vivantes = []  # Initialiser comme liste vide si absente
                    if still_lifes_data is None:
                        still_lifes_data = []  # Initialiser comme liste vide si absente
                    boucle_jeu_load(grille, regles, cellules_vivantes, still_lifes_data)  # Lancer le jeu avec les données chargées
            else:
                print("Nom de fichier non valide.")

        elif action == "quit":
            continue
