import pygame
import numpy as np

# Paramètres de la grille
TAILLE_GRILLE = 10  # Nombre de cellules par côté
TAILLE_CELLULE = 50  # Taille d'une cellule en pixels
ESPACE_BOUTONS = 60  # Hauteur de l'espace dédié aux boutons
LARGEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE
HAUTEUR_FENETRE = TAILLE_GRILLE * TAILLE_CELLULE + ESPACE_BOUTONS

# Couleurs
COULEUR_FOND = (34, 139, 34)
COULEUR_CELLULE_VIVANTE = (0, 0, 0)
COULEUR_CELLULE_MORTE = (200, 200, 200)
COULEUR_BOUTON = (204, 204, 0)
COULEUR_TEXTE = (255, 255, 255)

# Initialisation de pygame
pygame.init()
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Jeu de la Vie")

# Initialisation de la grille
grille = np.zeros((TAILLE_GRILLE, TAILLE_GRILLE), dtype=int)

# Police pour le texte
font = pygame.font.Font(None, 36)


# Fonction pour dessiner la grille
def dessiner_grille(fenetre, grille):
    for x in range(TAILLE_GRILLE):
        for y in range(TAILLE_GRILLE):
            rect = pygame.Rect(x * TAILLE_CELLULE, y * TAILLE_CELLULE + ESPACE_BOUTONS, TAILLE_CELLULE, TAILLE_CELLULE)
            if grille[x, y] == 1:
                pygame.draw.rect(fenetre, COULEUR_CELLULE_VIVANTE, rect)
            else:
                pygame.draw.rect(fenetre, COULEUR_CELLULE_MORTE, rect)
            pygame.draw.rect(fenetre, (0, 0, 0), rect, 1)  # Bordure des cellules


# Fonction pour dessiner les boutons
def dessiner_boutons(fenetre):
    # Bouton "Réinitialiser"
    bouton_reset = pygame.Rect(50, 10, 170, 40)
    pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_reset)
    texte_reset = font.render("Réinitialiser", True, COULEUR_TEXTE)
    fenetre.blit(texte_reset, (61, 15))

    # Bouton "Avancer d'une étape"
    bouton_step = pygame.Rect(300, 10, 150, 40)
    pygame.draw.rect(fenetre, COULEUR_BOUTON, bouton_step)
    texte_step = font.render("Avancer", True, COULEUR_TEXTE)
    fenetre.blit(texte_step, (325, 15))

    return bouton_reset, bouton_step


# Fonction pour appliquer les règles du jeu
def appliquer_regles(grille):
    nouvelle_grille = grille.copy()
    for x in range(grille.shape[0]):
        for y in range(grille.shape[1]):
            voisins_vivants = compter_voisins(grille, x, y)
            if grille[x, y] == 1:
                if voisins_vivants < 2 or voisins_vivants > 3:
                    nouvelle_grille[x, y] = 0  # Meurt par isolement ou surpopulation
            else:
                if voisins_vivants == 3:
                    nouvelle_grille[x, y] = 1  # Revient à la vie
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

# Boucle principale
running = True
en_marche = False  # Pour démarrer/arrêter l'animation

while running:
    fenetre.fill(COULEUR_FOND)
    bouton_reset, bouton_step = dessiner_boutons(fenetre)
    dessiner_grille(fenetre, grille)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if bouton_reset.collidepoint(x, y):
                grille = np.zeros((TAILLE_GRILLE, TAILLE_GRILLE), dtype=int)  # Réinitialise la grille
            elif bouton_step.collidepoint(x, y):
                grille = appliquer_regles(grille)  # Avance d'une étape
            elif y > ESPACE_BOUTONS:  # Clic dans la grille
                x //= TAILLE_CELLULE
                y = (y - ESPACE_BOUTONS) // TAILLE_CELLULE
                grille[x, y] = 1 - grille[x, y]  # Inverse l'état de la cellule
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Espace pour démarrer/arrêter l'animation
                en_marche = not en_marche

    if en_marche:
        grille = appliquer_regles(grille)
        pygame.time.delay(100)  # Contrôle de la vitesse de l'animation

pygame.quit()

