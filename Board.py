from Piece import Piece
import tkinter as tk

class Board:
    def __init__(self, root):
        # Instance variables for board configuration
        self.square_size = 60  # pixels
        self.board_size = self.square_size * 8

        # Colors for the squares
        self.light_color = "#F0D9B5"
        self.dark_color = "#B58863"

        # Chess pieces (as Piece objects)
        self.pieces = {}
        self.setup_pieces()

        # Player Turn
        self.current_turn = "white"
        
        self.highlighted_squares = []  # To store highlighted square IDs

        # Create the GUI elements
        self.root = root
        self.create_gui()

    def setup_pieces(self):
        """Set up the initial positions with Piece objects."""
        # Add pawns
        for col in range(8):
            self.pieces[(1, col)] = Piece("pawn", "black", (1, col))
            self.pieces[(6, col)] = Piece("pawn", "white", (6, col))

        # Add other pieces
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col, piece_type in enumerate(piece_order):
            self.pieces[(0, col)] = Piece(piece_type, "black", (0, col))
            self.pieces[(7, col)] = Piece(piece_type, "white", (7, col))

    def draw_board(self, canvas):
        """Draw the chessboard with alternating light and dark squares."""
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                # Alternate square colors
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def place_pieces(self, canvas):
        """Place the chess pieces on their starting positions."""
        for position, piece in self.pieces.items():
            row, col = position
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2

            # Draw text representing the piece
            canvas.create_text(x, y, text=str(piece), font=("Arial", 24), fill="black")

    def get_piece_at(self, position):
        """Return the piece at the given position or None."""
        return self.pieces.get(position)

    def move_piece(self, start_pos, end_pos):
        """Move a piece from start_pos to end_pos."""
        piece = self.get_piece_at(start_pos)
        if not piece:
            return False  # No piece at start_pos

        # Update piece position
        piece.position = end_pos
        self.pieces[end_pos] = piece
        del self.pieces[start_pos]
        return True

    def toggle_turn(self):
        """Toggles the current turn and updates the turn label."""
        self.current_turn = "black" if self.current_turn == "white" else "white"
        self.turn_label.config(text=f"Current Turn: {self.current_turn.capitalize()}")

    def create_gui(self):
        """Create and arrange the GUI elements."""
        # Create a main horizontal frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a vertical frame for the label
        label_frame = tk.Frame(main_frame)
        label_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

        # Turn indicator label
        self.turn_label = tk.Label(label_frame, text=f"Current Turn: {self.current_turn.capitalize()}", font=("Arial", 16))
        self.turn_label.pack(pady=10)  # Add padding around the label

        # Create a frame for the chessboard
        board_frame = tk.Frame(main_frame)
        board_frame.pack(side=tk.RIGHT)

        # Create canvas for the chessboard
        self.canvas = tk.Canvas(board_frame, width=self.board_size, height=self.board_size)
        self.canvas.pack()

        # Draw the chessboard and pieces
        self.draw_board(self.canvas)
        self.place_pieces(self.canvas)
    
    def highlight_square(self, position, color="yellow", stipple="gray50"):
        """Highlights a specific square."""
        row, col = position
        x1 = col * self.square_size
        y1 = row * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple=stipple)
        self.highlighted_squares.append(rect_id)

    def clear_highlighted_squares(self):
        """Clears all highlighted squares."""
        for rect_id in self.highlighted_squares:
            self.canvas.delete(rect_id)
        self.highlighted_squares = []

    def refresh_board(self):
        """Redraws the board and pieces."""
        self.draw_board(self.canvas)
        self.place_pieces(self.canvas)

    def get_square_from_event(self, event):
        """Converts a click event to a board position."""
        row = event.y // self.square_size
        col = event.x // self.square_size
        return (row, col)

    def bind_click_event(self, callback):
        """Binds a click event to the canvas."""
        self.canvas.bind("<Button-1>", callback)