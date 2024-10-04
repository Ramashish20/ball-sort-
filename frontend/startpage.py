import customtkinter as ctk
import pygame
from PIL import Image, ImageTk
from gamestart import BallSortGame

class Game(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Shot Put Game')
        self.config(bg="#060644")
        self.geometry('800x550')
        self.resizable(False,False)
        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0),weight=1)
        
        #doing the window in middle 
        self.middle(800,550)
    
        # Initialize Pygame mixer for background music
        pygame.mixer.init()
        pygame.mixer.music.load(r"./music/perfect-beauty-191271.mp3")
        pygame.mixer.music.play(loops=1)

        # Load the main image
        self.img = Image.open("./Images/startphoto.png")
        self.photo = ImageTk.PhotoImage(self.img)

        # Create and pack the main label with the image
        self.label = ctk.CTkLabel(self, text="",image=self.photo)
        self.label.grid(row=0,column=0)
       


        # Load the button image
        button_img = Image.open("./Images/arrow.jpg")
        button_img = button_img.resize((30, 30), Image.LANCZOS)
        self.button_photo = ctk.CTkImage(button_img)

        # Create and pack the play button
        self.play_button = ctk.CTkButton(
            self,
            text="Play",
            image=self.button_photo,
            compound="left",
            corner_radius=10,
            height=40,
            width=150,
            fg_color="#feed35",
            hover_color="white",
            text_color="black",
            border_width=2,
            font=("Helvetica", 14, "bold"),
            command=self.on_click
        )
        self.play_button.grid(row=0,column=0,sticky="s",pady=40)
        self.play_button.lift()

    def middle(self,width,height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


    def on_click(self):
        self.destroy()
        ballsort=BallSortGame()
        ballsort.mainloop()


if __name__ == "__main__":
    game = Game()
    game.mainloop()