""" Opgave "GUI step 4":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2040.png

Genbrug din kode fra "GUI step 3".

Fyld treeview'en med testdata.
Leg med farveværdierne. Find en farvekombination, som du kan lide.

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).
    Hvis du klikker på en datarække i træoversigten, kopieres dataene i denne række til indtastningsfelterne.

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as tk
from tkinter import ttk


even_row_color = "#cccccc"
odd_row_color = "#dddddd"
treeview_background = "#eeeeee"
row_height = 24


test_data = [
    ("1", 1000, "oslo"),
    ("2", 2000, "chicago"),
    ("3", 3000, "milano"),
    ("4", 4000, "amsterdam")
]

def read_table(tree):
    for i in enumerate(test_data):
        if i[0] % 2 == 0: # even
            tree.insert(parent="", index="end", text="", values=i[1], tags=("evenrow",))
        else:
            tree.insert(parent="", index="end", text="", values=i[1], tags=("oddrow",))

def empty_entries():
    print("Empty entries button was pressed")
    for i in entries:
        i.delete(0, tk.END)

def copy_entries(event, tree):
    index_selected = tree.focus()
    values = tree.item(index_selected, "values")
    for i in enumerate(entries):
        if not i[1] == entries[-1]: # skip the last one as weather isn't implemented
            i[1].delete(0, tk.END)
            i[1].insert(0, values[i[0]])

main_window = tk.Tk()
main_window.title("my first GUI")
main_window.geometry("493x466")
padx=8
pady=4
entries = []

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=treeview_background, rowheight=row_height)

frame_1 = tk.LabelFrame(main_window, text="Container")
frame_1.grid(row=0, padx=padx, pady=pady)

frame_1.pack(fill="both", expand=True, padx=padx, pady=pady)

frame_1_1 = tk.Frame(frame_1)
frame_1_1.grid(row=0, column=0, padx=padx, pady=pady)

tree_scrollbar = tk.Scrollbar(frame_1_1)
tree_scrollbar.grid(row=0, column=1, padx=pady, pady=pady, sticky="ns")
tree = ttk.Treeview(frame_1_1, yscrollcommand=tree_scrollbar.set, selectmode="browse")
tree.grid(row=0, column=0, padx=0, pady=pady)
tree_scrollbar.config(command=tree.yview)

tree["columns"] = ("col1", "col2", "col3")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("col1", anchor=tk.E, width=50)
tree.column("col2", anchor=tk.E, width=100)
tree.column("col3", anchor=tk.W, width=180)

tree.heading("#0", text="", anchor=tk.W)
tree.heading("col1", text="Id", anchor=tk.CENTER)
tree.heading("col2", text="Weight", anchor=tk.CENTER)
tree.heading("col3", text="Destination", anchor=tk.CENTER)

tree.tag_configure("oddrow", background=odd_row_color)
tree.tag_configure("evenrow", background=even_row_color)

tree.bind("<ButtonRelease-1>", lambda event: copy_entries(event, tree))

frame_1_2 = tk.Frame(frame_1)
frame_1_2.grid(row=1, column=0, padx=padx, pady=pady)

id_label = tk.Label(frame_1_2, text="Id")
id_label.grid(row=1, column=0, padx=padx, pady=pady)
weight_label = tk.Label(frame_1_2, text="Weight")
weight_label.grid(row=1, column=1, padx=padx, pady=pady)
destination_label = tk.Label(frame_1_2, text="Destination")
destination_label.grid(row=1, column=2, padx=padx, pady=pady)
weather_label = tk.Label(frame_1_2, text="Weather")
weather_label.grid(row=1, column=3, padx=padx, pady=pady)

id_entry = tk.Entry(frame_1_2, width=3)
entries.append(id_entry)
id_entry.grid(row=2, column=0, padx=padx, pady=pady)
weight_entry = tk.Entry(frame_1_2, width=8)
entries.append(weight_entry)
weight_entry.grid(row=2, column=1, padx=padx, pady=pady)
destination_entry = tk.Entry(frame_1_2, width=15)
entries.append(destination_entry)
destination_entry.grid(row=2, column=2, padx=padx, pady=pady)
weather_entry = tk.Entry(frame_1_2, width=12)
entries.append(weather_entry)
weather_entry.grid(row=2, column=3, padx=padx, pady=pady)


frame_1_3 = tk.Frame(frame_1)
frame_1_3.grid(row=2, column=0, padx=padx, pady=pady)

create_button = tk.Button(frame_1_3, text="Create")
create_button.grid(row=0, column=0, padx=padx, pady=pady)
update_button = tk.Button(frame_1_3, text="Update")
update_button.grid(row=0, column=1, padx=padx, pady=pady)
delete_button = tk.Button(frame_1_3, text="Delete")
delete_button.grid(row=0, column=2, padx=padx, pady=pady)
clear_entry_boxes_button = tk.Button(frame_1_3, text="Clear Entry Boxes", command=empty_entries)
clear_entry_boxes_button.grid(row=0, column=3, padx=padx, pady=pady)

read_table(tree)

if __name__ == "__main__":
    main_window.mainloop()

