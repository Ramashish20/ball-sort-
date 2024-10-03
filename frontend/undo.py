import tkinter as tk
import random

# ... (Your existing code for tubes, colors, and game logic)

class BallSortGame(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Ball Sort Puzzle")
        self.geometry("400x400")
       
        # Create tube frames
        self.tube_frames = []
        self.draw_tubes()
       
        # Initialize selected tube
        self.selected_tube = None

        # Initialize undo stack
        self.undo_stack = []

        # Create Undo button
        undo_button = tk.Button(self, text="Undo", command=self.undo_move)
        undo_button.grid(row=1, columnspan=NUM_TUBES, pady=10)

    def draw_tubes(self):
        return
        # ... (Your existing draw_tubes method)

    def select_tube(self, tube_idx):
        return
        # ... (Your existing select_tube method)

    def undo_move(self):
        if self.undo_stack:
            prev_state = self.undo_stack.pop()
            # Restore the previous state (e.g., update tubes)
            # You'll need to implement this part based on your existing game logic
            # For now, let's just print the previous state:
            print("Undoing move. Previous state:", prev_state)

    # ... (Your existing highlight_tube, reset_highlight, and check_win_condition methods)

# Start the game
if __name__ == "_main_":
    app = BallSortGame()
    app.mainloop()