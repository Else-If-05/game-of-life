import random
import pygame
import sys
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
COULEUR_FOND = (240, 248, 255)
COULEUR_BOUTON = (70, 130, 180)
COULEUR_BOUTON_SURVOL = (100, 149, 237)
COULEUR_TEXTE = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 48)

# Classes for structures
class Constant:
    Constant_color = (0, 0, 200)  # Blue

    def __init__(self, case_x, case_y):
        self.case_x = case_x
        self.case_y = case_y
        self.color = Constant.Constant_color
        self.value = 0

    def get_position(self):
        return self.case_x, self.case_y

    def get_matrix(self):
        if self.value == 0:
            return self.get_block()
        elif self.value == 1:
            return self.get_bee_hive()
        elif self.value == 2:
            return self.get_loaf()
        elif self.value == 3:
            return self.get_boat()
        elif self.value == 4:
            return self.get_tub()

    @staticmethod
    def get_block():
        return [[1, 1],
                [1, 1]]

    @staticmethod
    def get_bee_hive():
        return [[0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 1, 1, 0]]

    @staticmethod
    def get_loaf():
        return [[0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 1, 0, 1],
                [0, 0, 1, 0]]

    @staticmethod
    def get_boat():
        return [[1, 1, 0],
                [1, 0, 1],
                [0, 1, 0]]

    @staticmethod
    def get_tub():
        return [[0, 1, 0],
                [1, 0, 1],
                [0, 1, 0]]

class Oscillator:
    Oscillator_color = (200, 0, 0)  # Red

    def __init__(self, case_x, case_y):
        self.case_x = case_x
        self.case_y = case_y
        self.color = Oscillator.Oscillator_color
        self.value = 0
        self.Oscillator_period = 0

    def update_period(self, new_period, max_x, max_y):
        self.Oscillator_period = new_period
        matrix = self.get_matrix()
        matrix_height = len(matrix)
        matrix_width = len(matrix[0])

        self.case_x = max(0, min(self.case_x, max_x - matrix_width))
        self.case_y = max(0, min(self.case_y, max_y - matrix_height))

    def get_position(self):
        return self.case_x, self.case_y

    def get_matrix(self):
        if self.Oscillator_period == 0:
            return self.get_blinker()
        elif self.Oscillator_period == 1:
            return self.get_toad()
        elif self.Oscillator_period == 2:
            return self.get_beacon()
        elif self.Oscillator_period == 3:
            return self.get_pulsar()
        elif self.Oscillator_period == 4:
            return self.get_penta_decathlon()

    @staticmethod
    def get_blinker():
        return [[1],
                [1],
                [1]]

    @staticmethod
    def get_toad():
        return [[0, 0, 1, 0],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [0, 1, 0, 0]]

    @staticmethod
    def get_beacon():
        return [[1, 1, 0, 0],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [0, 0, 1, 1]]

    @staticmethod
    def get_pulsar():
        return [[0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]]

    @staticmethod
    def get_penta_decathlon():
        return [[0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]]

class Ship:
    Ship_color = (0, 200, 0)  # Green

    def __init__(self, case_x, case_y):
        self.case_x = case_x
        self.case_y = case_y
        self.color = Ship.Ship_color
        self.value = 0

    def move(self, max_x, max_y):
        matrix = self.get_matrix()
        matrix_height = len(matrix)
        matrix_width = len(matrix[0])

        # Move the ship downwards
        self.case_y = (self.case_y + 1) % max_y  # Wrap around vertically

    def get_position(self):
        return self.case_x, self.case_y

    def get_matrix(self):
        if self.value == 0:
            return self.get_glider()
        elif self.value == 1:
            return self.get_light_weight_ship()
        elif self.value == 2:
            return self.get_middle_weight_ship()
        elif self.value == 3:
            return self.get_heavy_weight_ship()

    @staticmethod
    def get_glider():
        return [[0, 0, 1],
                [1, 0, 1],
                [0, 1, 1]]

    @staticmethod
    def get_light_weight_ship():
        return [[0, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 1],
                [1, 0, 0, 1, 0]]

    @staticmethod
    def get_middle_weight_ship():
        return [[0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1]]

    @staticmethod
    def get_heavy_weight_ship():
        return [[0, 0, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1, 1]]

