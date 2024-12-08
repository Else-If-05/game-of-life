import fonctions_base
import save
import optimisation
import pygame
import jeu_final

# Programme principal
if __name__ == "__main__":
    screen = pygame.display.set_mode((1000, 800))  # Fenêtre plus large pour le panneau
    pygame.display.set_caption("Jeu de la Vie")

    while True:
        action = fonctions_base.afficher_accueil()
        if action == "new_game":
            TAILLE_GRILLE = fonctions_base.demander_taille(screen)

            REGLES = fonctions_base.demander_regles(screen)
            if TAILLE_GRILLE > 100:
                optimisation.boucle_jeu_optimisé(TAILLE_GRILLE, REGLES)
            else:
                jeu_final.boucle_jeu(TAILLE_GRILLE, REGLES)
        elif action == "load_game":
            nom_fichier = save.demander_nom_fichier(screen)
            if nom_fichier:
                result = save.load_game(nom_fichier + ".json")
                if result:
                    grille, regles = result
                    if TAILLE_GRILLE > 100:
                        optimisation.boucle_jeu_load(grille, regles)
                    else :
                        jeu_final.boucle_jeu_load(grille, regles)
            else:
                print("Nom de fichier non valide.")
        elif action == "quit":
            continue