import random


# Initialisation du jeu
def create_board():
    # Crée un tableau 4x4 avec des valeurs aléatoires entre 1 et 10
    return [[random.randint(1, 10) for _ in range(4)] for _ in range(4)]


def display_board(board, hidden=True):
    # Affiche le tableau (face cachée ou visible selon hidden)
    for row in board:
        for card in row:
            if hidden and card != 0:
                print("X ", end=" ")
            else:
                print(f"{card:2}", end=" ")
        print()
    print()


def are_adjacent(board, x1, y1, x2, y2):
    # Vérifie si deux positions sont adjacentes orthogonalement
    return abs(x1 - x2) + abs(y1 - y2) == 1


def cancel_groups(board):
    # Annule les groupes de cartes adjacentes de même valeur
    visited = set()
    for i in range(4):
        for j in range(4):
            if (i, j) not in visited and board[i][j] != 0:
                value = board[i][j]
                group = [(i, j)]
                visited.add((i, j))

                # Recherche des voisins de même valeur
                k = 0
                while k < len(group):
                    x, y = group[k]
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < 4 and 0 <= ny < 4 and
                                (nx, ny) not in visited and
                                board[nx][ny] == value):
                            group.append((nx, ny))
                            visited.add((nx, ny))
                    k += 1

                # Si groupe de 2 ou plus, annule les valeurs
                if len(group) >= 2:
                    for x, y in group:
                        board[x][y] = 0


def calculate_score(board):
    # Calcule le score (somme des cartes non annulées)
    cancel_groups(board)
    return sum(sum(row) for row in board)


def push_card(board, card, direction, index):
    # Pousse une carte dans une ligne ou colonne
    if direction == 'row':
        row = board[index]
        row.insert(0, card)
        row.pop()
    elif direction == 'col':
        col = [board[i][index] for i in range(4)]
        col.insert(0, card)
        col.pop()
        for i in range(4):
            board[i][index] = col[i]


def play_game():
    # Initialisation des joueurs
    players = [create_board(), create_board()]
    center_cards = []

    print("Début de la partie Dékal !\n")

    # 16 tours pour révéler toutes les cartes
    for turn in range(16):
        for player_idx, board in enumerate(players):
            print(f"Tableau du Joueur {player_idx + 1} :")
            display_board(board)

            # Choix de la carte à placer au centre
            while True:
                try:
                    x = int(input(f"Joueur {player_idx + 1}, choisissez la ligne (0-3) : "))
                    y = int(input(f"Joueur {player_idx + 1}, choisissez la colonne (0-3) : "))
                    if 0 <= x < 4 and 0 <= y < 4 and board[x][y] != 0:
                        card = board[x][y]
                        board[x][y] = None  # Marque comme utilisée
                        center_cards.append(card)
                        break
                    else:
                        print("Position invalide ou déjà utilisée !")
                except ValueError:
                    print("Entrez des nombres valides !")

        # Révélation et récupération des cartes
        print(f"Cartes au centre : {center_cards}")
        for player_idx, board in enumerate(players):
            if len(center_cards) > 0:
                card = center_cards.pop(0)
                print(f"Joueur {player_idx + 1} récupère la carte {card}")

                # Choix de la direction et de la position
                direction = input(f"Joueur {player_idx + 1}, 'row' ou 'col' ? ").lower()
                index = int(input(f"Joueur {player_idx + 1}, choisissez l'index (0-3) : "))
                push_card(board, card, direction, index)

    # Fin de la partie : calcul des scores
    print("\nFin de la partie ! Calcul des scores...")
    for player_idx, board in enumerate(players):
        print(f"Tableau final du Joueur {player_idx + 1} :")
        display_board(board, hidden=False)
        score = calculate_score(board)
        print(f"Score du Joueur {player_idx + 1} : {score}")

    # Détermine le gagnant
    scores = [calculate_score(board) for board in players]
    winner = scores.index(min(scores)) + 1
    print(f"\nLe Joueur {winner} gagne avec le score le plus bas !")


# Lancer le jeu
if __name__ == "__main__":
    play_game()