def spawn_random_structure(max, x, y, key):
    if key == pygame.K_a:
        stru = Constant(x, y)
        stru.value = 0  # Block
        return stru
    elif key == pygame.K_b:
        stru = Constant(x, y)
        stru.value = 1  # Bee hive
        return stru
    elif key == pygame.K_c:
        stru = Constant(x, y)
        stru.value = 2  # Loaf
        return stru
    elif key == pygame.K_d:
        stru = Constant(x, y)
        stru.value = 3  # Boat
        return stru
    elif key == pygame.K_e:
        stru = Constant(x, y)
        stru.value = 4  # Tub
        return stru
    elif key == pygame.K_f:
        stru = Oscillator(x, y)
        stru.Oscillator_period = 0  # Blinker
        return stru
    elif key == pygame.K_g:
        stru = Oscillator(x, y)
        stru.Oscillator_period = 1  # Toad
        return stru
    elif key == pygame.K_h:
        stru = Oscillator(x, y)
        stru.Oscillator_period = 2  # Beacon
        return stru
    elif key == pygame.K_i:
        stru = Oscillator(x, y)
        stru.Oscillator_period = 3  # Pulsar
        return stru
    elif key == pygame.K_j:
        stru = Oscillator(x, y)
        stru.Oscillator_period = 4  # Penta-decathlon
        return stru
    elif key == pygame.K_k:
        stru = Ship(x, y)
        stru.value = 0  # Glider
        return stru
    elif key == pygame.K_l:
        stru = Ship(x, y)
        stru.value = 1  # Light weight ship
        return stru
    elif key == pygame.K_m:
        stru = Ship(x, y)
        stru.value = 2  # Middle weight ship
        return stru
    elif key == pygame.K_n:
        stru = Ship(x, y)
        stru.value = 3  # Heavy weight ship
        return stru

    return None

def update_structures(structures, max_x, max_y):
    for structure in structures:
        if isinstance(structure, Oscillator):
            new_period = (structure.Oscillator_period + 1) % 5
            structure.update_period(new_period, max_x, max_y)
        elif isinstance(structure, Ship):
            structure.move(max_x, max_y)

def dessiner_bouton(fenetre, rect, texte, survole):
    couleur = COULEUR_BOUTON_SURVOL if survole else COULEUR_BOUTON
    pygame.draw.rect(fenetre, couleur, rect, border_radius=10)
    texte_surface = font.render(texte, True, COULEUR_TEXTE)
    texte_rect = texte_surface.get_rect(center=rect.center)
    fenetre.blit(texte_surface, texte_rect)

def dessiner_grille(fenetre, grille, taille_cellule, scale_factor, taille_grille, deplacement_x, deplacement_y, structures):
    offset_x = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_x
    offset_y = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_y

    # Draw the grid
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            rect = pygame.Rect(offset_x + x * taille_cellule * scale_factor,
                               offset_y + y * taille_cellule * scale_factor,
                               taille_cellule * scale_factor,
                               taille_cellule * scale_factor)
            if grille[x, y] == 1:
                pygame.draw.rect(fenetre, BLACK, rect)
            else:
                pygame.draw.rect(fenetre, WHITE, rect)
            pygame.draw.rect(fenetre, GRAY, rect, 1)

    # Draw structures
    for structure in structures:
        ship_x, ship_y = structure.get_position()
        matrix = structure.get_matrix()
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if cell == 1:
                    rect = pygame.Rect(offset_x + (ship_x + j) * taille_cellule * scale_factor,
                                       offset_y + (ship_y + i) * taille_cellule * scale_factor,
                                       taille_cellule * scale_factor,
                                       taille_cellule * scale_factor)
                    pygame.draw.rect(fenetre, structure.color, rect)

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

def compter_voisins(grille, x, y):
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    total = sum(grille[(x + dx) % grille.shape[0], (y + dy) % grille.shape[1]] for dx, dy in voisins)
    return total

def placer_structure_dans_grille(grille, structure):
    x, y = structure.get_position()
    matrix = structure.get_matrix()
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 1:
                if 0 <= x + j < grille.shape[0] and 0 <= y + i < grille.shape[1]:
                    grille[x + j, y + i] = 1

