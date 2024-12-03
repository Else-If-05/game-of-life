import json
import numpy as np
import pygame

def save_game(filename, grille, regles):

    try:
        game_state = {
            "taille_grille": grille.shape[0],
            "regles": regles,
            "grille": grille.tolist()
        }

        with open(filename, 'w') as file:
            json.dump(game_state, file)

        print(f"Game saved to file {filename}")
    except Exception as e:
        print(f"Error while saving: {e}")

def load_game(filename):

    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
            print("Game state loaded:", game_state)  # Debugging line

        taille_grille = game_state["taille_grille"]
        regles = game_state["regles"]
        grille = np.array(game_state["grille"], dtype=int)

        print(f"Game loaded from file {filename}")
        return grille, regles
    except Exception as e:
        print(f"Error while loading: {e}")
        return None

def demander_nom_fichier(screen):

    input_box = pygame.Rect(300, 350, 400, 50)
    font = pygame.font.Font(None, 36)
    actif = True
    texte = ""
    running = True

    while running:
        screen.fill((240, 248, 255))  # Fond blanc cassé

        #affiche la boîte de texte
        pygame.draw.rect(screen, (200, 200, 200), input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        text_surface = font.render(texte, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        #affiche un texte explicatif
        message = font.render("Entrez le nom du fichier et appuyez sur Entrée", True, (0, 0, 0))
        screen.blit(message, (200, 250))

        pygame.display.flip()

        #clavier
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
