import pygame
import sys
import numpy as np
import save
import optimisation


# Initialiser Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
COULEUR_FOND = (240, 248, 255)
COULEUR_BOUTON = (70, 130, 180)
COULEUR_BOUTON_SURVOL = (100, 149, 237)
COULEUR_TEXTE = (0, 0, 0)

# Police
font = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)


def demander_regles(fenetre):
    input_boxes = [
        {'rect': pygame.Rect(300, 200, 200, 50), 'text': '', 'label': 'Min voisins pour survivre :'},
        {'rect': pygame.Rect(300, 300, 200, 50), 'text': '', 'label': 'Max voisins pour survivre :'},
        {'rect': pygame.Rect(300, 400, 200, 50), 'text': '', 'label': 'Voisins pour revivre :'}
    ]

    bouton_valider = pygame.Rect(350, 500, 100, 50)
    font = pygame.font.Font(None, 25)
    active_box = None
    running = True
    titre_surface = font.render("Changez les paramètres si vous le souhaitez, sinon cliquez directement sur valider", True, COULEUR_TEXTE)
    instruction_surface = font.render("Veuillez entrer les règles du jeu :", True, COULEUR_TEXTE)

    while running:
        fenetre.fill(COULEUR_FOND)
        fenetre.blit(titre_surface, (50, 50))
        fenetre.blit(instruction_surface, (300, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in input_boxes:
                        if box['rect'].collidepoint(event.pos):
                            active_box = box
                    if bouton_valider.collidepoint(event.pos):
                        try:
                            min_vivants = int(input_boxes[0]['text'])
                            max_vivants = int(input_boxes[1]['text'])
                            revient_a_la_vie = int(input_boxes[2]['text'])
                            return {
                                'min_vivants': min_vivants,
                                'max_vivants': max_vivants,
                                'revient_a_la_vie': revient_a_la_vie
                            }
                        except ValueError:
                            print("Entrée invalide. Les règles par défaut seront utilisées.")
                            return {
                                'min_vivants': 2,
                                'max_vivants': 3,
                                'revient_a_la_vie': 3
                            }
            elif event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        active_box = None
                    elif event.key == pygame.K_BACKSPACE:
                        active_box['text'] = active_box['text'][:-1]
                    else:
                        active_box['text'] += event.unicode

        for box in input_boxes:
            pygame.draw.rect(fenetre, COULEUR_BOUTON, box['rect'], 2)
            label_surface = font.render(box['label'], True, COULEUR_TEXTE)
            fenetre.blit(label_surface, (box['rect'].x - 250, box['rect'].y + 10))
            text_surface = font.render(box['text'], True, COULEUR_TEXTE)
            fenetre.blit(text_surface, (box['rect'].x + 5, box['rect'].y + 10))

        pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_valider)
        valider_surface = font.render("Valider", True, COULEUR_TEXTE)
        fenetre.blit(valider_surface, (bouton_valider.x + 10, bouton_valider.y + 10))

        pygame.display.flip()
# Fonction pour dessiner un bouton
def dessiner_bouton(fenetre, rect, texte, survole):
    couleur = COULEUR_BOUTON_SURVOL if survole else COULEUR_BOUTON
    pygame.draw.rect(fenetre, couleur, rect, border_radius=10)
    texte_surface = font.render(texte, True, COULEUR_TEXTE)
    texte_rect = texte_surface.get_rect(center=rect.center)
    fenetre.blit(texte_surface, texte_rect)


def afficher_accueil():
    boutons = [
        {'rect': pygame.Rect(200, 150, 300, 60), 'text': "Nouvelle Partie"},
        {'rect': pygame.Rect(200, 250, 300, 60), 'text': "Charger une Partie"},
        {'rect': pygame.Rect(200, 350, 300, 60), 'text': "Quitter"}
    ]

    accueil = True
    while accueil:
        screen.fill(COULEUR_FOND)
        titre_surface = font.render("Jeu de la Vie", True, COULEUR_TEXTE)
        titre_rect = titre_surface.get_rect(center=(400, 80))
        screen.blit(titre_surface, titre_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for bouton in boutons:
                        if bouton['rect'].collidepoint(event.pos):
                            if bouton['text'] == "Nouvelle Partie":
                                return "new_game"
                            if bouton['text'] == "Charger une Partie":
                                return "load_game"
                            elif bouton['text'] == "Quitter":
                                pygame.quit()
                                sys.exit()

        for bouton in boutons:
            survole = bouton['rect'].collidepoint(pygame.mouse.get_pos())
            dessiner_bouton(screen, bouton['rect'], bouton['text'], survole)

        pygame.display.flip()

# Fonction pour dessiner la grille
def dessiner_grille(fenetre, grille, taille_cellule):
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            rect = pygame.Rect(x * taille_cellule, y * taille_cellule, taille_cellule, taille_cellule)
            if grille[x, y] == 1:
                pygame.draw.rect(fenetre, BLACK, rect)
            else:
                pygame.draw.rect(fenetre, WHITE, rect)
            pygame.draw.rect(fenetre, GRAY, rect, 1)


# Fonction pour appliquer les règles du jeu
def appliquer_regles(grille, regles):
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:
                if voisins_vivants < regles['min_vivants'] or voisins_vivants > regles['max_vivants']:
                    nouvelle_grille[x, y] = 0
            else:
                if voisins_vivants == regles['revient_a_la_vie']:
                    nouvelle_grille[x, y] = 1
    return nouvelle_grille


# Fonction pour compter les voisins vivants
def compter_voisins(grille, x, y):
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    total = sum(grille[(x + dx) % grille.shape[0], (y + dy) % grille.shape[1]] for dx, dy in voisins)
    return total



def demander_taille(fenetre):
    input_boxes = [
        {'rect': pygame.Rect(300, 200, 200, 50), 'text': '', 'label': 'Taille de la map:'},
    ]
    bouton_valider = pygame.Rect(350, 500, 100, 50)
    font = pygame.font.Font(None, 25)
    active_box = None
    error_message = ""
    running = True

    while running:
        fenetre.fill(COULEUR_FOND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in input_boxes:
                        if box['rect'].collidepoint(event.pos):
                            active_box = box
                    if bouton_valider.collidepoint(event.pos):
                        try:
                            taille = int(input_boxes[0]['text'])
                            if taille >= 50:
                                return taille
                            else:
                                error_message = "La taille doit être >= 50."
                        except ValueError:
                            error_message = "Entrée invalide. Veuillez entrer un nombre entier."
            elif event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_RETURN:
                        active_box = None
                    elif event.key == pygame.K_BACKSPACE:
                        active_box['text'] = active_box['text'][:-1]
                    else:
                        active_box['text'] += event.unicode

        # Dessiner les boîtes d'entrée
        for box in input_boxes:
            pygame.draw.rect(fenetre, COULEUR_BOUTON, box['rect'], 2)
            label_surface = font.render(box['label'], True, COULEUR_TEXTE)
            fenetre.blit(label_surface, (box['rect'].x - 250, box['rect'].y + 10))
            text_surface = font.render(box['text'], True, COULEUR_TEXTE)
            fenetre.blit(text_surface, (box['rect'].x + 5, box['rect'].y + 10))

        # Dessiner le bouton Valider
        pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_valider)
        valider_surface = font.render("Valider", True, COULEUR_TEXTE)
        fenetre.blit(valider_surface, (bouton_valider.x + 10, bouton_valider.y + 10))

        # Afficher le message d'erreur s'il existe
        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))  # Texte rouge pour l'erreur
            fenetre.blit(error_surface, (300, 300))  # Position du message d'erreur

        pygame.display.flip()

