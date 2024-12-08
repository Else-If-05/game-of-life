import pygame
import sys
import numpy as np
import save
import matplotlib
matplotlib.use("TkAgg")  # Utiliser un backend compatible
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import fonctions_base


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

    fig, ax = plt.subplots()
    ax.plot(tailles, temps, marker='o', label="Temps de calcul")
    ax.set_title("Temps de calcul en fonction de la taille de la grille")
    ax.set_xlabel("Taille de la grille")
    ax.set_ylabel("Temps de calcul (secondes)")
    ax.legend()
    plt.show()


# Fonction principale du jeu
def boucle_jeu(taille_grille, regles):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Liste pour stocker le nombre de cellules vivantes
    cellules_vivantes = []
    threading.Thread(target=afficher_graphe_evolutif, args=(cellules_vivantes,), daemon=True).start()

    while running:
        screen.fill(COULEUR_FOND)
        dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = []
        bouton_random = pygame.Rect(850, 50, 140, 50)
        bouton_reset = pygame.Rect(850, 100, 140, 50)
        bouton_step = pygame.Rect(850, 150, 140, 50)
        bouton_auto = pygame.Rect(850, 200, 140, 50)
        bouton_quitter = pygame.Rect(850, 250, 140, 50)
        bouton_save = pygame.Rect(850, 300, 140, 50)

        boutons.extend([("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random), ("quitter", bouton_quitter), ("save", bouton_save)])

        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for nom, bouton in boutons:
                        if bouton.collidepoint(event.pos):
                            if nom == "reset":
                                grille = np.zeros((taille_grille, taille_grille), dtype=int)
                                cellules_vivantes.clear()
                            elif nom == "step":
                                grille = appliquer_regles(grille, regles)
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(nom_fichier + ".json", grille, regles)
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(compter_cellules_vivantes(grille))
                            elif nom == "quitter":
                                return afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = appliquer_regles(grille, regles)
            cellules_vivantes.append(compter_cellules_vivantes(grille))
            pygame.time.delay(300)

        clock.tick(60)

# Fonction principale du jeu avec sauvegarde chargée
def boucle_jeu_load(grille, regles):
    taille_grille = grille.shape[0]  # Taille de la grille déjà chargée
    taille_cellule = 800 // taille_grille  # Calcul de la taille de chaque cellule

    if grille is None:
        print("Erreur lors du chargement de la grille.")
        return "quit"

    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Boucle de jeu principale (comme boucle_jeu)
    while running:
        screen.fill(COULEUR_FOND)
        dessiner_grille(screen, grille, taille_cellule)  # Dessiner la grille

        # Boutons à afficher
        boutons = [
            ("reset", pygame.Rect(850, 50, 140, 50)),
            ("step", pygame.Rect(850, 120, 140, 50)),
            ("auto", pygame.Rect(850, 190, 140, 50)),
            ("random", pygame.Rect(850, 260, 140, 50)),
            ("save", pygame.Rect(850, 330, 140, 50)),
            ("quit", pygame.Rect(850, 400, 140, 50))
        ]

        # Afficher les boutons
        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for nom, bouton in boutons:
                        if bouton.collidepoint(event.pos):
                            if nom == "reset":
                                grille = np.zeros((taille_grille, taille_grille), dtype=int)  # Réinitialiser la grille
                            elif nom == "step":
                                grille = appliquer_regles(grille, regles)
                            elif nom == "auto":
                               auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))  # Remplir la grille aléatoirement
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(nom_fichier + ".json", grille, regles)
                            elif nom == "quit":
                                return "quit"

                # Basculer l'état de la cellule lors du clic sur la grille
                x, y = event.pos
                if x < 800 and y < 800:  # Clic à l'intérieur de la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]  # Basculer l'état de la cellule entre 0 et 1

        # Mode automatique : appliquer continuellement les règles
        if auto_mode:
            grille = appliquer_regles(grille, regles)
            pygame.time.delay(300)  # Délai pour contrôler la vitesse du mode automatique

        clock.tick(60)  # Limiter la fréquence d'images à 60 FPS

# Programme principal
if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))  # Fenêtre plus large pour le panneau
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = demander_taille(screen)
            REGLES = demander_regles(screen)

            # Calculer les temps de calcul pour différentes tailles de grilles
            tailles = np.arange(50, 201, 10)  # Tailles de grilles de 50 à 200
            temps = []
            for taille in tailles:
                grille_test = np.random.randint(2, size=(taille, taille))
                start = time.time()
                appliquer_regles(grille_test, REGLES)
                end = time.time()
                temps.append(end - start)

            # Afficher le graphe des temps de calcul
            afficher_graphe_temps_calcul(tailles, temps)

            # Lancer la boucle du jeu
            boucle_jeu(TAILLE_GRILLE, REGLES)
        elif action == "load_game":
            nom_fichier = save.demander_nom_fichier(screen)
            if nom_fichier:
                result = save.load_game(nom_fichier + ".json")
                if result:
                    grille, regles = result
                    boucle_jeu_load(grille, regles)  # Lancer le jeu avec les données chargées
            else:
                print("Nom de fichier non valide.")
        elif action == "quit":
            pygame.quit()
            sys.exit()
