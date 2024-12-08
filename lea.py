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



#avec structure
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
            grille = fonctions_base.appliquer_regles(grille_temp, regles)
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



if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = fonctions_base.afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = fonctions_base.demander_taille(screen)
            REGLES = fonctions_base.demander_regles(screen)
            boucle_jeu(TAILLE_GRILLE, REGLES)
