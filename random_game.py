import cv2
import numpy as np
from Board import *
import time
import random





def random_game():
    global black, white

    current_player = 'black'
    no_moves_passes = 0  # Compteur de passes consécutives

    # Afficher le plateau initial
    update_board_from_bitboards(black, white)
    # time.sleep(0)

    while True:
        # Générer les mouvements possibles pour le joueur actuel
        own, enemy = (black, white) if current_player == 'black' else (white, black)
        moves, directions = generate_moves(own, enemy, board_size)

        if not moves:
            print(f"{current_player.capitalize()} ne peut pas jouer.")
            no_moves_passes += 1
            if no_moves_passes >= 2:
                # Si les deux joueurs ne peuvent pas jouer, la partie se termine
                break
            # Changer de joueur
            current_player = 'white' if current_player == 'black' else 'black'
            continue
        else:
            no_moves_passes = 0  # Réinitialisation du compteur de passes

        # Choisir un mouvement aléatoire
        move = random.choice(moves)

        # Appliquer le mouvement
        if current_player == 'black':
            black, white = make_move(black, white, move, directions)
        else:
            white, black = make_move(white, black, move, directions)

        # Afficher le plateau mis à jour
        update_board_from_bitboards(black, white)

        #print toutes les infos (jeu)

        print(f"{current_player.capitalize()} Pieces")
        print_pieces(black if current_player == 'black' else white, board_size)
        print(f"Board")
        print_board(white, black, board_size)
        print(f'{white:064b}')
        print(f'{black:064b}')



        # Changer de joueur
        current_player = 'white' if current_player == 'black' else 'black'

        time.sleep(0)

    # Fin du jeu : déterminer le gagnant
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


random_game()