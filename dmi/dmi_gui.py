import tkinter as tk
import tkinter.messagebox as messagebox
import ctypes

window_name = "DMI Kola"  # Kort over lynnedslag app

ctypes.windll.shcore.SetProcessDpiAwareness(1)
main_window = tk.Tk()
main_window.title(window_name)
padx=8
pady=4

if __name__ == "__main__":
    messagebox.showerror(main_window, "Ingen API key suppleret! V")