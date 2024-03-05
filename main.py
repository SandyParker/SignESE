import tkinter as tk
from PIL import Image, ImageTk
from gtts import gTTS
import os
import cv2
# import pygame
from io import BytesIO

class CameraApp:
    def __init__(self, parent_frame):
        self.vid = None  # Initialize vid as None
        self.frame = tk.Frame(parent_frame, bg='lightblue')
        self.frame.pack(fill='both', expand=True)

        self.label_widget = tk.Label(self.frame)
        self.label_widget.pack()

        # Load camera icon image
        icon_image = Image.open("camera-solid-24.png")
        self.icon_photo = ImageTk.PhotoImage(icon_image)

        self.open_button = tk.Button(self.frame, text="Open Camera", command=self.toggle_camera, bg='lightgreen', bd=4, font=('Arial', 14))
        self.open_button.pack(pady=20)

        self.close_button = tk.Button(self.frame, text="Close Camera", command=self.close_camera, bg='tomato', bd=4, font=('Arial', 14), state='disabled')
        self.close_button.pack(pady=5)

        self.camera_opened = False

    def toggle_camera(self):
        if not self.camera_opened:
            self.open_camera()
        else:
            self.close_camera()

    def open_camera(self):
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.camera_opened = True
        self.open_button.config(state='disabled')
        self.close_button.config(state='normal')
        self.show_frame()

    def close_camera(self):
        if self.vid:
            self.vid.release()  # Release the video capture resources
        self.label_widget.config(image='')
        self.label_widget.photo_image = None
        self.open_button.config(state='normal')
        self.close_button.config(state='disabled')
        self.camera_opened = False

    def show_frame(self):
        _, frame = self.vid.read()
        if frame is not None:
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            self.label_widget.photo_image = photo_image
            self.label_widget.configure(image=photo_image)
            self.label_widget.after(10, self.show_frame)


class TextApp:
    def __init__(self, parent_frame):
        self.frame = tk.Frame(parent_frame, bg='lightblue')  # Modified background color
        self.frame.pack(fill='both', expand=True)

        self.facts = []
        self.current_fact_index = 0

        self.label = tk.Label(self.frame, text="Text to Speech", font="bold, 30", bg="lightgreen")  # Modified background color
        self.label.pack(fill=tk.X, pady=20)

        self.fact_entry = tk.Entry(self.frame, width=45, bd=4, font=('Arial', 14))
        self.fact_entry.pack(pady=10)

        button_frame = tk.Frame(self.frame, bg='lightblue')  # Modified background color
        button_frame.pack(pady=10)

        clear_button = tk.Button(button_frame, text="Clear Text", command=self.clear_text, bg='lightgreen', bd=4, font=('Arial', 14))
        clear_button.pack(side=tk.LEFT, padx=10)

        self.play_button = tk.Button(button_frame, text="Play Audio", command=self.play, bg='lightgreen', bd=4, font=('Arial', 14))
        self.play_button.pack(side=tk.LEFT, padx=10)

        # Dropdown menu for language selection
        self.language_var = tk.StringVar(self.frame)
        self.language_var.set("en")  # Default language is English
        languages = ["en", "es", "fr", "de", "hi", "it", "ja", "kn", "ml", "ru", "sa", "ta", "te"]  # Add more languages as needed
        language_dropdown = tk.OptionMenu(button_frame, self.language_var, *languages)
        language_dropdown.config(bg='lightgreen', bd=4, font=('Arial', 14))  # Modified background color
        language_dropdown.pack(side=tk.LEFT, padx=10)

        # self.t = tk.Text(self.frame, height=5, width=70, font=('Arial', 12))
        # self.t.pack(pady=20)
        # self.t.config(state=tk.DISABLED)

        self.audio_data = None

    def add_fact(self):
        fact = self.fact_entry.get()
        if fact:
            self.facts.append(fact)
            self.fact_entry.delete(0, tk.END)
            self.update_fact()

    def next_fact(self):
        if self.facts:
            self.current_fact_index = (self.current_fact_index + 1) % len(self.facts)
            self.update_fact()

    def clear_text(self):
        self.fact_entry.delete(0, tk.END)

    def play(self):
        if self.fact_entry.get():
            language = self.language_var.get()  # Get the selected language from the dropdown
            tts = gTTS(text=self.fact_entry.get(), lang=language, slow=False)
            audio_data = BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()

    def update_fact(self):
        self.t.config(state=tk.NORMAL)
        self.t.delete('1.0', tk.END)
        if self.facts:
            self.t.insert(tk.END, self.facts[self.current_fact_index])
        self.t.config(state=tk.DISABLED)

def on_escape(event):
    root.quit()

root = tk.Tk()
root.title("SIGN-ESE")

camera_app = CameraApp(root)
text_app = TextApp(root)

root.bind('<Escape>', on_escape)
root.mainloop()
