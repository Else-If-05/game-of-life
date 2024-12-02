import pygame
import sys

# Initialiser Pygame
pygame.init()

# Définir les paramètres de la grille
TAILLE_GRILLE = 10  # Nombre de cellules par côté
TAILLE_CELLULE = 50  # Taille d'une cellule en pixels
LARGEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE + 200  # Ajout d'espace pour les boutons
HAUTEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
COULEUR_FOND = (34, 139, 34)
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
    {'rect': pygame.Rect(130, 275, 240, 50), 'text': 'Quitter'},
    {'rect': pygame.Rect(LARGEUR_FENETRE - 180, 50, 160, 50), 'text': 'Avancer'},
    {'rect': pygame.Rect(LARGEUR_FENETRE - 180, 120, 160, 50), 'text': 'Auto-Avancer'}
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

# Boucle principale du menu
running = True
auto_advance = False
while running:
    screen.blit(Accueil, (0, 0))
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # if buttons[0]['rect'].collidepoint(event.pos):
                #     Jeu()  # Appeler la fonction Jeu depuis moteur.py
                if buttons[2]['rect'].collidepoint(event.pos):
                    running = False
                elif buttons[3]['rect'].collidepoint(event.pos):
                    # Avancer manuellement
                    grille = appliquer_regles(grille)
                elif buttons[4]['rect'].collidepoint(event.pos):
                    # Activer/désactiver l'auto-avancement
                    auto_advance = not auto_advance

    if auto_advance:
        grille = appliquer_regles(grille)
        pygame.time.delay(100)  # Délai pour l'auto-avancement

    pygame.display.flip()

pygame.quit()
sys.exit()