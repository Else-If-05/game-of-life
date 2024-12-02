import json
import numpy as np

def save_game(filename, grille, regles):
    """Sauvegarde l'état actuel de la grille et des règles dans un fichier JSON."""
    data = {
        'grille': grille.tolist(),  # Convertir la grille numpy en liste pour JSON
        'regles': regles
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)  # Indentation pour lisibilité
    print(f"Partie sauvegardée dans {filename}.")

def load_game(filename):
    """Charge l'état de la grille et des règles depuis un fichier JSON."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        grille = np.array(data['grille'])  # Reconvertir la grille en tableau numpy
        regles = data['regles']
        print(f"Partie chargée depuis {filename}.")
        return grille, regles
    except FileNotFoundError:
        print(f"Erreur : le fichier {filename} est introuvable.")
        return None, None
    except json.JSONDecodeError:
        print(f"Erreur : le fichier {filename} n'est pas un fichier JSON valide.")
        return None, None
