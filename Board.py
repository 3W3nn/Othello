
board_size = 8

white = 0
black = 0
board = white | black

print(f'{white:064b}')
print(f'{black:064b}')
print(f'{board:064b}')


def get_state(bitboard: int, x: int, y: int, size: int = board_size):
    """Retourne l'état d'une cellule en décalant le bitboard vers la droite
    par x * taille + y et en prenant le LSB"""
    return (bitboard >> (x * size + y)) & 1

def is_black(x, y):
    """Vérifie si la cellule est occupée par un pion noir"""
    return get_state(black, x, y) == 1

def is_white(x, y):
    """Vérifie si la cellule est occupée par un pion blanc"""
    return get_state(white, x, y) == 1


def set_state(bitboard: int, x: int, y: int, size: int):
    """Add a bit to the board by shifting a 1 to the left
    by x * size + y and performing a bitwise OR with the board"""
    return bitboard | (1 << (x * size + y))

def reset_board():
    """Réinitialiser le plateau à son état initial"""
    global white, black
    white = 0x00_00_00_00_00_00_00_00
    black = 0x00_00_00_00_00_00_00_00

    white = set_state(white, 3, 3, board_size)
    white = set_state(white, 4, 4, board_size)
    black = set_state(black, 3, 4, board_size)
    black = set_state(black, 4, 3, board_size)
    white = set_state(white, 1, 1, board_size)
    black = set_state(black, 2, 2, board_size)


def print_pieces(bitboard: int, size: int):
    """Print the bit values of the board as a matrix of 0 and 1"""
    for i in range(size):
        for j in range(size):
            print(get_state(bitboard, i, j, size), end=' ')
        print()
    print()

def print_board(white_pieces: int, black_pieces: int, size: int):
    """Print the board with W for white_pieces, B for black_pieces and . for empty cells"""
    for i in range(size):
        for j in range(size):
            if get_state(white_pieces, i, j, size):
                print('W', end=' ')
            elif get_state(black_pieces, i, j, size):
                print('B', end=' ')
            else:
                print('.', end=' ')
        print()
    print()


def print_information():
    """Affiche le bitboard sous forme binaire pour visualiser l'état du plateau"""
    print(f'{white:064b}')
    print(f'{black:064b}')
    print("Board")
    print_board(white, black, board_size)
    print("----------------------------")

def cell_count(bitboard: int):
    """Count the number of cells in the board"""
    return bitboard.bit_count() # most efficient way to count for python>=3.10



def N(x):
    return x >> 8
def S(x):
    return (x & 0x00ffffffffffffff) << 8
def E(x):
    return (x & 0x7f7f7f7f7f7f7f7f) << 1
def W(x):
    return (x & 0xfefefefefefefefe) >> 1

def NW(x):
    return N(W(x))
def NE(x):
    return N(E(x))
def SW(x):
    return S(W(x))
def SE(x):
    return S(E(x))


# Generate possible moves
def generate_moves(own, enemy, size) -> tuple[list, dict]:
    """Generate the possible moves for the current player using bitwise operations"""
    empty = ~(own | enemy)  # Empty squares (not owned by either player)
    unique_moves = []  # List of possible moves
    dir_jump = {}  # Dictionary of moves and the number of pieces that can be captured in each direction

    # Generate moves in all eight directions
    for direction in [N, S, E, W, NW, NE, SW, SE]:
        # We get the pieces that are next to an enemy piece in the direction
        count = 0
        victims = direction(own) & enemy
        if not victims:
            continue

        # We keep getting the pieces that are next to an enemy piece in the direction
        for _ in range(size):
            count += 1
            next_piece = direction(victims) & enemy
            if not next_piece:
                break
            victims |= next_piece

        # We get the pieces that can be captured in the direction
        captures = direction(victims) & empty
        # if there are multiple pieces in captures, we separate them and add them to the set
        while captures:
            capture = captures & -captures  # get the least significant bit
            captures ^= capture  # remove the lsb
            if capture not in dir_jump:
                unique_moves.append(capture)
                dir_jump[capture] = []
            dir_jump[capture].append((direction, count))

    return unique_moves, dir_jump



