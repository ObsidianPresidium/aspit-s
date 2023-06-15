""" Opgave "GUI step 2":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2020.png

Genbrug din kode fra "GUI step 1".

GUI-strukturen bør være som følger:
    main window
        labelframe
            frame
                labels and entries
            frame
                buttons

Funktionalitet:
    Klik på knappen "clear entry boxes" sletter teksten i alle indtastningsfelter (entries).

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as tk

main_window = tk.Tk()
main_window.title("my first GUI")
main_window.geometry("493x179")
padx=8
pady=4
entries = []

def empty_entries():
    print("Empty entries button was pressed")
    for i in entries:
        i.delete(0, tk.END)

frame_1 = tk.LabelFrame(main_window, text="Container")
frame_1.grid(row=0, padx=padx, pady=pady)

frame_1.pack(fill="both", expand=True, padx=padx, pady=pady)

frame_1_1 = tk.Frame(frame_1)
frame_1_1.grid(row=0, column=0, padx=padx, pady=pady)

id_label = tk.Label(frame_1_1, text="Id")
id_label.grid(row=1, column=0, padx=padx, pady=pady)
weight_label = tk.Label(frame_1_1, text="Weight")
weight_label.grid(row=1, column=1, padx=padx, pady=pady)
destination_label = tk.Label(frame_1_1, text="Destination")
destination_label.grid(row=1, column=2, padx=padx, pady=pady)
weather_label = tk.Label(frame_1_1, text="Weather")
weather_label.grid(row=1, column=3, padx=padx, pady=pady)

id_entry = tk.Entry(frame_1_1, width=3)
entries.append(id_entry)
id_entry.grid(row=2, column=0, padx=padx, pady=pady)
weight_entry = tk.Entry(frame_1_1, width=8)
entries.append(weight_entry)
weight_entry.grid(row=2, column=1, padx=padx, pady=pady)
destination_entry = tk.Entry(frame_1_1, width=15)
entries.append(destination_entry)
destination_entry.grid(row=2, column=2, padx=padx, pady=pady)
weather_entry = tk.Entry(frame_1_1, width=12)
entries.append(weather_entry)
weather_entry.grid(row=2, column=3, padx=padx, pady=pady)


frame_1_2 = tk.Frame(frame_1)
frame_1_2.grid(row=1, column=0, padx=padx, pady=pady)

create_button = tk.Button(frame_1_2, text="Create")
create_button.grid(row=0, column=0, padx=padx, pady=pady)
update_button = tk.Button(frame_1_2, text="Update")
update_button.grid(row=0, column=1, padx=padx, pady=pady)
delete_button = tk.Button(frame_1_2, text="Delete")
delete_button.grid(row=0, column=2, padx=padx, pady=pady)
clear_entry_boxes_button = tk.Button(frame_1_2, text="Clear Entry Boxes", command=empty_entries)
clear_entry_boxes_button.grid(row=0, column=3, padx=padx, pady=pady)

if __name__ == "__main__":
    main_window.mainloop()