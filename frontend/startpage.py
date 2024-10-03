import customtkinter as ctk
import pygame
from PIL import Image, ImageTk
from gamestart import BallSortGame

class ShotPutGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Shot Put Game')
        self.config(bg='sky blue')
        self.geometry('800x600')
        
        # Initialize Pygame mixer for background music
        pygame.mixer.init()
        pygame.mixer.music.load("./music.mp3")
        pygame.mixer.music.play(loops=1)

        # Load the main image
        # self.img = Image.open(r"D:\Computer Science\internal project\ds\images\WhatsApp Image 2024-10-02 at 19.50.03_5f74c71d.jpg")
        # self.photo = ImageTk.PhotoImage(self.img)

        # Create and pack the main label with the image
        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(pady=50)

        # Load the button image
        button_img = Image.open(r"D:\Computer Science\internal project\ds\ball-sort-\images\arrow.jpg")
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
            fg_color="pink",
            hover_color="white",
            text_color="black",
            border_width=2,
            font=("Helvetica", 14, "bold"),
            command=self.on_click
        )
        self.play_button.pack(pady=20)

    def on_click(self):
        game.destroy()
        ballsort=BallSortGame()
        ballsort.mainloop()
if __name__ == "__main__":
    game = ShotPutGame()
    game.mainloop()