import numpy as np
import time
import matplotlib.pyplot as plt
import moteur
import analyse_de_donnees as graphe
import matplotlib
matplotlib.use("TkAgg")  # Utilise Tkinter pour afficher les graphiques

#DEBUT PARTIE DE PAUL

# Demander à l'utilisateur la taille de la grille
while True:
    taille = int(input("Veuillez entrer la taille de la grille (N pour une grille NxN) : "))
    if taille >= 10:
        print("Grille initialisée.")
        break

# Initialisation de la grille
grille = moteur.initialiser_grille(taille)

# Demander les règles
regles = moteur.demander_regles()

# Nombre d'itérations
iterations = 2
cellules_vivantes = []
fig1 = plt.figure(1)
fig2 = plt.figure(2)

# Affichage de l'évolution de la grille
for i in range(1, iterations+1):  #j'ai changé iteration+1 au lieu de iteration
    print(f"Étape {i}:")
    plt.figure(1)
    moteur.afficher_grille(grille)
    plt.figure(2)
    cellules_vivantes.append(graphe.compter_cellules(grille))
    plt.clf()
    plt.plot(np.arange(1, i+1, 1), cellules_vivantes)
    plt.draw()
    plt.pause(0.9)
    grille = moteur.appliquer_regles(grille, regles)
    time.sleep(0.5)  # Pause pour voir l'évolution

#FIN PARTIE DE PAUL

# Paramètres
taille_grille = 50  # Taille de la grille (50x50)
steps = 100  # Nombre d'étapes pour la simulation

# Grille initiale aléatoire
grille_initiale = np.random.randint(2, size=(taille_grille, taille_grille))

print("Simulation de l'évolution des cellules...")
graphe.evolution_cellules(grille_initiale, steps, regles)

print("\nCalcul du temps de calcul en fonction de la taille de la grille...")
graphe.temps_de_calcul_par_taille(100, steps, regles)

