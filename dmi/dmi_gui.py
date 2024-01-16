import tkinter as tk
from tkinter import ttk
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
even_row_color = "#cccccc"
odd_row_color = "#dddddd"
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#209bef"
row_height = 24


style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=treeview_background, foreground=treeview_foreground, rowheight=row_height, fieldbackground=treeview_background)
style.map("Treeview", background=[("selected", treeview_selected)])

df.parseargs(sys.argv[1:])
api_key = df.get_key()

progress = tk.IntVar()
initial_map = Image.open("denmark_osm_small.png")
initial_map_tk = ImageTk.PhotoImage(initial_map)
initial_map_resized = initial_map.resize((500, 426))
initial_map_resized = ImageTk.PhotoImage(initial_map_resized)

map_frame = tk.Frame(main_window)
map_frame.pack()
map_label = tk.Label(map_frame, image=initial_map_tk)
map_label.pack(side=tk.LEFT)
tree_frame = tk.Frame(map_frame)
tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
tree_scroll = tk.Scrollbar(tree_frame)
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("municipality", "lightning_strikes"))
tree.column("#0", width=0, stretch=tk.NO)
tree.column("municipality", anchor=tk.E, width=200)
tree.column("lightning_strikes", anchor=tk.E, width=120)
tree.heading("#0", text="", anchor=tk.W)
tree.heading("municipality", text="Kommune", anchor=tk.CENTER)
tree.heading("lightning_strikes", text="Lynnedslag", anchor=tk.CENTER)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.tag_configure("oddrow", background=odd_row_color)
tree.tag_configure("evenrow", background=even_row_color)
tree_scroll.config(command=tree.yview)
tree_scroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

controls_button_frame = tk.Frame(main_window)
controls_button_frame.pack()

controls_frame = tk.Frame(controls_button_frame)
controls_frame.grid(row=0, column=0, padx=padx, pady=pady)
year_label = tk.Label(controls_frame, text="Årstal")
year_label.grid(row=0, column=0, padx=padx, pady=pady)
year_entry = tk.Entry(controls_frame, width=6)
year_entry.bind("<Return>", lambda event: df.do_kola(year_entry.get()))
year_entry.grid(row=1, column=0, padx=padx, pady=pady)

buttons_frame = tk.Frame(controls_button_frame)
buttons_frame.grid(row=0, column=1, padx=padx, pady=pady)
request_button = tk.Button(buttons_frame, text="Tegn Lynnedslag", command=lambda: df.do_kola(year_entry.get()))
request_button.grid(row=0, column=0, padx=padx, pady=pady)
clear_button = tk.Button(buttons_frame, text="Slet Lynnedslag", command=df.clear)
clear_button.grid(row=0, column=1, padx=padx, pady=pady)
save_button = tk.Button(buttons_frame, text="Gem Kort", command=df.save_as)
save_button.grid(row=0, column=2, padx=padx, pady=pady)

progress_frame = tk.Frame(main_window)
progress_frame.pack(expand=True)

progress_bar_frame = tk.Frame(progress_frame)
progress_bar_frame.grid(row=0, column=0, sticky=tk.W)
progress_bar_label = tk.Label(progress_bar_frame, text="")
progress_bar_label.grid(row=0, column=0, padx=padx, pady=pady)
progress_bar = ttk.Progressbar(progress_bar_frame, length=200, variable=progress)
progress_bar.grid(row=1, column=0, padx=padx, pady=pady)
progress_eta_label = tk.Label(progress_bar_frame, text="")
progress_eta_label.grid(row=2, column=0, padx=padx, pady=pady)

progress_info_frame = tk.LabelFrame(progress_frame, text="Status")
progress_info_frame.grid(row=0, column=1, sticky=tk.E, padx=padx, pady=pady)
progress_info_scroll = tk.Scrollbar(progress_info_frame)
progress_info_text = tk.Text(progress_info_frame, bg="white", fg="black", height=10, width=40, state="disabled", yscrollcommand=progress_info_scroll.set)
progress_info_scroll.config(command=progress_info_text.yview)
progress_info_text.config(spacing1=1.5)
progress_info_text.config(spacing3=1.5)
progress_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(padx, 0), pady=pady)
progress_info_scroll.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, padx), pady=pady)


df.load_into_func(main_window, progress_bar_label, progress_info_text, progress_bar, progress, progress_eta_label, map_label, request_button, tree)

if __name__ == "__main__":
    if api_key == False:
        messagebox.showerror(window_name, "Ingen API key suppleret!\nKør scriptet med -k {KEY} eller placér en tekstfil med API key i projektets mappe, og kald den key.txt.", parent=main_window)
    main_window.mainloop()
