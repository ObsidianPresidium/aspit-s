"""
Opgave "GUI step 1":

Som altid skal du læse hele øpgavebeskrivelsen omhyggeligt, før du begynder at løse opgaven.

Kopier denne fil til din egen løsningsmappe. Skriv din løsning ind i kopien.

Bruge det, du har lært i GUI-eksempelfilerne, og byg den GUI, der er afbildet i images/gui_2010.png

Når dit program er færdigt, skal du skubbe det til dit github-repository.
Send derefter denne Teams-meddelelse til din lærer: <filename> færdig
Fortsæt derefter med den næste fil."""

import tkinter as tk

main_window = tk.Tk()
main_window.title("my first GUI")
main_window.geometry("125x200")
padx=8
pady=4

frame_1 = tk.LabelFrame(main_window, text="Container")
frame_1.grid(row=0, padx=padx, pady=pady)

frame_1.pack(fill="both", expand=True, padx=padx, pady=pady)

id_label = tk.Label(frame_1, text="Id")
id_label.grid(row=1)
frame_1.rowconfigure(1, weight=1)
frame_1.columnconfigure(0, weight=1)

my_entry = tk.Entry(frame_1, width=3)
my_entry.grid(row=2)
frame_1.rowconfigure(2, weight=1)
# frame_1.columnconfigure(2, weight=1)

my_button = tk.Button(frame_1, text="Create")
my_button.grid(row=3)
frame_1.rowconfigure(3, weight=1)
# frame_1.columnconfigure(3, weight=1)

if __name__ == "__main__":
    main_window.mainloop()