import tkinter as tk
from tkinter import ttk

even_row_color = "#cccccc"
odd_row_color = "#dddddd"
treeview_background = "#eeeeee"
row_height = 24

main_window = tk.Tk()
main_window.title = "Dansk Cargo Containeradministrationsprogram"
main_window.geometry("1500x500")
padx=8
pady=4

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=treeview_background, rowheight=row_height)

container_frame = tk.LabelFrame(main_window, text="Container")
container_frame.grid(row=0, column=0, padx=padx, pady=pady)

container_treeviewframe = tk.Frame(container_frame)
container_treeviewframe.grid(row=0, column=0, padx=padx, pady=pady)

container_treeview_scrollbar = tk.Scrollbar(container_treeviewframe)
container_treeview_scrollbar.grid(row=0, column=1, padx=padx, pady=pady, sticky="ns")
container_treeview = ttk.Treeview(container_treeviewframe, yscrollcommand=container_treeview_scrollbar.set, selectmode="browse")
container_treeview.grid(row=0, column=0, padx=0, pady=pady)
container_treeview_scrollbar.config(command=container_treeview.yview)

if __name__ == "__main__":
    main_window.mainloop()