# Fonction principale du jeu
def boucle_jeu(taille_grille, regles):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()

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
                            elif nom == "step":
                                grille = appliquer_regles(grille, regles)
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "save":
                                nom_fichier = save.demander_nom_fichier(screen)
                                if nom_fichier:
                                    save.save_game(nom_fichier + ".json", grille, regles)
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                            elif nom == "quitter":
                                return afficher_accueil()
                x, y = event.pos
                if x < 800 and y < 800:  # Clic dans la grille
                    x //= taille_cellule
                    y //= taille_cellule
                    grille[x, y] = 1 - grille[x, y]

        if auto_mode:
            grille = appliquer_regles(grille, regles)
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

def boucle_jeu_optimisé(taille_grille, regles):
            """
            Boucle de jeu optimisée pour les grandes grilles.
            """
            grille = np.zeros((taille_grille, taille_grille), dtype=int)
            auto_mode = False
            clock = pygame.time.Clock()

            taille_cellule = 800 // taille_grille

            while True:
                screen.fill(COULEUR_FOND)

                # Dessiner la grille
                dessiner_grille(screen, grille, taille_cellule)

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
                    dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

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
                                        grille = optimisation.appliquer_regles_optimise(grille, regles)
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
                    grille = optimisation.appliquer_regles_optimise(grille, regles)
                    pygame.time.delay(300)

                clock.tick(60)


# Programme principal
if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))  # Fenêtre plus large pour le panneau
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = demander_taille(screen)

            REGLES = demander_regles(screen)
            if TAILLE_GRILLE > 100:
                boucle_jeu_optimisé(TAILLE_GRILLE, REGLES)
            else:
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
            continue  # Retour à l'écran d'accueil
