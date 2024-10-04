import random
import copy
import pygame
import customtkinter as ctk
from PIL import Image, ImageTk

# Stack Classes

class Node:
    def __init__(self, data):
        self.data = data
        self.nextnode = None

    def showInfo(self):
        print("Node Info --> " + str(self.data))


class Undo:
    def __init__(self):
        self.top = None

    def push(self, newnode):
        newnode.nextnode = self.top
        self.top = newnode

    def peek(self):
        return self.top

    def pop(self):
        if self.top is None:
            return None
        else:
            s = self.top
            self.top = self.top.nextnode
            return s


# Fixed number of balls in a test tube
NUM_BALLS_PER_TUBE = 4
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
        self.config(background="#060644")
        self.selected_tube = None
        self.undo_stack = Undo()  # Use the DataStack for undo operations

        # Middle window
        #self.middle(800, 600)

        # To verify if music is playing or not
        self.is_music_playing = 1
        pygame.mixer.init()
        pygame.mixer.music.load("./music/perfect-beauty-191271.mp3")
        pygame.mixer.music.play(loops=-1)

        self.tube_frames = []
        self.tube_frames=[]
        self.draw_tubes()

        # Ball sort heading text
        ctk.CTkLabel(self, text="Ball Sort", text_color="black", font=("Times", 50, "bold"), fg_color="#ebd469").grid(
            row=0, column=0, columnspan=10, sticky="nsew")

        # Add the Undo button
        self.undo_button = ctk.CTkButton(
            self,
            image=self.resizable_Images("./Images/undo.png", 30, 30), text="",
            command=self.undo_move,
            fg_color="#ede8d0", bg_color="#ebd469",
            corner_radius=10,
            border_color="black", border_width=2,
            width=20, hover_color="white",
            state='disabled'  # Initially disabled as no move has been made
        )
        self.undo_button.grid(row=0, column=0, columnspan=6, padx=10, sticky="w")
        self.undo_button.lift()

        # OFF MUSIC BUTTON   
        self.music = ctk.CTkButton(
            self,
            image=self.resizable_Images("./Images/music.png", 30, 30), text="",
            command=self.toggle_music,
            fg_color="#ede8d0", bg_color="#ebd469",
            corner_radius=10,
            border_color="black", border_width=2,
            width=20, hover_color="white",
        )
        self.music.grid(row=0, column=0, columnspan=6, padx=10, sticky="e")
        self.music.lift()

        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.rowconfigure((0), weight=1)
        self.rowconfigure((1), weight=5)

    def toggle_music(self):
        if self.is_music_playing:
            # Stop the music
            pygame.mixer.music.stop()
            self.is_music_playing = 0
        else:
            # Start the music again
            pygame.mixer.music.play(loops=-1)
            self.is_music_playing = 1

    def resizable_Images(self, image_path, x, y):
        image = Image.open(image_path)
        imageresize = image.resize((x, y))
        readyimage = ImageTk.PhotoImage(imageresize)
        return readyimage

    def draw_tubes(self):
        for i, tube in enumerate(tubes):
            self.frame = ctk.CTkFrame(self, width=90, height=355, border_color="white", border_width=3, fg_color="#060644", bg_color="#060644", corner_radius=50)
            self.frame.grid(row=1, column=i, padx=10, pady=10)
            self.temp = ctk.CTkFrame(self, width=90, height=20, fg_color="#060644", border_width=3, border_color="white")
            self.temp.grid(row=1, column=i, sticky="n", pady=80)
            self.temp.lift()
            self.frame.rowconfigure((0, 1, 2, 3), weight=5)
            self.frame.grid_propagate(False)
            self.tube_frames.append(self.frame)
            self.draw_balls_in_tube(i)
            self.frame.bind("<Button-1>", lambda e, idx=i: self.select_tube(idx))

    def draw_balls_in_tube(self, tube_idx):
        self.frame = self.tube_frames[tube_idx]
        for widget in self.frame.winfo_children():
            widget.destroy()

        for idx, ball in enumerate(tubes[tube_idx]):
            color = BALL_COLORS[ball]
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
            label.grid(row=idx, column=0, pady=14, padx=15)
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
            else:
                self.reset_highlight()
                self.selected_tube = None

        if is_game_won():
            self.display_winning_frame()

    def highlight_tube(self, tube_idx):
        self.tube_frames[tube_idx].configure(border_color="yellow")
       
    def reset_highlight(self):
        for tube_idx in range(NUM_TUBES):
            self.tube_frames[tube_idx].configure(border_color="white")

    def save_undo_state(self):
        state_copy = copy.deepcopy(tubes)  # Create a deep copy of the current state
        self.undo_stack.push(Node(state_copy))  # Push the state onto the undo stack

    def undo_move(self):
        if self.undo_stack.peek() is not None:
            last_state = self.undo_stack.pop().data  # Get the last state
            global tubes
            tubes = last_state  # Restore the last state
            self.update_display()  # Update the display for all tubes
            if self.undo_stack.peek() is None:  # Disable undo if there's no more states
                self.undo_button.configure(state='disabled')

    def update_display(self):
        for tube_idx in range(NUM_TUBES):
            self.draw_balls_in_tube(tube_idx)

    def display_winning_frame(self):
        self.win_frame=ctk.CTkFrame(self,height=150,width=150,fg_color="#ebd469")
        self.win_frame.place(x=200,y=300)

        self.win_frame.columnconfigure((0,1),weight=1)
        self.win_frame.rowconfigure((0,1),weight=1)

        win_label = ctk.CTkLabel(self.win_frame, text="Congratulations! You won the game!",font=("Times", 28, "bold"), text_color="green",height=30,width=100)
        win_label.grid(row=0,column=0, columnspan=2, pady=10,padx=10)

        play_again=ctk.CTkButton(self.win_frame,command=self.play_again,text="Play Again",height=30,width=40,hover_color="#4895ef",fg_color="#060644",font=("arial", 20, "bold"))
        play_again.grid(row=1,column=0,padx=5,pady=10)

        exitt=ctk.CTkButton(self.win_frame,command=self.main_menu,text="Main Menu",height=30,width=140,hover_color="#4895ef",fg_color="#060644",font=("arial", 20, "bold"))
        exitt.grid(row=1,column=1,padx=5,pady=10)
        exitt.lift()

    def play_again(self):
        self.win_frame.destroy()
        global tubes
        tubes = generate_tubes()  # Reset the game state with new tubes
        self.update_display()  # Update the display for all tubes
        self.undo_stack = Undo()  # Reset the undo stack
        self.undo_button.configure(state='disabled')  # Disable undo button
    
    def main_menu(self):
        self.destroy()
        from startpage import Game
        Game=Game()
        Game.mainloop()

# Run the application
if __name__ == "__main__":
    app = BallSortGame()
    app.mainloop()
