# Generation ID: Hutch_1763731569781_nj4lcd81q (前半)

def myai(board, color):
    """
    オセロの最適な手を返す関数
    """
    BLACK = 1
    WHITE = 2
    opponent = WHITE if color == BLACK else BLACK

    size = len(board)
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    def is_valid(r, c):
        return 0 <= r < size and 0 <= c < size

    def count_flips(r, c, col, board_copy):
        if board_copy[r][c] != 0:
            return 0
        total = 0
        for dr, dc in directions:
            count = 0
            nr, nc = r + dr, c + dc
            while is_valid(nr, nc) and board_copy[nr][nc] == opponent:
                count += 1
                nr += dr
                nc += dc
            if is_valid(nr, nc) and board_copy[nr][nc] == col and count > 0:
                total += count
        return total

    def get_flipped_positions(r, c, col, board_copy):
        if board_copy[r][c] != 0:
            return []
        flipped = []
        for dr, dc in directions:
            temp = []
            nr, nc = r + dr, c + dc
            while is_valid(nr, nc) and board_copy[nr][nc] == opponent:
                temp.append((nr, nc))
                nr += dr
                nc += dc
            if is_valid(nr, nc) and board_copy[nr][nc] == col and temp:
                flipped.extend(temp)
        return flipped

    def apply_move(r, c, col, board_copy):
        new_board = [row[:] for row in board_copy]
        new_board[r][c] = col
        for nr, nc in get_flipped_positions(r, c, col, board_copy):
            new_board[nr][nc] = col
        return new_board

    def count_adjacent_empty(r, c, board_copy):
        count = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and board_copy[nr][nc] == 0:
                count += 1
        return count

    def get_opponent_moves(board_copy):
        moves = set()
        for r in range(size):
            for c in range(size):
                if count_flips(r, c, opponent, board_copy) > 0:
                    moves.add((r, c))
        return len(moves)

    def is_corner(r, c):
        return (r, c) in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]

    def is_corner_adjacent(r, c):
        corners = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]
        for cr, cc in corners:
            if abs(r - cr) <= 1 and abs(c - cc) <= 1 and (r, c) != (cr, cc):
                return True
        return False

    def count_stones(board_copy, col):
        return sum(row.count(col) for row in board_copy)

    def count_empty(board_copy):
        return sum(row.count(0) for row in board_copy)

    valid_moves = []
    for r in range(size):
        for c in range(size):
            flips = count_flips(r, c, color, board)
            if flips > 0:
                valid_moves.append((r, c, flips))

    if not valid_moves:
        return None

    total_stones = count_stones(board, color) + count_stones(board, opponent)
    empty_count = count_empty(board)
    progress = total_stones / (size * size)

    corner_moves = [(r, c, flips) for r, c, flips in valid_moves if is_corner(r, c)]
    if corner_moves:
        return (corner_moves[0][1], corner_moves[0][0])

    if progress < 0.3:
        safe_moves = [(r, c, flips) for r, c, flips in valid_moves if not is_corner_adjacent(r, c)]
        if safe_moves:
            safe_moves.sort(key=lambda x: (x[2], -count_adjacent_empty(x[0], x[1], board)))
            return (safe_moves[0][1], safe_moves[0][0])
        else:
            valid_moves.sort(key=lambda x: (x[2], -count_adjacent_empty(x[0], x[1], board)))
            return (valid_moves[0][1], valid_moves[0][0])

    elif progress < 0.65:
        best_move = None
        best_score = -float('inf')

        for r, c, flips in valid_moves:
            if is_corner_adjacent(r, c):
                continue

            new_board = apply_move(r, c, color, board)
            opponent_moves = get_opponent_moves(new_board)
            adjacent_empty = count_adjacent_empty(r, c, board)

            score = flips - (adjacent_empty * 0.3) - (opponent_moves * 0.5)

            if score > best_score:
                best_score = score
                best_move = (r, c)

        if best_move:
            return (best_move[1], best_move[0])

    else:
        if empty_count % 2 == 0:
            valid_moves.sort(key=lambda x: x[2], reverse=True)
            return (valid_moves[0][1], valid_moves[0][0])
        else:
            valid_moves.sort(key=lambda x: x[2], reverse=True)
            return (valid_moves[0][1], valid_moves[0][0])

    valid_moves.sort(key=lambda x: x[2], reverse=True)
    return (valid_moves[0][1], valid_moves[0][0])

# Generation ID: Hutch_1763731569781_nj4lcd81q (後半)