def make_move(own, enemy, move_to_play, directions):
    """Make the move and update the board using bitwise operations."""
    for direction, count in directions[move_to_play]:
        victims = move_to_play  # Init the victims with the move to play

        op_dir = opposite_dir(direction)  # opposite direction since we go from the move to play to the captured pieces
        for _ in range(count):
            victims |= (op_dir(victims) & enemy)
        own ^= victims
        enemy ^= victims & ~move_to_play
    # because of the XOR, the move to play which is considered a victim can be returned a pair number of times
    own |= move_to_play

    return own, enemy


opposite_direction = {N: S, S: N, E: W, W: E, NW: SE,
                      NE: SW,
                      SW: NE, SE: NW}


def opposite_dir(direction):
    return opposite_direction[direction]

# print(f"The top left corner of the board is owned by black : "
#       f"{get_state(board, 0, 0, board_size) == get_state(black, 0, 0, board_size)}")       # True
# print(f"The bottom right corner of the board is owned by white : "
#       f"{get_state(board, 7, 7, board_size) == get_state(white, 7, 7, board_size)}")   # True

import numpy as np

TABLE1 = np.array([
    700, -150, 30, 10, 10, 30, -150, 700,
    -150, -250, 0, 0, 0, 0, -250, -150,
    30, 0, 1, 2, 2, 1, 0, 30,
    10, 0, 2, 16, 16, 2, 0, 10,
    10, 0, 2, 16, 16, 2, 0, 10,
    30, 0, 1, 2, 2, 1, 0, 30,
    -150, -250, 0, 0, 0, 0, -250, -150,
    700, -150, 30, 10, 10, 30, -150, 700
])


def positional(own, enemy, size, table=TABLE1):
    """Calcule la différence pondérée des positions entre les deux joueurs."""
    # Aplatir la table en 1D pour correspondre à l'indexation des bits
    table_flat = table.flatten()

    # Convertir les bitboards en masques booléens
    own_mask = np.array([bool(own & (1 << i)) for i in range(size * size)])
    enemy_mask = np.array([bool(enemy & (1 << i)) for i in range(size * size)])

    # Appliquer les masques à la table aplatie pour obtenir les valeurs
    own_values = table_flat[own_mask]
    enemy_values = table_flat[enemy_mask]

    # Calculer les sommes
    sum1 = np.sum(own_values)
    sum2 = np.sum(enemy_values)

    return sum1 - sum2

def display_positional_details(own, enemy, size, table=TABLE1):
    """Affiche les détails du calcul positionnel."""
    table_flat = table.flatten()
    own_mask = np.array([bool(own & (1 << i)) for i in range(size * size)])
    enemy_mask = np.array([bool(enemy & (1 << i)) for i in range(size * size)])

    own_values = table_flat[own_mask]
    enemy_values = table_flat[enemy_mask]

    sum1 = np.sum(own_values)
    sum2 = np.sum(enemy_values)

    own_positions = [bitboard_to_coords(1 << i) for i, val in enumerate(own_mask) if val]
    enemy_positions = [bitboard_to_coords(1 << i) for i, val in enumerate(enemy_mask) if val]

    print("Calcul du score de la position :")
    print("          ", "-" * 20, "          ")
    print(f"Pions du joueur courant (own) :")
    print(f"Positions : {own_positions}")
    print(f"Valeurs   : {own_values}")
    print(f"Somme own : {sum1}")
    print()
    print(f"Pions de l'adversaire (enemy) :")
    print(f"Positions : {enemy_positions}")
    print(f"Valeurs   : {enemy_values}")
    print(f"Somme enemy : {sum2}")
    print()
    print(f"Score final (own - enemy) : {sum1} - {sum2} = {sum1 - sum2}")
    return sum1 - sum2

