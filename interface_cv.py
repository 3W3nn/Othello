import cv2
import numpy as np
from Board import *

# Paramètres du plateau
cell_size = 80
window_size = board_size * cell_size

# Charger une image JPG pour l'arrière-plan
background_image = cv2.imread('wood_texture.jpg')

# Redimensionner l'image de fond pour correspondre à la taille de la fenêtre
background_image = cv2.resize(background_image, (window_size, window_size))


# Créer une image représentant le plateau avec des cases semi-transparentes
def create_board_with_transparent_cells():
    board = background_image.copy()

    # Créer un calque semi-transparent (nuances de blanc)
    overlay = board.copy()
    for row in range(board_size):
        for col in range(board_size):
            transparency = 100  # Valeur de transparence (0-255)
            if (row + col) % 2 == 0:
                color = (255, 255, 255, transparency)  # Blanc
            else:
                color = (200, 200, 200, transparency)  # Gris clair

            # Appliquer la couleur semi-transparente
            cv2.rectangle(overlay,
                          (col * cell_size, row * cell_size),
                          ((col + 1) * cell_size, (row + 1) * cell_size),
                          color[:3], -1)

    cv2.addWeighted(overlay, 0.5, board, 0.5, 0, board)
    return board


# Dessiner un pion
def draw_piece(board, row, col, player):
    color = (0, 0, 0) if player == 'black' else (255, 255, 255)
    center = (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2)
    radius = cell_size // 2 - 5
    cv2.circle(board, center, radius, color, -1)


# Gestion des événements de la souris
def mouse_callback(event, x, y, flags, param):
    global current_player, black, white
    if event == cv2.EVENT_LBUTTONDOWN:
        col = x // cell_size
        row = y // cell_size
        move_to_play = 1 << (row * board_size + col)

        if not is_black(row, col) and not is_white(row, col):
            print(f"Placer un pion {current_player} en ({row}, {col})")
            # Générer les mouvements possibles pour le joueur actuel
            own, enemy = (black, white) if current_player == 'black' else (white, black)
            moves, directions = generate_moves(own, enemy, board_size)

            # Vérifier si le mouvement est valide
            if move_to_play in moves:
                # Effectuer le mouvement avec make_move
                if current_player == 'black':
                    black, white = make_move(black, white, move_to_play, directions)
                else:
                    white, black = make_move(white, black, move_to_play, directions)

                # Imprimer l'état du plateau
                print_information()

                # Changer de joueur
                current_player = 'white' if current_player == 'black' else 'black'
                update_board()
            else:
                print("Mouvement invalide.")
        else:
            print("Case déjà occupée.")


# Mettre à jour l'affichage du plateau
def update_board():
    updated_board = create_board_with_transparent_cells()
    for row in range(board_size):
        for col in range(board_size):
            if is_black(row, col):
                draw_piece(updated_board, row, col, 'black')
            elif is_white(row, col):
                draw_piece(updated_board, row, col, 'white')
    cv2.imshow("Othello", updated_board)


# Initialisation du jeu
reset_board()
current_player = 'black'

# Créer et afficher le plateau de départ
board = create_board_with_transparent_cells()
update_board()

# Définir la gestion des événements de la souris
cv2.setMouseCallback("Othello", mouse_callback)

# Boucle principale
while True:
    key = cv2.waitKey(1)
    if key == 27:  # Appuyer sur 'Esc' pour quitter
        break

cv2.destroyAllWindows()
