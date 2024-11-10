from Board import *
# Table de transposition pour l'algorithme Minimax
transposition_table = {}

# Fonction Minimax avec élagage alpha-bêta
def minimax_alpha_beta(own, enemy, depth, max_depth, alpha, beta, maximizing_player):
    """Algorithme Minimax avec élagage alpha-bêta et table de transposition."""
    position_key = (own, enemy)

    # Vérifier si la position est déjà dans la table de transposition
    if position_key in transposition_table:
        entry = transposition_table[position_key]
        # Si la profondeur stockée est supérieure ou égale, retourner le score stocké
        if entry['depth'] >= max_depth - depth:
            return entry['score']

    if depth == max_depth:
        score = hybrid_evaluation(own, enemy, board_size)
        transposition_table[position_key] = {'score': score, 'depth': max_depth - depth}
        return score

    moves, directions = generate_moves(own, enemy, board_size)
    if not moves:
        # Si le joueur courant n'a pas de mouvements, passer le tour sans changer la profondeur
        enemy_moves, _ = generate_moves(enemy, own, board_size)
        if not enemy_moves:
            # Si aucun des deux joueurs ne peut jouer, la partie est terminée
            score = hybrid_evaluation(own, enemy, board_size)
            transposition_table[position_key] = {'score': score, 'depth': max_depth - depth}
            return score
        else:
            # Passer le tour au joueur adverse
            score = minimax_alpha_beta(enemy, own, depth, max_depth, alpha, beta, not maximizing_player)
            transposition_table[position_key] = {'score': score, 'depth': max_depth - depth}
            return score

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
            eval = minimax_alpha_beta(new_own, new_enemy, depth + 1, max_depth, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Coupure beta
        transposition_table[position_key] = {'score': max_eval, 'depth': max_depth - depth}
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
        transposition_table[position_key] = {'score': min_eval, 'depth': max_depth - depth}
        return min_eval

# Fonction pour trouver le meilleur mouvement
def find_best_move(own, enemy, max_depth):
    """Trouve le meilleur coup en utilisant l'algorithme Minimax avec élagage alpha-bêta."""
    best_move = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    moves, directions = generate_moves(own, enemy, board_size)

    if not moves:
        return None, best_score

    # Trier les mouvements pour améliorer l'efficacité de l'élagage
    moves = sort_moves(moves, own, enemy)

    for move in moves:
        new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
        score = minimax_alpha_beta(new_own, new_enemy, 1, max_depth, alpha, beta, False)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)

    return best_move, best_score

# Fonction pour trier les mouvements (vous pouvez adapter la fonction selon vos besoins)
def sort_moves(moves, own, enemy):
    """Trie les mouvements en fonction du nombre de pions capturés pour optimiser l'élagage alpha-bêta."""
    move_scores = []
    for move in moves:
        # Vous pouvez utiliser une heuristique pour évaluer les mouvements
        # Par exemple, compter le nombre de pions retournés
        directions = {}
        temp_own, temp_enemy = make_move_simulation(own, enemy, move, directions)
        score = cell_count(temp_own) - cell_count(own)
        move_scores.append((score, move))
    # Trier les mouvements par score décroissant
    move_scores.sort(reverse=True)
    # Extraire les mouvements triés
    sorted_moves = [move for score, move in move_scores]
    return sorted_moves