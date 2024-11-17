import pygame
import sys

# Initialiser Pygame
pygame.init()

# Définir les paramètres de la grille
TAILLE_GRILLE = 10  # Nombre de cellules par côté
TAILLE_CELLULE = 50  # Taille d'une cellule en pixels
LARGEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE
HAUTEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE

# Définir les couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

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

# Définir la police
font = pygame.font.Font(None, 36)


# Fonction pour dessiner les boutons
def draw_buttons():
    for button in buttons:
        # Vérifier si la souris est sur le bouton
        if button['rect'].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, DARK_GRAY, button['rect'])
        else:
            pygame.draw.rect(screen, GRAY, button['rect'])

        # Dessiner le texte au centre du bouton
        text_surface = font.render(button['text'], True, BLACK)
        text_rect = text_surface.get_rect(center=button['rect'].center)
        screen.blit(text_surface, text_rect)


# Boucle principale du programme
running = True
while running:
    screen.blit(Accueil, (0, 0))  # Dessiner l'image de fond
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                for button in buttons:
                    if button['rect'].collidepoint(event.pos):
                        print(f"{button['text']} cliqué!")

    pygame.display.flip()

# Quitter Pygame
pygame.quit()
sys.exit()