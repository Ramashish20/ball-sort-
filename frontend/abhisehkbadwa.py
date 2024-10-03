import customtkinter as ctk
import pygame
from PIL import Image, ImageTk

class ShotPutGame:
    def __init__(self, app):  # Corrected __init__ method
        self.app = app
        self.app.title('Shot Put Game')
        self.app.config(bg='sky blue')
        self.app.geometry('800x600')
        
        # Initialize Pygame mixer for background music
        pygame.mixer.init()
        pygame.mixer.music.load(r"frontend\music.mp3")
        pygame.mixer.music.play(loops=1)

        # Load the main image
        self.img = Image.open(r"images\WhatsApp Image 2024-10-02 at 19.50.03_5f74c71d.jpg")
        self.photo = ImageTk.PhotoImage(self.img)

        # Create and pack the main label with the image
        self.label = ctk.CTkLabel(self.app, image=self.photo, text="")
        self.label.pack(pady=50)

        # Load the button image
        button_img = Image.open(r"images\arrow.jpg")
        button_img = button_img.resize((30, 30), Image.LANCZOS)
        self.button_photo = ctk.CTkImage(button_img)

        # Create and pack the play button
        self.play_button = ctk.CTkButton(
            self.app,
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
        print("You entered the game")
        self.game_over()

    def game_over(self):
        self.game_over = ctk.CTkToplevel(self.app)
        self.game_over.title("Game Over")
        self.game_over.geometry("200x200")
        self.game_over.configure(bg="sky blue")

        l = ctk.CTkLabel(self.game_over, text="Game Over", font=("Helvetica", 10, "bold"), fg_color="yellow")
        l.pack(pady=10)

        playbutton = ctk.CTkButton(self.game_over, text="Play Again", command=self.play)
        playbutton.pack(padx=20, pady=20)

        exitbutton = ctk.CTkButton(self.game_over, text="Exit", command=self.exit)
        exitbutton.pack(padx=30, pady=20)

    def play(self):
        self.game_over.destroy()
        self.on_click()

    def exit(self):
        self.app.quit()

if __name__ == "__main__":
    apps = ctk.CTk()
    game = ShotPutGame(apps)
    apps.mainloop()
