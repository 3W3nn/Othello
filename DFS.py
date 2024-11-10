from Board import *


def dfs_traversal(own, enemy, depth, max_depth, maximizing_player, path, results):
    """Parcours en profondeur du jeu jusqu'à une certaine profondeur."""
    path_coords = [bitboard_to_coords(move) for move in path]


    if depth == max_depth:
        print(f"DFS: profondeur {depth}, chemin {path_coords}, joueur {'max' if maximizing_player else 'min'}")
        # Évaluation de la position actuelle
        score = hybrid_evaluation2(own, enemy, board_size, table=TABLE1)
        results.append((path.copy(), score))
        print(f"Score évalué à la profondeur {depth} : {score}\n\n")
        print("-" * 40)
        return

    moves, directions = generate_moves(own, enemy, board_size)
    if not moves:
        # Si pas de mouvements, passer le tour
        dfs_traversal(enemy, own, depth + 1, max_depth, not maximizing_player, path, results)
        return

    for move in moves:
        # Simuler le mouvement
        new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
        # Ajouter le mouvement au chemin
        path.append(move)
        #affichage
        print(f"DFS: profondeur {depth}, chemin {path_coords}, joueur {'max' if maximizing_player else 'min'}")
        # Appel récursif en incrémentant la profondeur
        dfs_traversal(new_enemy, new_own, depth + 1, max_depth, not maximizing_player, path, results)
        # Retirer le mouvement du chemin (backtracking)
        path.pop()


def minimax_with_dfs(own, enemy, max_depth, maximizing_player):
    results = []
    path = []
    depth = 0  # Profondeur initiale
    dfs_traversal(own, enemy, depth, max_depth, maximizing_player, path, results)
    # Maintenant, nous avons tous les chemins et leurs scores
    # Nous devons sélectionner le meilleur chemin selon minimax

    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None

    for move_sequence, score in results:
        if not move_sequence:
            continue
        first_move = move_sequence[0]
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = first_move
        else:
            if score < best_score:
                best_score = score
                best_move = first_move
    print(f"score : {score} ")

    best_move_coords = bitboard_to_coords(best_move)
    print(f"Meilleur coup déterminé par minimax_with_dfs : {best_move_coords} avec score {best_score}")
    return best_score, best_move



def minimax_alpha_beta(own, enemy, depth, max_depth, alpha, beta, maximizing_player):
    if depth == max_depth:
        return hybrid_evaluation(own, enemy, board_size)

    moves, directions = generate_moves(own, enemy, board_size)
    if not moves:
        # Si le joueur courant n'a pas de mouvements, passer le tour sans changer la profondeur
        return minimax_alpha_beta(enemy, own, depth, max_depth, alpha, beta, not maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
            eval = minimax_alpha_beta(new_enemy, new_own, depth + 1, max_depth, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Coupure beta
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_enemy, new_own = make_move_simulation(enemy, own, move, directions)
            eval = minimax_alpha_beta(new_own, new_enemy, depth + 1, max_depth, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Coupure alpha
        return min_eval


def find_best_move(own, enemy, max_depth):
    best_move = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    moves, directions = generate_moves(own, enemy, board_size)

    for move in moves:
        new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
        score = minimax_alpha_beta(new_enemy, new_own, 1, max_depth, alpha, beta, False)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)

    return best_move, best_score