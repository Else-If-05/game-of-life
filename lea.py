#"""""Code avec structures complexes """"

import fonctions_base
import pygame
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

    def update_period(self, new_period, max_x, max_y):
        """Mise à jour de la période et cycle de vie."""
        self.Ship_period = new_period
        self.phase = (self.phase + 1) % self.get_max_phases()  # Passe à la phase suivante

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

    def __init__(self, case_x, case_y, oscillator_type=0):
        self.case_x = case_x
        self.case_y = case_y
        self.color = Oscillator.Oscillator_color
        self.type = oscillator_type  # Type d'oscillateur (0 = blinker, 1 = toad, etc.)
        self.phase = 0  # État courant de l'oscillateur
        self.Oscillator_period = 0  # Période actuelle pour un contrôle précis

    def get_position(self):
        return self.case_x, self.case_y

    def get_matrix(self):
        """Récupère la matrice correspondant à la phase actuelle."""
        if self.type == 0:
            return self.get_blinker(self.phase)
        elif self.type == 1:
            return self.get_toad(self.phase)
        elif self.type == 2:
            return self.get_beacon(self.phase)
        elif self.type == 3:
            return self.get_pulsar(self.phase)

    def update_period(self, new_period, max_x, max_y):
        """Mise à jour de la période et cycle de vie."""
        self.Oscillator_period = new_period
        self.phase = (self.phase + 1) % self.get_max_phases()  # Passe à la phase suivante

    def get_max_phases(self):
        """Retourne le nombre de phases pour un oscillateur donné."""
        if self.type == 0:  # Blinker
            return 2
        elif self.type == 1:  # Toad
            return 2
        elif self.type == 2:  # Beacon
            return 2
        elif self.type == 3:  # Pulsar
            return 3
        return 1

    @staticmethod
    def get_blinker(phase):
        """Phases du Blinker (période 2)."""
        phases = [
            [[1, 1, 1]],
            [[1], [1], [1]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_toad(phase):
        """Phases du Toad (période 2)."""
        phases = [
            [[0, 1, 1, 1], [1, 1, 1, 0]],
            [[0, 1, 0, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 0, 1, 0]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_beacon(phase):
        """Phases du Beacon (période 2)."""
        phases = [
            [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
            [[1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 1]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_pulsar(phase):
        """Phases du Pulsar (période 3)."""
        phases = [
            [[0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0]],
            [[0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
             [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
             [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]]
        ]
        return phases[phase % len(phases)]


class Ship:
    Ship_color = (0, 200, 0)  # Green

    def __init__(self, case_x, case_y, grid):
        self.case_x = case_x
        self.case_y = case_y
        self.grid = grid  # Référence à la grille principale
        self.value = 0  # Identifie le type de ship (0 = glider, etc.)
        self.phase = 0  # État courant du vaisseau
        self.color = Ship.Ship_color  # Add color attribute
        self.Ship_period = 0  # Période actuelle pour un contrôle précis

    def update_period(self, new_period, max_x, max_y):
        """Mise à jour de la période et cycle de vie."""
        self.Ship_period = new_period
        self.phase = (self.phase + 1) % 8  # Passe à la phase suivante

    def move(self, max_x, max_y, reset_threshold=3):
        self.case_x = (self.case_x + 1) % max_x  # Mouvement horizontal
        self.case_y = (self.case_y + 1) % max_y  # Mouvement vertical


    def get_position(self):
        return self.case_x, self.case_y

    def get_matrix(self):
        """Récupère la matrice correspondant à la phase actuelle."""
        #self.phase += 1
        if self.phase >= 8:  # 8 est le nombre maximum de phases (modifiable)
            self.phase = 0

        if self.value == 0:
            return self.get_glider(self.phase)
        elif self.value == 1:
            return self.get_light_weight_ship(self.phase)
        elif self.value == 2:
            return self.get_middle_weight_ship(self.phase)
        elif self.value == 3:
            return self.get_heavy_weight_ship(self.phase)

    @staticmethod
    def get_glider(phase):
        """Phases du Glider."""
        phases = [
            [[0, 0, 1], [1, 0, 1], [0, 1, 1]],
            [[1, 0, 0], [0, 1, 1], [1, 1, 0]],
            [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
            [[0, 0, 1], [1, 0, 1], [0, 1, 1]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_light_weight_ship(phase):
        """Phases du Lightweight Ship."""
        phases = [
            [[0, 1, 1, 1, 1], [1, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 0, 0, 1, 0]],
            [[1, 0, 1, 1, 1], [0, 1, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 0, 0]],
            [[0, 0, 1, 1, 0], [1, 0, 0, 0, 1], [0, 1, 1, 0, 1], [1, 1, 0, 1, 0]],
            [[1, 1, 0, 1, 1], [0, 1, 1, 0, 0], [1, 0, 1, 1, 1], [0, 0, 0, 0, 1]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_middle_weight_ship(phase):
        """Phases du Middleweight Ship."""
        phases = [
            [[0, 1, 1, 1, 1, 0], [1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1]],
            [[1, 0, 1, 1, 1, 0], [0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 1, 1, 0, 1, 0], [1, 0, 1, 1, 1, 1]],
            [[0, 1, 0, 1, 1, 1], [1, 0, 1, 0, 0, 1], [0, 1, 1, 0, 0, 0], [1, 1, 0, 1, 0, 1], [0, 1, 1, 1, 0, 0]],
            [[1, 1, 1, 0, 1, 1], [0, 1, 0, 1, 0, 0], [1, 0, 1, 0, 1, 1], [0, 1, 1, 1, 0, 1], [1, 1, 0, 1, 1, 0]]
        ]
        return phases[phase % len(phases)]

    @staticmethod
    def get_heavy_weight_ship(phase):
        """Phases du Heavyweight Ship."""
        phases = [
            [[0, 1, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1, 1]],
            [[1, 0, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 1, 1]],
            [[0, 1, 0, 1, 1, 1, 0], [1, 0, 1, 0, 0, 0, 1], [0, 1, 0, 0, 0, 1, 1], [1, 0, 1, 1, 0, 0, 0], [0, 1, 1, 1, 1, 0, 0]],
            [[1, 1, 1, 0, 1, 1, 1], [0, 1, 0, 1, 0, 0, 0], [1, 0, 1, 0, 1, 1, 1], [0, 1, 0, 1, 1, 1, 0], [1, 1, 1, 0, 1, 0, 1]]
        ]
        return phases[phase % len(phases)]
def spawn_random_structure(max, x, y, key, grid):
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
        stru = Oscillator(x, y, oscillator_type=0)  # Blinker
        stru.grid = grid  # Lier la grille à l'oscillateur
        return stru
    elif key == pygame.K_g:
        stru = Oscillator(x, y, oscillator_type=1)  # Toad
        stru.grid = grid  # Lier la grille à l'oscillateur
        return stru
    elif key == pygame.K_h:
        stru = Oscillator(x, y, oscillator_type=2)  # Beacon
        stru.grid = grid  # Lier la grille à l'oscillateur
        return stru
    elif key == pygame.K_i:
        stru = Oscillator(x, y, oscillator_type=3)  # Pulsar
        stru.grid = grid  # Lier la grille à l'oscillateur
        return stru

    elif key == pygame.K_j:
        stru = Ship(x, y, grid)  # Lier la grille au vaisseau
        stru.value = 0  # Glider
        return stru
    elif key == pygame.K_k:
        stru = Ship(x, y, grid)  # Lier la grille au vaisseau
        stru.value = 1  # Light weight ship
        return stru
    elif key == pygame.K_l:
        stru = Ship(x, y, grid)  # Lier la grille au vaisseau
        stru.value = 2  # Middle weight ship
        return stru
    elif key == pygame.K_m:
        stru = Ship(x, y, grid)  # Lier la grille au vaisseau
        stru.value = 3  # Heavy weight ship
        return stru

    return None


def update_structures(structures, max_x, max_y):
    for structure in structures:
        if isinstance(structure, Oscillator):
            structure.update_period(structure.Oscillator_period, max_x, max_y)
        elif isinstance(structure, Ship):
            structure.update_period(structure.Ship_period, max_x, max_y)
            structure.move(max_x, max_y)


def dessiner_grille(fenetre, grille, taille_cellule, scale_factor, taille_grille, deplacement_x, deplacement_y,
                    structures):
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
                    corrected_x = (ship_x + j) % grille.shape[0]
                    corrected_y = (ship_y + i) % grille.shape[1]
                    rect = pygame.Rect(offset_x + corrected_x * taille_cellule * scale_factor,
                                       offset_y + corrected_y * taille_cellule * scale_factor,
                                       taille_cellule * scale_factor,
                                       taille_cellule * scale_factor)

                    pygame.draw.rect(fenetre, structure.color, rect)


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
        if keys[pygame.K_F1]:
            scale_factor *= 1.02
        if keys[pygame.K_F2]:
            scale_factor = max(1, scale_factor / 1.02)


        # Place structures in the grid
        grille_temp = grille.copy()
        #for structure in structures:
           # placer_structure_dans_grille(grille_temp, structure)

        # Apply rules to the entire grid including structures
        if auto_mode:
            grille = fonctions_base.appliquer_regles(grille_temp, regles)
            # Update structures
            update_structures(structures, taille_grille, taille_grille)
            pygame.time.delay(300)

        dessiner_grille(screen, grille, taille_cellule, scale_factor, taille_grille, deplacement_x, deplacement_y,
                        structures)

        boutons = []
        bouton_random = pygame.Rect(850, 50, 140, 50)
        bouton_reset = pygame.Rect(850, 120, 140, 50)
        bouton_step = pygame.Rect(850, 230, 140, 50)
        bouton_auto = pygame.Rect(850, 300, 140, 50)
        boutons.extend(
            [("reset", bouton_reset), ("step", bouton_step), ("auto", bouton_auto), ("random", bouton_random)])

        for nom, bouton in boutons:
            texte = "Auto: ON" if auto_mode and nom == "auto" else nom.capitalize()
            fonctions_base.dessiner_bouton(screen, bouton, texte, bouton.collidepoint(pygame.mouse.get_pos()))

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
                                # Update structures
                                update_structures(structures, taille_grille, taille_grille)
                                grille = fonctions_base.appliquer_regles(grille_temp, regles)

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
                if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g,
                                 pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    offset_x = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_x
                    offset_y = ((800 - taille_grille * taille_cellule * scale_factor) / 2) + deplacement_y
                    grid_x = int((mouse_x - offset_x) / (taille_cellule * scale_factor))
                    grid_y = int((mouse_y - offset_y) / (taille_cellule * scale_factor))

                    if 0 <= grid_x < taille_grille and 0 <= grid_y < taille_grille:
                        structure = spawn_random_structure(taille_grille, grid_x, grid_y, event.key, grille)
                        if structure:
                            structures.append(structure)

        clock.tick(60)


if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = fonctions_base.afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = fonctions_base.demander_taille(screen)
            REGLES = fonctions_base.demander_regles(screen)
            boucle_jeu(TAILLE_GRILLE, REGLES)
