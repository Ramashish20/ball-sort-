
import random
import pygame
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter


#fixed number of ball in a testtube
NUM_BALLS_PER_TUBE = 4

# Define the number of tubes and colors
NUM_TUBES = 6
NUM_COLORS = 4

# Colors for balls (use simple color names)
BALL_COLORS = ["red", "blue", "green",  "violet", "yellow"]

# Generate random tubes
def generate_tubes():
    colors = []
    for color in range(NUM_COLORS):
        colors.extend([color] * NUM_BALLS_PER_TUBE)
        print(colors)

    random.shuffle(colors)
    print(colors)

    tubes = []
    index = 0
    #using underscore becuase loop variable is not needed so no need to store it which will takes some memory space
    for _ in range(NUM_TUBES):
        if index < len(colors):
            tubes.append(colors[index:index + NUM_BALLS_PER_TUBE])
            index += NUM_BALLS_PER_TUBE
        else:
            tubes.append([])  # Empty tube
    return tubes
    

# Initialize tubes
tubes = generate_tubes()
print(tubes)
def is_valid_move(tube_from, tube_to):
    if not tubes[tube_from]: # tube_from is empty
        return False
    if not tubes[tube_to]: # tube_to is empty
        return True
    if len(tubes[tube_to]) >= NUM_BALLS_PER_TUBE: # tube_to cannot hold more than 4 balls
        return False
    return tubes[tube_from][0] == tubes[tube_to][0]  # Colors must match
    

def make_move(tube_from, tube_to):
    if is_valid_move(tube_from, tube_to):
        ball = tubes[tube_from].pop(0)  # Remove ball from tube_from
        tubes[tube_to].insert(0,ball) 
           # Add ball to tube_to
        return True
    return False


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
        self.geometry("800x600")  # Adjust the size to fit the tubes
        self.resizable(False, False)

        # Variable to store selected tube
        self.selected_tube = None

        # Initialize Pygame mixer for background music
        
        pygame.mixer.init()
        pygame.mixer.music.load(r"D:\Computer Science\internal project\ds\frontend\perfect-beauty-191271.mp3")
        pygame.mixer.music.play(loops=1) 

        # Draw the tubes and balls
        self.tube_frames = []
        self.draw_tubes()

        # Create Undo button
        

      # Set size to fit the window
        self.columnconfigure((0, 1, 2, 3, 4,5,), weight=1)
        self.rowconfigure((0),weight=1)
        self.rowconfigure((1),weight=5)

        # header_image=self.resizable_image("D:/Computer Science/internal project/ds/th.jpeg",800,300)
        ctk.CTkLabel(self,text="Ball Sort",text_color="black",font=("Times", 50, "bold"),fg_color="#a2d2ff").grid(row=0,column=0,columnspan=10,sticky="nsew")
    

    def draw_tubes(self):
        for i, tube in enumerate(tubes):
            frame = ctk.CTkFrame(self, width=90, height=355,
                                border_color="black", border_width=3, corner_radius=50)
            frame.grid(row=1, column=i, padx=10, pady=10)
            self.temp=ctk.CTkFrame(self,width=90,height=20,border_width=3,border_color="black")
            self.temp.grid(row=1,column=i,sticky="n",pady=80)
            self.temp.lift()
            frame.grid_propagate(False)
            self.tube_frames.append(frame)
            self.draw_balls_in_tube(i)

            frame.bind("<Button-1>", lambda e, idx=i: self.select_tube(idx))


    def resizable_image(self, image_path, x, y):
        image = Image.open(image_path)
        imageresize = image.resize((x, y))
        readyimage = ImageTk.PhotoImage(imageresize)
        return readyimage
    # ... [rest of your methods] ...



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
            label.bind("<Button-1>", lambda e, tube_idx=tube_idx: self.select_ball(tube_idx))

    def select_tube(self, tube_idx):
        if self.selected_tube is None:
            self.selected_tube = tube_idx
            self.highlight_tube(tube_idx)
        else:
            if self.selected_tube != tube_idx:
                if make_move(self.selected_tube, tube_idx):
                    self.draw_balls_in_tube(self.selected_tube)
                    self.draw_balls_in_tube(tube_idx)
                self.reset_highlight()  # Reset the highlight before unselecting
                self.selected_tube = None
                self.check_win_condition()

    def select_ball(self, tube_idx):
        if self.selected_tube is None:
            self.selected_tube = tube_idx
            self.highlight_tube(tube_idx)
        else: 
            if self.selected_tube != tube_idx:
                if make_move(self.selected_tube, tube_idx):
                    self.draw_balls_in_tube(self.selected_tube)
                    self.draw_balls_in_tube(tube_idx)
                self.reset_highlight()  # Reset the highlight before unselecting
                self.selected_tube = None
                self.check_win_condition()
                

    def highlight_tube(self, tube_idx):
        frame = self.tube_frames[tube_idx]
        # Highlight all balls in the tube
        frame.configure(border_color="white",bg_color="white")
        # for widget in frame.winfo_children():
        #     widget.configure(bg_color="#fffcf2")

    def reset_highlight(self):
        for i, frame in enumerate(self.tube_frames):
            # Reset the color of all balls in each tube
            for j, widget in enumerate(frame.winfo_children()):
                ball_color = BALL_COLORS[tubes[i][j]] if j < len(tubes[i]) else "grey"
                widget.configure(fg_color=ball_color)
                frame.configure(border_color="black",bg_color="transparent")  # Reset to original color 

    def check_win_condition(self):
        if is_game_won():
            win_label = ctk.CTkLabel(self, text="Congratulations! You won the game!", font=("Arial", 16), text_color="green")
            win_label.grid(row=1, columnspan=len(tubes), pady=10)

# Start the game
if __name__ == "__main__":
    app = BallSortGame()
    app.mainloop()
