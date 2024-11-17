import pygame
import sys
import numpy as np

# Initialiser Pygame
pygame.init()

# Définir les paramètres de la grille
TAILLE_GRILLE = 10  # Nombre de cellules par côté
TAILLE_CELLULE = 50  # Taille d'une cellule en pixels
LARGEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE
HAUTEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
COULEUR_FOND = (34, 139, 34)
COULEUR_CELLULE_VIVANTE = (0, 0, 0)
COULEUR_CELLULE_MORTE = (200, 200, 200)
COULEUR_BOUTON = (204, 204, 0)
COULEUR_TEXTE = (255, 255, 255)

# Définir la taille de la fenêtre
screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption('Jeu de la vie')

# Charger l'image de fond
Accueil = pygame.image.load('accueil.png')
Accueil = pygame.transform.scale(Accueil, (LARGEUR_FENETRE, HAUTEUR_FENETRE))

# Définir les caractéristiques des boutons
buttons = [
    {'rect': pygame.Rect(130, 125, 240, 50), 'text': 'Nouvelle Partie'},
    {'rect': pygame.Rect(130, 200, 240, 50), 'text': 'Charger une Partie'},
    {'rect': pygame.Rect(130, 275, 240, 50), 'text': 'Quitter'}
]

# Police
font = pygame.font.Font(None, 36)

def draw_buttons():
    for button in buttons:
        if button['rect'].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, button['rect'])
        else:
            pygame.draw.rect(screen, GRAY, button['rect'])
        text_surface = font.render(button['text'], True, BLACK)
        text_rect = text_surface.get_rect(center=button['rect'].center)
        screen.blit(text_surface, text_rect)

# Fonction pour afficher l'écran de la nouvelle partie
def Jeu():
    grille = np.zeros((TAILLE_GRILLE, TAILLE_GRILLE), dtype=int)
    running = True
    while running:
        screen.fill(COULEUR_FOND)
        dessiner_grille(screen, grille)
        bouton_reset, bouton_step = dessiner_boutons(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_reset.collidepoint(x, y):
                    grille = np.zeros((TAILLE_GRILLE, TAILLE_GRILLE), dtype=int)
                elif bouton_step.collidepoint(x, y):
                    grille = appliquer_regles(grille)
                elif y > 60:  # Clic dans la grille
                    x //= TAILLE_CELLULE
                    y = (y - 60) // TAILLE_CELLULE
                    grille[x, y] = 1 - grille[x, y]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Retourne au menu principal

        pygame.time.delay(100)

def dessiner_grille(fenetre, grille):
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE + 60, TAILLE_CELLULE, TAILLE_CELLULE)
            if grille[x, y] == 1:
                pygame.draw.rect(fenetre, COULEUR_CELLULE_VIVANTE, rect)
            else:
                pygame.draw.rect(fenetre, COULEUR_CELLULE_MORTE, rect)
            pygame.draw.rect(fenetre, (0, 0, 0), rect, 1)

def dessiner_boutons(fenetre):
    bouton_reset = pygame.Rect(50, 10, 170, 40)
    pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_reset)
    texte_reset = font.render("Réinitialiser", True, COULEUR_TEXTE)
    fenetre.blit(texte_reset, (61, 15))

    bouton_step = pygame.Rect(300, 10, 150, 40)
    pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_step)
    texte_step = font.render("Avancer", True, COULEUR_TEXTE)
    fenetre.blit(texte_step, (325, 15))

    return bouton_reset, bouton_step

def appliquer_regles(grille):
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:
                if voisins_vivants < 2 or voisins_vivants > 3:
                    nouvelle_grille[x, y] = 0
            else:
                if voisins_vivants == 3:
                    nouvelle_grille[x, y] = 1
    return nouvelle_grille

def compter_voisins(grille, x, y):
    voisins = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    total = sum(grille[(x + dx) % grille.shape[0], (y + dy) % grille.shape[1]] for dx, dy in voisins)
    return total

# Boucle principale du menu
running = True
while running:
    screen.blit(Accueil, (0, 0))
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if buttons[0]['rect'].collidepoint(event.pos):
                    Jeu()
                elif buttons[2]['rect'].collidepoint(event.pos):
                    running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
