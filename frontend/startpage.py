import customtkinter as ctk
import pygame
from PIL import Image, ImageTk
from gui import BallSortGame

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

        self.is_music_playing=1

        # Initialize Pygame mixer for background music
        pygame.mixer.init()
        pygame.mixer.music.load(r"./music/perfect-beauty-191271.mp3")
        pygame.mixer.music.play(loops=1)



        # Create and pack the main label with the image
        self.label = ctk.CTkLabel(self, text="",image=self.resizable_Images("./Images/startphoto.png",500,450))
        self.label.grid(row=0,column=0)
       


   

        # Create and pack the play button
        self.play_button = ctk.CTkButton(
            self,
            text="Play",
            image=self.resizable_Images("./Images/play.png",30,30),
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
        self.play_button.place(relx=0.41,rely=0.8)
        self.play_button.lift()

        self.music = ctk.CTkButton(
        self,
        image=self.resizable_Images("./Images/musicplay.png", 30, 30,), text="",
        command=self.toggle_music,
        fg_color="#ede8d0", bg_color="#060644",
        corner_radius=10,
        border_color="black", border_width=2,
        width=20, hover_color="white",
    )
        self.music.grid(row=2,pady=10)

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

    def toggle_music(self):
        if self.is_music_playing==1:
            pygame.mixer.music.stop()
            self.is_music_playing = 0
            self.music.configure(image=self.resizable_Images("./Images/music.png", 30, 30))
        else:
            pygame.mixer.music.play(loops=-1)
            self.is_music_playing = 1
            self.music.configure(image=self.resizable_Images("./Images/musicplay.png", 30, 30))

    def resizable_Images(self, image_path, x, y):
        image = Image.open(image_path)
        imageresize = image.resize((x, y))
        readyimage = ImageTk.PhotoImage(imageresize)
        return readyimage

if __name__ == "__main__":
    game = Game()
    game.mainloop()