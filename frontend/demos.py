import random
import copy
import pygame
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

# Stack Classes
class Node:
    def __init__(self, data):
        self.data = data
        self.nextnode = None

    def showInfo(self):
        print("Node Info --> " + str(self.data))


class DataStack:
    def __init__(self):
        self.top = None

    def push(self, newnode):
        if self.top is None:
            self.top = newnode
        else:
            newnode.nextnode = self.top
            self.top = newnode

    def peek(self):
        if self.top is None:
            return None
        else:
            return self.top

    def pop(self):
        if self.top is None:
            return None
        else:
            s = self.top
            self.top = self.top.nextnode
            return s

    def traverse(self):
        if self.top is None:
            print("The stack is empty")
        else:
            print("Traversing the contents of the stack...")
            ptr = self.top
            while ptr is not None:
                ptr.showInfo()
                ptr = ptr.nextnode

# fixed number of balls in a test tube
NUM_BALLS_PER_TUBE = 4

# Define the number of tubes and colors
NUM_TUBES = 6
NUM_COLORS = 4

# Colors for balls
BALL_COLORS = ["red", "blue", "green", "violet", "yellow"]

# Generate random tubes
def generate_tubes():
    colors = []
    for color in range(NUM_COLORS):
        colors.extend([color] * NUM_BALLS_PER_TUBE)

    random.shuffle(colors)
    tubes = []
    index = 0
    for _ in range(NUM_TUBES):
        if index < len(colors):
            tubes.append(colors[index:index + NUM_BALLS_PER_TUBE])
            index += NUM_BALLS_PER_TUBE
        else:
            tubes.append([])  # Empty tube
    return tubes

# Initialize tubes
tubes = generate_tubes()

# Check if the move is valid
def is_valid_move(tube_from, tube_to):
    if not tubes[tube_from]:  # tube_from is empty
        return False
    if not tubes[tube_to]:  # tube_to is empty
        return True
    if len(tubes[tube_to]) >= NUM_BALLS_PER_TUBE:  # tube_to cannot hold more than 4 balls
        return False
    return tubes[tube_from][0] == tubes[tube_to][0]  # Colors must match

# Make a move
def make_move(tube_from, tube_to):
    if is_valid_move(tube_from, tube_to):
        ball = tubes[tube_from].pop(0)  # Remove ball from tube_from
        tubes[tube_to].insert(0, ball)  # Add ball to tube_to
        return True
    return False

# Check if the game is won
def is_game_won():
    for tube in tubes:
        if tube and (len(tube) != NUM_BALLS_PER_TUBE or len(set(tube)) > 1):
            return False
    return True

# GUI implementation
class BallSortGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ball Sort Puzzle")
        self.geometry("800x600")
        self.resizable(False, False)
        self.config(background="skyblue")
        self.selected_tube = None
        self.undo_stack = DataStack()  # Use the DataStack for undo operations

        pygame.mixer.init()
        pygame.mixer.music.load("./perfect-beauty-191271.mp3")
        pygame.mixer.music.play(loops=1)

        self.tube_frames = []
        self.draw_tubes()

        # Add the Undo button
        self.undo_button = ctk.CTkButton(
            self,
            text="Undo",
            command=self.undo_move,  # Link to the undo function
            fg_color="red",
            text_color="white",
            corner_radius=10,
            state='disabled'  # Initially disabled as no move has been made
        )
        self.undo_button.grid(row=2, column=0, columnspan=6, pady=10)

        self.columnconfigure((0, 1, 2, 3, 4, 5,), weight=1)
        self.rowconfigure((0), weight=1)
        self.rowconfigure((1), weight=5)

        ctk.CTkLabel(self, text="Ball Sort", text_color="black", font=("Times", 50, "bold"), fg_color="#a2d2ff").grid(row=0, column=0, columnspan=10, sticky="nsew")

    def draw_tubes(self):
        for i, tube in enumerate(tubes):
            frame = ctk.CTkFrame(self, width=90, height=355, border_color="black", border_width=3, fg_color="skyblue", bg_color="skyblue", corner_radius=50)
            frame.grid(row=1, column=i, padx=10, pady=10)
            self.temp = ctk.CTkFrame(self, width=90, height=20, fg_color="skyblue", border_width=3, border_color="black")
            self.temp.grid(row=1, column=i, sticky="n", pady=60)
            self.temp.lift()
            frame.grid_propagate(False)
            self.tube_frames.append(frame)
            self.draw_balls_in_tube(i)
            frame.bind("<Button-1>", lambda e, idx=i: self.select_tube(idx))

    def draw_balls_in_tube(self, tube_idx):
        self.frame = self.tube_frames[tube_idx]
        # Clear the frame before redrawing the balls
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Using grid to position each button
        for idx, ball in enumerate(tubes[tube_idx]):
            color = BALL_COLORS[ball]
            # Create a button for each ball
            label = ctk.CTkButton(
                self.frame,
                text="",
                fg_color=color,
                corner_radius=100,
                hover_color=color,
                border_color="black",
                width=60,
                height=60,
                border_width=2
            )
            label.grid(row=idx, column=0, pady=14, padx=15)  # Place each button in a new row
            label.lift()

            # Bind the label click to select the tube itself
            label.bind("<Button-1>", lambda e, tube_idx=tube_idx: self.select_tube(tube_idx))

    def select_tube(self, tube_idx):
        if self.selected_tube is None:
            self.selected_tube = tube_idx
            self.highlight_tube(tube_idx)
        else:
            if self.selected_tube != tube_idx:
                if make_move(self.selected_tube, tube_idx):
                    self.save_undo_state()  # Save the move in the undo stack
                    self.draw_balls_in_tube(self.selected_tube)
                    self.draw_balls_in_tube(tube_idx)
                    self.undo_button.configure(state='normal')  # Enable undo after a move is made
                self.reset_highlight()
                self.selected_tube = None
                self.check_win_condition()

    def save_undo_state(self):
        state_copy = copy.deepcopy(tubes)  # Save the current state
        new_node = Node(state_copy)
        self.undo_stack.push(new_node)

    def undo_move(self):
        if self.undo_stack.peek() is not None:
            last_state_node = self.undo_stack.pop()  # Retrieve the previous state
            global tubes
            tubes = last_state_node.data
            self.update_display()  # Update the display with the previous state
        if self.undo_stack.peek() is None:
            self.undo_button.configure(state='disabled')  # Disable the undo button if no moves are left

    def update_display(self):
        for tube_idx in range(NUM_TUBES):
            self.draw_balls_in_tube(tube_idx)  # Redraw the tubes after an undo

    def highlight_tube(self, tube_idx):
        frame = self.tube_frames[tube_idx]
        frame.configure(border_color="white", bg_color="white")

    def reset_highlight(self):
        for i, frame in enumerate(self.tube_frames):
            for j, widget in enumerate(frame.winfo_children()):
                ball_color = BALL_COLORS[tubes[i][j]] if j < len(tubes[i]) else "grey"
                widget.configure(fg_color=ball_color)
                frame.configure(border_color="black", bg_color="skyblue")

    def check_win_condition(self):
        if is_game_won():
            win_label = ctk.CTkLabel(self, text="Congratulations! You won the game!", font=("Arial", 16), text_color="green")
            win_label.grid(row=1, columnspan=len(tubes), pady=10)

# Start the game
if __name__ == "__main__":
    app = BallSortGame()
    app.mainloop()
