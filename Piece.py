class Piece:
    def __init__(self, piece_type, color, position):
        self.piece_type = piece_type  # "pawn", "rook", "knight", etc.
        self.color = color  # "white" or "black"
        self.position = position

    def get_valid_moves(self, board):
        """Returns a list of valid moves for the piece."""
        if self.piece_type == "pawn":
            return self.get_pawn_moves(board)
        elif self.piece_type == "rook":
            return self.get_rook_moves(board)
        elif self.piece_type == "knight":
            return self.get_knight_moves(board)
        elif self.piece_type == "bishop":
            return self.get_bishop_moves(board)
        elif self.piece_type == "queen":
            return self.get_queen_moves(board)
        elif self.piece_type == "king":
            return self.get_king_moves(board)
        return []

    def get_pawn_moves(self, board):
        """Calculates valid moves for a pawn."""
        row, col = self.position
        direction = -1 if self.color == "white" else 1
        moves = []

        # Check forward move
        if board.get_piece_at((row + direction, col)) is None:
            moves.append((row + direction, col))

        # Check double forward move (only from starting position)
        starting_row = 6 if self.color == "white" else 1
        if row == starting_row and board.get_piece_at((row + 2 * direction, col)) is None:
            moves.append((row + 2 * direction, col))

        # Check diagonal captures
        for offset in [-1, 1]:
            new_pos = (row + direction, col + offset)
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:  # Ensure within bounds
                target = board.get_piece_at(new_pos)
                if target and target.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_rook_moves(self, board):
        """Calculates valid moves for a rook."""
        return self.get_straight_line_moves(board, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)])

    def get_bishop_moves(self, board):
        """Calculates valid moves for a bishop."""
        return self.get_straight_line_moves(board, directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)])

    def get_queen_moves(self, board):
        """Calculates valid moves for a queen."""
        return self.get_straight_line_moves(
            board,
            directions=[(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
        )

    def get_king_moves(self, board):
        """Calculates valid moves for a king."""
        row, col = self.position
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                target = board.get_piece_at(new_pos)
                if not target or target.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_knight_moves(self, board):
        """Calculates valid moves for a knight."""
        row, col = self.position
        moves = []
        knight_jumps = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2),
        ]

        for dr, dc in knight_jumps:
            new_pos = (row + dr, col + dc)
            if 0 <= new_pos[0] < 8 and 0 <= new_pos[1] < 8:
                target = board.get_piece_at(new_pos)
                if not target or target.color != self.color:
                    moves.append(new_pos)
        return moves

    def get_straight_line_moves(self, board, directions):
        """Helper method to calculate straight-line moves for rooks, bishops, and queens."""
        row, col = self.position
        moves = []

        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:  # Ensure within bounds
                    target = board.get_piece_at((r, c))
                    if target:
                        if target.color != self.color:
                            moves.append((r, c))  # Capture move
                        break  # Stop further moves in this direction
                    moves.append((r, c))  # Valid empty square
                else:
                    break
        return moves

    def __str__(self):
        # White and Black representations of pieces
        notation = self.piece_type[0]
        if self.piece_type == "knight":
            notation = self.piece_type[1]
        if self.color == "white":
            return notation.upper()
        return notation
