from collections import deque
from Board import *

def bfs_traversal(own_start, enemy_start, depth_limit, maximizing_player):
    """Parcours en largeur du jeu jusqu'à une certaine profondeur."""
    queue = deque()
    results = []
    # Chaque élément de la file : (own, enemy, depth, maximizing_player, path)
    queue.append((own_start, enemy_start, 0, maximizing_player, []))

    while queue:
        own, enemy, depth, max_player, path = queue.popleft()
        if depth == depth_limit:
            # Évaluation de la position actuelle
            score = positional(own, enemy, board_size)
            results.append((path, score))
            continue

        moves, directions = generate_moves(own, enemy, board_size)
        if not moves:
            # Si pas de mouvements, passer le tour
            queue.append((enemy, own, depth + 1, not max_player, path.copy()))
            continue

        for move in moves:
            # Simuler le mouvement
            new_own, new_enemy = make_move_simulation(own, enemy, move, directions)
            # Ajouter le mouvement au chemin
            new_path = path + [move]
            # Ajouter à la file
            queue.append((new_own, new_enemy, depth + 1, not max_player, new_path))

    return results


def minimax_with_bfs(own, enemy, depth_limit, maximizing_player):
    results = bfs_traversal(own, enemy, depth_limit, maximizing_player)
    # Tri des résultats par longueur de chemin décroissante pour commencer par les feuilles
    results.sort(key=lambda x: len(x[0]), reverse=True)
    scores = {}

    for path, score in results:
        if not path:
            continue
        first_move = path[0]
        if tuple(path) not in scores:
            scores[tuple(path)] = score
        else:
            # Mise à jour du score en fonction du joueur
            if maximizing_player:
                scores[tuple(path)] = max(scores[tuple(path)], score)
            else:
                scores[tuple(path)] = min(scores[tuple(path)], score)

    # Sélection du meilleur coup
    best_score = float('-inf') if maximizing_player else float('inf')
    best_move = None

    for path_tuple, score in scores.items():
        move = path_tuple[0]
        if maximizing_player:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    print(f"Meilleur coup déterminé par minimax_with_bfs : {best_move} avec score {best_score}")
    return best_score, best_move