def boucle_jeu(taille_grille, regles):
    taille_cellule = 800 // taille_grille
    grille = np.zeros((taille_grille, taille_grille), dtype=int)
    running = True
    auto_mode = False
    clock = pygame.time.Clock()
    scale_factor = 1.0
    deplacement_x = 0
    deplacement_y = 0
    structures = []

    while running:
        screen.fill(COULEUR_FOND)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            deplacement_y += 10
        if keys[pygame.K_DOWN]:
            deplacement_y -= 10
        if keys[pygame.K_LEFT]:
            deplacement_x += 10
        if keys[pygame.K_RIGHT]:
            deplacement_x -= 10
        if keys[pygame.K_KP_PLUS]:
            scale_factor *= 1.02
        if keys[pygame.K_KP_MINUS]:
            scale_factor = max(1, scale_factor / 1.02)

        # Update structures
        update_structures(structures, taille_grille, taille_grille)

        # Place structures in the grid
        grille_temp = grille.copy()
        for structure in structures:
            placer_structure_dans_grille(grille_temp, structure)

        # Apply rules to the entire grid including structures
        if auto_mode:
            grille = appliquer_regles(grille_temp, regles)
            pygame.time.delay(300)

        dessiner_grille(screen, grille, taille_cellule, scale_factor, taille_grille, deplacement_x, deplacement_y, structures)

        boutons = []
        bouton_random = pygame.Rect(850, 50, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 230, 140, 50)
        bouton_auto = pygame.Rect(850, 300, 140, 50)
        boutons.extend([("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random)])

        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for nom, bouton in boutons:
                        if bouton.collidepoint(event.pos):
                            if nom == "reset":
                                grille = np.zeros((taille_grille, taille_grille), dtype=int)
                                structures.clear()
                            elif nom == "step":
                                grille = appliquer_regles(grille_temp, regles)
                            elif nom == "auto":
                                auto_mode = not auto_mode
                            elif nom == "random":
                                grille = np.random.randint(2, size=(taille_grille, taille_grille))
                x, y = event.pos
                offset_x = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_x
                offset_y = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_y
                x = (x - offset_x) / (taille_cellule * scale_factor)
                y = (y - offset_y) / (taille_cellule * scale_factor)
                if 0 <= x < grille.shape[0] and 0 <= y < grille.shape[1]:
                    x, y = int(x), int(y)
                    grille[x, y] = 1 - grille[x, y]

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    offset_x = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_x
                    offset_y = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_y
                    grid_x = int((mouse_x - offset_x) / (taille_cellule * scale_factor))
                    grid_y = int((mouse_y - offset_y) / (taille_cellule * scale_factor))

                    if 0 <= grid_x < taille_grille and 0 <= grid_y < taille_grille:
                        structure = spawn_random_structure(taille_grille, grid_x, grid_y, event.key)
                        if structure:
                            structures.append(structure)

        clock.tick(60)

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
                if event.button == 1:  # Left click
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

        for box in input_boxes:
            pygame.draw.rect(fenetre, COULEUR_BOUTON, box['rect'], 2)
            label_surface = font.render(box['label'], True, COULEUR_TEXTE)
            fenetre.blit(label_surface, (box['rect'].x - 250, box['rect'].y + 10))
            text_surface = font.render(box['text'], True, COULEUR_TEXTE)
            fenetre.blit(text_surface, (box['rect'].x + 5, box['rect'].y + 10))

        pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_valider)
        valider_surface = font.render("Valider", True, COULEUR_TEXTE)
        fenetre.blit(valider_surface, (bouton_valider.x + 10, bouton_valider.y + 10))

        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))
            fenetre.blit(error_surface, (300, 300))

        pygame.display.flip()

def demander_regles(fenetre):
    input_boxes = [
        {'rect': pygame.Rect(300, 200, 200, 50), 'text': '', 'label': 'Min voisins pour survivre :'},
        {'rect': pygame.Rect(300, 300, 200, 50), 'text': '', 'label': 'Max voisins pour survivre :'},
        {'rect': pygame.Rect(300, 400, 200, 50), 'text': '', 'label': 'Voisins pour revivre :' }
    ]

    bouton_valider = pygame.Rect(350, 500, 100, 50)
    font = pygame.font.Font(None, 25)
    active_box = None
    running = True
    titre_surface = font.render("Changez les paramètres si vous le souhaitez, sinon cliquez directement sur valider",
                                True, COULEUR_TEXTE)
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

if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = demander_taille(screen)
            REGLES = demander_regles(screen)
            boucle_jeu(TAILLE_GRILLE, REGLES)
