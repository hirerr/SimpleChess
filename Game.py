import tkinter as tk
from Board import Board
from GameStatus import GameStatus

class Game:
    def __init__(self):
        self.current_turn = "white"  # "white" or "black"
        self.status = GameStatus()  # Initialize the game status
        self.selected_piece = None  # Currently selected piece
        self.selected_position = None  # Position of the selected piece
        self.highlighted_squares = []  # List of highlighted squares

        # Create the main Tkinter window
        self.root = tk.Tk()
        self.root.title("Chess Game")

        # Initialize the Board
        self.board = Board(self.root)

    def highlight_moves(self, moves):
        """Highlights the valid moves for the selected piece."""
        for move in moves:
            self.board.highlight_square(move, color="yellow", stipple="gray50")

    def clear_highlights(self):
        """Clears all highlighted squares."""
        self.board.clear_highlighted_squares()

    def refresh_board(self):
        """Redraw the board and pieces after a move."""
        self.board.refresh_board()

    def on_square_click(self, event):
        """Handles clicks on the chessboard."""
        position = self.board.get_square_from_event(event)

        # If a piece is already selected, attempt to move it
        if self.selected_piece:
            if position in self.selected_piece.get_valid_moves(self.board):
                # Move the piece
                self.board.move_piece(self.selected_position, position)

                # Clear highlights and refresh the board
                self.clear_highlights()
                self.refresh_board()

                # Switch turn
                self.current_turn = "black" if self.current_turn == "white" else "white"
                self.board.toggle_turn()

            # Reset the selected piece
            self.selected_piece = None
            self.selected_position = None
        else:
            # Clear previous highlights
            self.clear_highlights()

            # Check if there is a piece at the clicked position
            piece = self.board.get_piece_at(position)
            if piece and piece.color == self.current_turn:
                # Highlight possible moves for the selected piece
                self.selected_piece = piece
                self.selected_position = position
                valid_moves = piece.get_valid_moves(self.board)
                self.highlight_moves(valid_moves)

    def main(self):
        """Start the game loop."""
        # Bind the click event to the board's canvas
        self.board.bind_click_event(self.on_square_click)

        # Start the Tkinter event loop
        self.root.mainloop()

# Run the program
if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.main()
