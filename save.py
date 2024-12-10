import json
import numpy as np
import pygame

def save_jeu(fichier, grille, regles):
    try:
        game_state = {
            "taille_grille": grille.shape[0],
            "regles": regles,
            "grille": grille.tolist(),
        }

        with open(fichier, 'w') as file:
            json.dump(game_state, file)

        print(f"Jeu sauvegarde : {fichier}")
    except Exception as e:
        print(f"Erreur : {e}")

def load_jeu(fichier):
    try:
        with open(fichier, 'r') as file:
            game_state = json.load(file)
            print("Jeu load :", game_state)

        taille_grille = game_state["taille_grille"]
        regles = game_state["regles"]
        grille = np.array(game_state["grille"], dtype=int)

        print(f" Jeu load de :  {fichier}")
        return grille, regles

    except Exception as e:
        print(f"Erreur: {e}")
        return None

def demander_nom_fichier(screen):
    input_box = pygame.Rect(300, 350, 400, 50)
    font = pygame.font.Font(None, 36)
    actif = True
    texte = ""
    running = True

    while running:
        screen.fill((240, 248, 255))  # Fond blanc cassé

        # Affiche la boîte de texte
        pygame.draw.rect(screen, (200, 200, 200), input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        text_surface = font.render(texte, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        # Affiche un texte explicatif
        message = font.render("Entrez le nom du fichier et appuyez sur Entrée", True, (0, 0, 0))
        screen.blit(message, (200, 250))

        pygame.display.flip()

        # Clavier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return texte
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]
                else:
                    texte += event.unicode

    return texte
