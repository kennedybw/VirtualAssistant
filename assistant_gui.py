import tkinter as tk
from tkinter import PhotoImage


def create_gui(greet_text):
    window = tk.Tk()
    window.title("Virtual Assistant")
    window.geometry("400x400")

    # icon 
    window.icon_image = PhotoImage(file="VAicon.png")
    icon_label = tk.Label(window, image=window.icon_image)
    icon_label.pack(pady=10)

    output_text = tk.Text(window, height=5, wrap ="word")
    output_text.pack(pady=10)

    # display virtual assistant's words to the screen
    def speak_and_display(text):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text + "\n")
        output_text.see(tk.END)

    speak_and_display(greet_text)
    

    return window, speak_and_display