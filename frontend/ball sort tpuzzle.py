import tkinter as tk
from tkinter import messagebox
import random
import copy

# Parameters for the game
NUM_TUBES = 6
BALLS_PER_TUBE = 4
COLORS = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
UNDO_STACK = []
BALL_RADIUS = 30  # Radius of each ball for circular shape

# Create the main window
root = tk.Tk()
root.title("Advanced Ball Sort Puzzle")

# Store tubes and their contents (balls)
tubes = [[] for _ in range(NUM_TUBES)]
selected_tube = None
move_count = 0

# Canvas where we will draw the balls and test tubes
canvas = tk.Canvas(root, width=800, height=500)
canvas.pack()

# Function to initialize the tubes with random balls
def initialize_tubes():
    global move_count
    balls = []

    # Add colored balls to the list
    for color in COLORS:
        balls.extend([color] * BALLS_PER_TUBE)

    # Shuffle balls
    random.shuffle(balls)

    # Distribute balls among the tubes, leave 2 tubes empty
    for i in range(NUM_TUBES - 2):
        for _ in range(BALLS_PER_TUBE):
            tubes[i].append(balls.pop())

    move_count = 0
    update_display()

# Function to handle tube selection
def on_tube_click(tube_index):
    global selected_tube

    if selected_tube is not None:
        # Move ball from selected tube to clicked tube if possible
        if selected_tube != tube_index and move_ball(selected_tube, tube_index):
            selected_tube = None
            update_display()
            check_win_condition()
        else:
            selected_tube = None
    else:
        # Select this tube
        selected_tube = tube_index
        update_display()

# Function to move a ball from one tube to another
def move_ball(from_tube, to_tube):
    global move_count

    if tubes[from_tube] and len(tubes[to_tube]) < BALLS_PER_TUBE:
        if not tubes[to_tube] or tubes[to_tube][-1] == tubes[from_tube][-1]:
            save_undo_state()  # Save the current state for undo
            tubes[to_tube].append(tubes[from_tube].pop())
            move_count += 1
            return True
    return False

# Function to check if the player has won
def check_win_condition():
    for tube in tubes:
        if len(tube) == BALLS_PER_TUBE and len(set(tube)) == 1:
            continue
        elif len(tube) == 0:
            continue
        else:
            return
    messagebox.showinfo("You Win!", f"Congratulations! You solved it in {move_count} moves.")
    reset_game()

# Function to update the display of the tubes and balls
def update_display():
    canvas.delete("all")  # Clear the canvas before redrawing

    tube_width = 50
    tube_height = 300
    tube_x_spacing = 120
    tube_y_start = 100

    for i, tube in enumerate(tubes):
        # Draw the test tube (as a rectangle)
        x0 = 50 + i * tube_x_spacing
        y0 = tube_y_start
        x1 = x0 + tube_width
        y1 = y0 + tube_height
        canvas.create_rectangle(x0, y0, x1, y1, width=3)

        # Draw the balls inside the tube
        for j, color in enumerate(tube):
            ball_x0 = x0 + 5
            ball_y0 = y1 - (j + 1) * 2 * BALL_RADIUS - 10
            ball_x1 = ball_x0 + 2 * BALL_RADIUS
            ball_y1 = ball_y0 + 2 * BALL_RADIUS
            canvas.create_oval(ball_x0, ball_y0, ball_x1, ball_y1, fill=color)

        # Highlight selected tube
        if selected_tube == i:
            canvas.create_rectangle(x0, y0, x1, y1, width=5, outline="blue")

    # Update move counter display
    move_label.config(text=f"Moves: {move_count}")

# Function to reset the game
def reset_game():
    global tubes, selected_tube, move_count, UNDO_STACK
    tubes = [[] for _ in range(NUM_TUBES)]
    selected_tube = None
    move_count = 0
    UNDO_STACK = []
    initialize_tubes()

# Function to undo the last move
def undo_move():
    global tubes, move_count
    if UNDO_STACK:
        tubes = copy.deepcopy(UNDO_STACK.pop())
        move_count -= 1
        update_display()

# Function to save the current state for undo
def save_undo_state():
    global UNDO_STACK
    UNDO_STACK.append(copy.deepcopy(tubes))

# Create a reset button
reset_button = tk.Button(root, text="Reset", command=reset_game)
reset_button.pack(side=tk.BOTTOM, pady=20)

# Create an undo button
undo_button = tk.Button(root, text="Undo", command=undo_move)
undo_button.pack(side=tk.BOTTOM, pady=5)

# Create a move counter label
move_label = tk.Label(root, text=f"Moves: {move_count}")
move_label.pack(side=tk.BOTTOM, pady=5)

# Mouse click event to select the tube
def on_canvas_click(event):
    tube_width = 50
    tube_x_spacing = 120
    x_click = event.x

    # Detect which tube is clicked based on x-coordinate
    for i in range(NUM_TUBES):
        x0 = 50 + i * tube_x_spacing
        x1 = x0 + tube_width
        if x0 <= x_click <= x1:
            on_tube_click(i)
            break

# Bind mouse clicks to the canvas
canvas.bind("<Button-1>", on_canvas_click)

# Initialize the puzzle with random balls
initialize_tubes()

# Start the main event loop
root.mainloop()
