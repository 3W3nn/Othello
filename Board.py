
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
    white = 0
    black = 0

    white = set_state(white, 3, 3, board_size)
    white = set_state(white, 4, 4, board_size)
    black = set_state(black, 3, 4, board_size)
    black = set_state(black, 4, 3, board_size)

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

reset_board()
print("White Pieces")
print(f"{white:064b}")
print_pieces(white, board_size)
print("Black Pieces")
print(f"{black:064b}")
print_pieces(black, board_size)
print("Board")
print_board(white, black, board_size)