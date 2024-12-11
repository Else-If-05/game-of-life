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
import optimisation
import fonctions_base
import graphique

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
    threading.Thread(target=graphique.afficher_graphes_evolutifs, args=(cellules_vivantes, still_lifes_data), daemon=True).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = []
        bouton_random = pygame.Rect(850, 60, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 180, 140, 50)
        bouton_auto = pygame.Rect(850, 240, 140, 50)
        bouton_quitter = pygame.Rect(850, 300, 140, 50)
        bouton_save = pygame.Rect(850, 360, 140, 50)

        boutons.extend([("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random), ("quitter", bouton_quitter), ("save", bouton_save)])

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
                                grille = optimisation.appliquer_regles_optimise(grille, regles)
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                optimisation.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")

                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_jeu(nom_fichier + ".json", grille, regles)

                            elif nom == "quitter":
                                return fonctions_base.afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
            still_lifes_data.append(graphique.analyser_still_lifes(grille))
            pygame.time.delay(300)

        clock.tick(60)


# Fonction principale du jeu avec sauvegarde chargée
def boucle_jeu_load(grille, regles, cellules_vivantes, still_lifes_data):
    taille_grille = grille.shape[0]
    taille_cellule = 800 // taille_grille
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Lancer le thread pour les graphiques évolutifs
    threading.Thread(
        target=graphique.afficher_graphes_evolutifs, args=(cellules_vivantes, still_lifes_data), daemon=True
    ).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = []
        bouton_random = pygame.Rect(850, 60, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 180, 140, 50)
        bouton_auto = pygame.Rect(850, 240, 140, 50)
        bouton_quitter = pygame.Rect(850, 300, 140, 50)
        bouton_save = pygame.Rect(850, 360, 140, 50)

        boutons.extend(
            [("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random),
             ("quitter", bouton_quitter), ("save", bouton_save)])

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
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                optimisation.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")

                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_jeu(nom_fichier + ".json", grille, regles)
                            elif nom == "quitter":
                                return fonctions_base.afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic à l'intérieur de la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]  # Basculer l'état de la cellule entre 0 et 1

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
            still_lifes_data.append(graphique.analyser_still_lifes(grille))
            pygame.time.delay(300)

        clock.tick(60)

# Optimisation pour une grille sup à 100


# Fonction principale du jeu
def boucle_jeu_optimisé(taille_grille, regles, cellules_vivantes=None, still_lifes_data=None):
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
    threading.Thread(target=graphique.afficher_graphes_evolutifs, args=(cellules_vivantes, still_lifes_data), daemon=True).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = []
        bouton_random = pygame.Rect(850, 60, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 180, 140, 50)
        bouton_auto = pygame.Rect(850, 240, 140, 50)
        bouton_quitter = pygame.Rect(850, 300, 140, 50)
        bouton_save = pygame.Rect(850, 360, 140, 50)

        boutons.extend([("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random), ("quitter", bouton_quitter), ("save", bouton_save)])

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
                                grille = optimisation.appliquer_regles_optimise(grille, regles)
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                optimisation.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")

                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_jeu(nom_fichier + ".json", grille, regles)
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                            elif nom == "quitter":
                                return fonctions_base.afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = optimisation.appliquer_regles_optimise(grille, regles)
            pygame.time.delay(300)

        clock.tick(60)


# Fonction principale du jeu avec sauvegarde chargée
def boucle_jeu_optimisé_load(grille, regles, cellules_vivantes, still_lifes_date):
    taille_grille = grille.shape[0]  # Taille de la grille déjà chargée
    taille_cellule = 800 // taille_grille  # Calcul de la taille de chaque cellule

    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Lancer le thread pour les graphiques évolutifs
    threading.Thread(
        target=graphique.afficher_graphes_evolutifs, args=(cellules_vivantes, still_lifes_data), daemon=True
    ).start()

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)

        # Afficher boutons de contrôle
        boutons = []
        bouton_random = pygame.Rect(850, 60, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 180, 140, 50)
        bouton_auto = pygame.Rect(850, 240, 140, 50)
        bouton_quitter = pygame.Rect(850, 300, 140, 50)
        bouton_save = pygame.Rect(850, 360, 140, 50)

        boutons.extend(
            [("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random),
             ("quitter", bouton_quitter), ("save", bouton_save)])

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
                                grille = optimisation.appliquer_regles_optimise(grille, regles)
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                optimisation.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")

                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
                                still_lifes_data.append(graphique.analyser_still_lifes(grille))
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_jeu(nom_fichier + ".json", grille, regles)
                            elif nom == "quitter":
                                return fonctions_base.afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic à l'intérieur de la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]  # Basculer l'état de la cellule entre 0 et 1

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            cellules_vivantes.append(graphique.compter_cellules_vivantes(grille))
            still_lifes_data.append(graphique.analyser_still_lifes(grille))
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
            graphique.afficher_graphe_temps_calcul(tailles, temps)

            # Initialisation pour une nouvelle partie
            cellules_vivantes = []  # Liste pour l'évolution des cellules vivantes
            still_lifes_data = []  # Liste pour l'évolution des structures still lifes
            if TAILLE_GRILLE > 100 :
                boucle_jeu_optimisé(TAILLE_GRILLE, REGLES)
            else :
                boucle_jeu(TAILLE_GRILLE, REGLES, cellules_vivantes, still_lifes_data)

        elif action == "load_game":
            nom_fichier = save.demander_nom_fichier(screen)
            if nom_fichier:
                cellules_vivantes = []  # Liste pour l'évolution des cellules vivantes
                still_lifes_data = []
                result = save.load_jeu(nom_fichier + ".json")
                if result:
                    grille, regles = result
                    TAILLE_GRILLE = grille.shape[0]
                    if TAILLE_GRILLE > 100:
                        boucle_jeu_optimisé_load(grille, regles)
                    else :
                        boucle_jeu_load(grille, regles, cellules_vivantes,still_lifes_data)  # Lancer le jeu avec les données chargées
            else:
                print("Nom de fichier non valide.")

        elif action == "quit":
            continue



