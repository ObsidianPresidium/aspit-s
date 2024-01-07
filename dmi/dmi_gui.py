import tkinter as tk
import tkinter.messagebox as messagebox
import dmi_func as df
import sys
from PIL import ImageTk, Image
import ctypes

window_name = "DMI Kola"  # Kort over lynnedslag app

main_window = tk.Tk()
main_window.title(window_name)
padx=8
pady=4

df.parseargs(sys.argv[1:])
api_key = df.get_key()

initial_map = Image.open("denmark_osm_small.png")
initial_map_tk = ImageTk.PhotoImage(initial_map)
initial_map_resized = initial_map.resize((500, 426))
initial_map_resized = ImageTk.PhotoImage(initial_map_resized)

map_frame = tk.Frame(main_window)
map_frame.pack()
map_label = tk.Label(map_frame, image=initial_map_tk)
map_label.pack()

controls_button_frame = tk.Frame(main_window)
controls_button_frame.pack()

controls_frame = tk.Frame(controls_button_frame)
controls_frame.grid(row=0, column=0, padx=padx, pady=pady)
year_label = tk.Label(controls_frame, text="Årstal")
year_label.grid(row=0, column=0, padx=padx, pady=pady)
year_entry = tk.Entry(controls_frame, width=6)
year_entry.grid(row=1, column=0, padx=padx, pady=pady)

buttons_frame = tk.Frame(controls_button_frame)
buttons_frame.grid(row=0, column=1, padx=padx, pady=pady)
request_button = tk.Button(buttons_frame, text="Tegn Lynnedslag", command=lambda: df.do_kola(map_label, year_entry.get()))
request_button.grid(padx=padx, pady=pady)

if __name__ == "__main__":
    if api_key == False:
        messagebox.showerror(window_name, "Ingen API key suppleret!\nKør scriptet med -k {KEY} eller placér en tekstfil med API key i projektets mappe, og kald den key.txt.")
    main_window.mainloop()
