import pygame
import optimisation
import numpy as np
import save
import fonctions_base
import cellules_et_temps

screen = pygame.display.set_mode((1000, 800))


# Fonction principale du jeu
def boucle_jeu(taille_grille, regles):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

    # Liste pour stocker le nombre de cellules vivantes
    #cellules_vivantes = []
    #threading.Thread(target=cellules_et_temps.afficher_graphe_evolutif, args=(cellules_vivantes,), daemon=True).start()

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
                                grille = np.zeros((taille_grille, taille_grille), dtype=int)
                                #cellules_vivantes.clear()
                            elif nom == "step":
                                grille = optimisation.appliquer_regles_optimise(grille, regles)
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                optimisation.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")
                               # cellules_et_temps.cellules_vivantes.append(cellules_et_temps.compter_cellules_vivantes(grille))

                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(nom_fichier + ".json", grille, regles)
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                #cellules_vivantes.append(cellules_et_temps.compter_cellules_vivantes(grille))

                            elif nom == "quitter":
                                return fonctions_base.afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille, regles)
            #cellules_vivantes.append(cellules_et_temps.compter_cellules_vivantes(grille))
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

    while running:
        screen.fill(fonctions_base.COULEUR_FOND)
        fonctions_base.dessiner_grille(screen, grille, taille_cellule)  # Dessiner la grille

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
                                grille = np.zeros((taille_grille, taille_grille), dtype=int)
                            elif nom == "step":
                                grille = fonctions_base.appliquer_regles(grille, regles)
                                duree, grille = optimisation.mesurer_temps_execution(grille, regles)
                                fonctions_base.afficher_popup(screen, duree)
                                print(f"Temps pour cette étape : {duree:.6f} secondes")
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(nom_fichier + ".json", grille, regles)
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
            grille = fonctions_base.appliquer_regles(grille, regles)
            pygame.time.delay(300)

        clock.tick(60)


