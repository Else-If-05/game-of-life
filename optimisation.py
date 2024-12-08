import numpy as np
import pygame
import save
import fonctions_base
import time

screen = pygame.display.set_mode((1000, 800))


def mesurer_temps_execution(grille, regles):

    debut = time.time()
    nouvelle_grille = appliquer_regles_optimise(grille, regles)
    fin = time.time()
    duree = fin - debut
    return duree, nouvelle_grille

# optimisation
def afficher_popup(fenetre, temps):
    # Dimensions de la fenêtre pop-up
    largeur, hauteur = 250, 50

    # Positionnement de la pop-up en bas à droite
    x = 750
    y = 500

    # Fond de la pop-up
    pygame.draw.rect(fenetre, (0, 0, 0), (x, y, largeur, hauteur))
    pygame.draw.rect(fenetre, (255, 255, 255), (x + 5, y + 5, largeur - 10, hauteur - 10))

    # Texte de la pop-up
    font_popup = pygame.font.Font(None, 26)
    texte = font_popup.render(f"Temps: {temps:.6f} secondes", True, (0, 0, 0))
    texte_rect = texte.get_rect(center=(x + largeur // 2, y + hauteur // 2))
    fenetre.blit(texte, texte_rect)

    pygame.display.flip()

    # Délai pour fermer la pop-up après 2 secondes
    pygame.time.delay(500)

def appliquer_regles_optimise(grille, regles):

    # Trouver toutes les cellules vivantes
    vivantes = np.argwhere(grille == 1)
    a_verifier = set()

    # Ajouter les cellules vivantes et leurs voisins à la liste à vérifier
    for x, y in vivantes:
        a_verifier.add((x, y))
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            a_verifier.add(((x + dx) % grille.shape[0], (y + dy) % grille.shape[1]))

    nouvelle_grille = grille.copy()

    for x, y in a_verifier:
        voisins_vivants = fonctions_base.compter_voisins(grille, x, y)
        if grille[x, y] == 1:
            # Cellule vivante, vérifier si elle survit
            if voisins_vivants < regles['min_vivants'] or voisins_vivants > regles['max_vivants']:
                nouvelle_grille[x, y] = 0
        else:
            # Cellule morte, vérifier si elle revient à la vie
            if voisins_vivants == regles['revient_a_la_vie']:
                nouvelle_grille[x, y] = 1

    return nouvelle_grille


def boucle_jeu_optimisé_ancien(taille_grille, regles):

            grille = np.zeros((taille_grille, taille_grille), dtype=int)
            auto_mode = False
            clock = pygame.time.Clock()

            taille_cellule = 800 // taille_grille

            while True:
                screen.fill(fonctions_base.COULEUR_FOND)

                # Dessiner la grille
                fonctions_base.dessiner_grille(screen, grille, taille_cellule)

                boutons = []
                bouton_reset = pygame.Rect(850, 50, 140, 50)
                bouton_step = pygame.Rect(850, 100, 140, 50)
                bouton_auto = pygame.Rect(850, 150, 140, 50)
                bouton_random = pygame.Rect(850, 200, 140, 50)
                bouton_quitter = pygame.Rect(850, 250, 140, 50)

                boutons.extend(
                    [("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random),
                     ("quitter", bouton_quitter)])

                for nom, bouton in boutons:
                    texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
                    fonctions_base.dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for nom, bouton in boutons:
                                if bouton.collidepoint(event.pos):
                                    if nom == "reset":
                                        grille = np.zeros((taille_grille, taille_grille), dtype=int)
                                    elif nom == "step":
                                        grille = appliquer_regles_optimise(grille, regles)
                                    elif nom == "auto":
                                        auto_mode = not auto_mode
                                    elif nom == "random":
                                        grille = np.random.randint(2, size=(taille_grille, taille_grille))
                                    elif nom == "quitter":
                                        return
                        x, y = event.pos
                        if x < 800 and y < 800:
                            x //= taille_cellule
                            y //= taille_cellule
                            grille[x, y] = 1 - grille[x, y]

                if auto_mode:
                    grille = appliquer_regles_optimise(grille, regles)
                    pygame.time.delay(300)

                clock.tick(60)

# Fonction principale du jeu
def boucle_jeu_optimisé(taille_grille, regles):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

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
                            elif nom == "step":
                                grille = appliquer_regles_optimise(grille, regles)
                                duree, grille = mesurer_temps_execution(grille, regles)
                                afficher_popup(screen, duree)
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
            grille = appliquer_regles_optimise(grille, regles)
            pygame.time.delay(300)

        clock.tick(60)

# Fonction principale du jeu avec sauvegarde chargée
def boucle_jeu__optimisé_load(grille, regles):
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
                                grille = appliquer_regles_optimise(grille, regles)
                                duree, grille = mesurer_temps_execution(grille, regles)
                                afficher_popup(screen, duree)
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
            grille = appliquer_regles_optimise(grille, regles)
            pygame.time.delay(300)

        clock.tick(60)


