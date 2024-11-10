from Board import *
from DFS import *
from BFS import *
from interface_v2 import *
import time, random
from alpha_beta import find_best_move

traversal_method = 'dfs'  # ou 'bfs'
stop_game = False

def game_with_ai():
    global black, white, stop_game

    current_player = 'black'
    no_moves_passes = 0
    depth_limit = 5  # Profondeur de recherche

    update_board_from_bitboards(black, white)
    time.sleep(3)

    while not stop_game:
        # Vérifier si Échap a été pressée
        key = cv2.waitKey(1)

        if key == 27:  # Code ASCII pour Échap
            print("Touche Échap détectée. Arrêt du jeu.")
            stop_game = True
            break

        own, enemy = (black, white) if current_player == 'black' else (white, black)
        moves, directions = generate_moves(own, enemy, board_size)

        if not moves:
            print(f"{current_player.capitalize()} ne peut pas jouer.")
            no_moves_passes += 1
            if no_moves_passes >= 2:
                break
            current_player = 'white' if current_player == 'black' else 'black'
            continue
        else:
            no_moves_passes = 0

        if current_player == 'black':
            # Choisir l'algorithme à utiliser

            if traversal_method == 'dfs':
                score, move = minimax_with_dfs(own, enemy, depth_limit, True)

            else:
                raise ValueError("Méthode de parcours invalide.")

            # Convertir le mouvement en coordonnées pour l'affichage
            move_coords = bitboard_to_coords(move)
            print(f"IA choisit le mouvement : {move_coords} avec score {score}")

        else:
            # L'adversaire ne joue plus aléatoirement
            score, move = minimax_with_dfs(own,enemy, depth_limit, True)
            move_coords = bitboard_to_coords(move)
            print(f"L'adversaire joue le mouvement : {move_coords}")

        # Appliquer le mouvement
        if current_player == 'black':
            black, white = make_move(black, white, move, directions)
        else:
            white, black = make_move(white, black, move, directions)

        update_board_from_bitboards(black, white)
        current_player = 'white' if current_player == 'black' else 'black'
        time.sleep(1)

    # Fin de la partie
    black_count = cell_count(black)
    white_count = cell_count(white)

    if black_count > white_count:
        print("Black wins!")
    elif white_count > black_count:
        print("White wins!")
    else:
        print("Draw!")

    print(f"Final count -> Black: {black_count}, White: {white_count}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


game_with_ai()
