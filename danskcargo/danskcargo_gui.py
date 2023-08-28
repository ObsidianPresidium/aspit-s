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

frame_container = tk.LabelFrame(main_window, text="Container")
frame_container.grid(row=0, column=0, padx=padx, pady=pady)

tree_frame_container = tk.Frame(frame_container)
tree_frame_container.grid(row=0, column=0, padx=padx, pady=pady)

tree_scroll_container = tk.Scrollbar(tree_frame_container)
tree_scroll_container.grid(row=0, column=1, padx=padx, pady=pady, sticky="ns")
tree_container = ttk.Treeview(tree_frame_container, yscrollcommand=tree_scroll_container.set, selectmode="browse")
tree_container.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_container.config(command=tree_container.yview)

if __name__ == "__main__":
    main_window.mainloop()