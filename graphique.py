import pygame
import sys
import numpy as np
import save
import matplotlib
matplotlib.use("TkAgg")  # Utiliser un backend compatible
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time
import optimisation
import fonctions_base

# Fonction pour compter les cellules vivantes dans la grille
def compter_cellules_vivantes(grille):
    return np.sum(grille)

# Fonction pour gérer le graphe évolutif dans un thread séparé
def afficher_graphe_evolutif(data):
    fig, ax = plt.subplots()
    ax.set_title("Évolution du nombre de cellules vivantes")
    ax.set_xlabel("Temps (itérations)")
    ax.set_ylabel("Cellules vivantes")
    line, = ax.plot([], [], label="Cellules vivantes")
    ax.legend()
    x_data, y_data = [], []

    def update(frame):
        if len(data) > 0:
            x_data.append(len(x_data))  # Ajoute le numéro de l'itération
            y_data.append(data[-1])    # Ajoute le dernier nombre de cellules vivantes
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view()

    ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
    plt.show()


# Fonction pour détecter une structure dans une sous-grille
def detect_structure(subgrid, structure):
    return np.array_equal(subgrid, structure)

# Fonction pour analyser la grille et compter les "Still lifes"
def analyser_still_lifes(grille):
    counts = {key: 0 for key in fonctions_base.STILL_LIFES}
    taille_grille = grille.shape

    for name, pattern in fonctions_base.STILL_LIFES.items():
        pattern_size = pattern.shape
        for x in range(taille_grille[0] - pattern_size[0] + 1):
            for y in range(taille_grille[1] - pattern_size[1] + 1):
                subgrid = grille[x:x + pattern_size[0], y:y + pattern_size[1]]
                if detect_structure(subgrid, pattern):
                    counts[name] += 1

    return counts

# Fonction pour afficher un histogramme
def afficher_histogramme_still_lifes(counts):
    names = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 6))
    plt.bar(names, values, color="skyblue")
    plt.xlabel("Structures")
    plt.ylabel("Occurrences")
    plt.title("Occurrences des Still Lifes dans la grille")
    plt.show()

def afficher_graphe_temps_calcul(tailles, temps):
    """
    Affiche un graphe des temps de calcul en fonction de la taille de la grille.
    """
    fig, ax = plt.subplots()
    ax.plot(tailles, temps, marker='o', label="Temps de calcul")
    ax.set_title("Temps de calcul en fonction de la taille de la grille")
    ax.set_xlabel("Taille de la grille")
    ax.set_ylabel("Temps de calcul (secondes)")
    ax.legend()
    plt.show()


# Fonction principale du jeu
# Fonction pour gérer les graphiques évolutifs
def afficher_graphes_evolutifs(cellules_vivantes, still_lifes_data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Graphique de l'évolution des cellules vivantes
    ax1.set_title("Évolution du nombre de cellules vivantes")
    ax1.set_xlabel("Temps (itérations)")
    ax1.set_ylabel("Cellules vivantes")
    line, = ax1.plot([], [], label="Cellules vivantes", color="blue")
    ax1.legend()
    x_data, y_data = [], []

    # Histogramme des still lifes
    ax2.set_title("Histogramme des Still Lifes")
    ax2.set_xlabel("Type de structure")
    ax2.set_ylabel("Nombre détecté")
    bars = ax2.bar(fonctions_base.STILL_LIFES.keys(), [0] * len(fonctions_base.STILL_LIFES), color="skyblue")
    plt.tight_layout()

    def update(frame):
        # Mettre à jour le graphe des cellules vivantes
        if len(cellules_vivantes) > 0:
            x_data.append(len(x_data))
            y_data.append(cellules_vivantes[-1])
            line.set_data(x_data, y_data)
            ax1.relim()
            ax1.autoscale_view()

        # Mettre à jour l'histogramme des still lifes
        if len(still_lifes_data) > 0:
            last_counts = still_lifes_data[-1]
            for bar, count in zip(bars, last_counts.values()):
                bar.set_height(count)

        ax2.set_ylim(0, max([bar.get_height() for bar in bars]) + 1)  # Ajuster la hauteur max

    ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
    plt.show()