def absolute(own: int, enemy: int):
    """Compute the difference between the number of pieces of the current player and the other player"""
    return cell_count(own) - cell_count(enemy)

def mobility(own: int, enemy: int, size: int):
    """Compute the difference between the number of possible moves for the current player and the other player"""
    own_moves, _ = generate_moves(own, enemy, size)
    enemy_moves, _ = generate_moves(enemy, own, size)
    return len(own_moves) - len(enemy_moves)


def make_move_simulation(own, enemy, move_to_play, directions):
    """Simule un coup sans modifier les bitboards originaux."""
    own_copy = own
    enemy_copy = enemy
    for direction, count in directions[move_to_play]:
        victims = move_to_play
        op_dir = opposite_dir(direction)
        for _ in range(count):
            victims |= (op_dir(victims) & enemy_copy)
        own_copy ^= victims
        enemy_copy ^= victims & ~move_to_play
    own_copy |= move_to_play
    return own_copy, enemy_copy

def bitboard_to_coords(bitboard):
    """Convertit un bitboard avec un seul bit à 1 en coordonnées (ligne, colonne)."""
    if bitboard == 0:
        return None
    bit_index = bitboard.bit_length() -1
    row = bit_index // board_size +1
    col = bit_index % board_size +1
    return row, col

def get_game_phase(own, enemy, total_cells):
    """Détermine la phase du jeu en fonction du nombre de pions sur le plateau."""
    total_pieces = cell_count(own) + cell_count(enemy)
    if total_pieces <= 20:
        return 'early'  # Début de partie
    elif total_pieces <= 44:
        return 'mid'    # Milieu de partie
    else:
        return 'late'   # Fin de partie


def hybrid_evaluation(own, enemy, size, table=TABLE1):
    """Évalue la position en combinant différentes stratégies en fonction de la phase du jeu."""
    phase = get_game_phase(own, enemy, size * size)

    if phase == 'early':
        # Stratégie positionnelle
        score = display_positional_details(own, enemy, size, table)
    elif phase == 'mid':
        # Stratégie de mobilité
        score = mobility(own, enemy, size)
    elif phase == 'late':
        # Stratégie absolue
        score = absolute(own, enemy)
    else:
        # Par défaut, utilisez la stratégie positionnelle
        score = positional(own, enemy, size, table)

    return score

def hybrid_evaluation2(own, enemy, size, table=TABLE1):
    """Évalue la position en combinant les stratégies avec des pondérations en fonction de la phase du jeu."""
    phase = get_game_phase(own, enemy, size * size)

    positional_score = positional(own, enemy, size, table)
    mobility_score = mobility(own, enemy, size)
    absolute_score = absolute(own, enemy)

    if phase == 'early':
        # Pondérations pour le début de partie
        score = (1.0 * positional_score) + (0.2 * mobility_score) + (0.0 * absolute_score)
    elif phase == 'mid':
        # Pondérations pour le milieu de partie
        score = (0.5 * positional_score) + (1.0 * mobility_score) + (0.0 * absolute_score)
    elif phase == 'late':
        # Pondérations pour la fin de partie
        score = (0.2 * positional_score) + (0.2 * mobility_score) + (1.0 * absolute_score)
    else:
        score = positional_score  # Par défaut

    return score


reset_board()
print("White Pieces")
print(f"{white:064b}")
print_pieces(white, board_size)
print("Black Pieces")
print(f"{black:064b}")
print_pieces(black, board_size)
print("Board")
print_board(white, black, board_size)

# white_moves, directions_white = generate_moves(white, black, board_size)
# all_w_moves = 0
# for move in white_moves:
#     all_w_moves |= move
# print_pieces(all_w_moves, board_size)
#
# black_moves, directions_black = generate_moves(black, white, board_size)
# all_b_moves = 0
# for move in black_moves:
#     all_b_moves |= move
# print_pieces(all_b_moves, board_size)