from Board import *
import cv2

# Paramètres du plateau
cell_size = 80
window_size = board_size * cell_size

# Charger une image JPG pour l'arrière-plan
background_image = cv2.imread('wood_texture.jpg')

# Redimensionner l'image de fond pour correspondre à la taille de la fenêtre
background_image = cv2.resize(background_image, (window_size, window_size))


# Créer une image représentant le plateau avec des cases semi-transparentes
def create_board():
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


# Mettre à jour l'affichage du plateau en fonction des bitboards
def update_board_from_bitboards(black_bitboard, white_bitboard):
    """Mettre à jour le plateau en fonction des bitboards des joueurs noirs et blancs."""
    updated_board = create_board()

    # Pour chaque cellule, vérifier si elle est occupée par un pion noir ou blanc en utilisant les bitboards
    for row in range(board_size):
        for col in range(board_size):
            pos = 1 << (row * board_size + col)  # Convertir la position en bit dans le bitboard
            if black_bitboard & pos:
                draw_piece(updated_board, row, col, 'black')
            elif white_bitboard & pos:
                draw_piece(updated_board, row, col, 'white')

    # Afficher le plateau mis à jour
    cv2.imshow("Othello", updated_board)
    cv2.waitKey(1)  # Nécessaire pour mettre à jour l'affichage

