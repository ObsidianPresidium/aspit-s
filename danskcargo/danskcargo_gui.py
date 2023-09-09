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

controls_frame_container = tk.Frame(frame_container)
controls_frame_container.grid(row=1, column=0, padx=padx, pady=pady)

edit_frame_container = tk.Frame(controls_frame_container)
edit_frame_container.grid(row=0,column=0, padx=padx, pady=pady)
label_container_id = tk.Label(edit_frame_container, text="ID")
label_container_id.grid(row=0, column=0, padx=padx, pady=pady)
label_container_weight = tk.Label(edit_frame_container, text="Weight")
label_container_weight.grid(row=0, column=1, padx=padx, pady=pady)
label_container_destination = tk.Label(edit_frame_container, text="Destination")
label_container_destination.grid(row=0, column=2, padx=padx, pady=pady)
label_container_weather = tk.Label(edit_frame_container, text="Weather")
label_container_weather.grid(row=0, column=3, padx=padx, pady=pady)
entry_container_id = tk.Entry(edit_frame_container, width=4)
entry_container_id.grid(row=1, column=0, padx=padx, pady=pady)
entry_container_weight = tk.Entry(edit_frame_container, width=4)
entry_container_weight.grid(row=1, column=1, padx=padx, pady=pady)
entry_container_destination = tk.Entry(edit_frame_container, width=8)
entry_container_destination.grid(row=1, column=2, padx=padx, pady=pady)
entry_container_weather = tk.Entry(edit_frame_container, width=6)
entry_container_weather.grid(row=1, column=3, padx=padx, pady=pady)


frame_aircraft = tk.LabelFrame(main_window, text="Aircraft")
frame_aircraft.grid(row=0, column=1, padx=padx, pady=pady)

tree_frame_aircraft = tk.Frame(frame_aircraft)
tree_frame_aircraft.grid(row=0, column=0, padx=padx, pady=pady)

tree_scroll_aircraft = tk.Scrollbar(tree_frame_aircraft)
tree_scroll_aircraft.grid(row=0, column=1, padx=padx, pady=pady, sticky="ns")
tree_aircraft = ttk.Treeview(tree_frame_aircraft, yscrollcommand=tree_scroll_aircraft.set, selectmode="browse")
tree_aircraft.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_aircraft.config(command=tree_aircraft.yview)

controls_frame_aircraft = tk.Frame(frame_aircraft)
controls_frame_aircraft.grid(row=1, column=0, padx=padx, pady=pady)

edit_frame_aircraft = tk.Frame(controls_frame_aircraft)
edit_frame_aircraft.grid(row=0,column=0, padx=padx, pady=pady)
label_aircraft_id = tk.Label(edit_frame_aircraft, text="ID")
label_aircraft_id.grid(row=0, column=0, padx=padx, pady=pady)
label_aircraft_maxweight = tk.Label(edit_frame_aircraft, text="Max.Carg.Wgt.")
label_aircraft_maxweight.grid(row=0, column=1, padx=padx, pady=pady)
label_aircraft_registration = tk.Label(edit_frame_aircraft, text="Registration")
label_aircraft_registration.grid(row=0, column=2, padx=padx, pady=pady)
entry_aircraft_id = tk.Entry(edit_frame_aircraft, width=4)
entry_aircraft_id.grid(row=1, column=0, padx=padx, pady=pady)
entry_aircraft_maxweight = tk.Entry(edit_frame_aircraft, width=4)
entry_aircraft_maxweight.grid(row=1, column=1, padx=padx, pady=pady)
entry_aircraft_registration = tk.Entry(edit_frame_aircraft, width=8)
entry_aircraft_registration.grid(row=1, column=2, padx=padx, pady=pady)


frame_transport = tk.LabelFrame(main_window, text="Transport")
frame_transport.grid(row=0, column=2, padx=padx, pady=pady)

tree_frame_transport = tk.Frame(frame_transport)
tree_frame_transport.grid(row=0, column=0, padx=padx, pady=pady)

tree_scroll_transport = tk.Scrollbar(tree_frame_transport)
tree_scroll_transport.grid(row=0, column=1, padx=padx, pady=pady, sticky="ns")
tree_transport = ttk.Treeview(tree_frame_transport, yscrollcommand=tree_scroll_transport.set, selectmode="browse")
tree_transport.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_transport.config(command=tree_transport.yview)

controls_frame_transport = tk.Frame(frame_transport)
controls_frame_transport.grid(row=1, column=0, padx=padx, pady=pady)

edit_frame_transport = tk.Frame(controls_frame_transport)
edit_frame_transport.grid(row=0,column=0, padx=padx, pady=pady)
label_transport_id = tk.Label(edit_frame_transport, text="ID")
label_transport_id.grid(row=0, column=0, padx=padx, pady=pady)
label_transport_date = tk.Label(edit_frame_transport, text="Date")
label_transport_date.grid(row=0, column=1, padx=padx, pady=pady)
label_transport_containerid = tk.Label(edit_frame_transport, text="Container ID")
label_transport_containerid.grid(row=0, column=2, padx=padx, pady=pady)
label_transport_aircraftid = tk.Label(edit_frame_transport, text="Aircraft ID")
label_transport_aircraftid.grid(row=0, column=3, padx=padx, pady=pady)
entry_transport_id = tk.Entry(edit_frame_transport, width=4)
entry_transport_id.grid(row=1, column=0, padx=padx, pady=pady)
entry_transport_date = tk.Entry(edit_frame_transport, width=4)
entry_transport_date.grid(row=1, column=1, padx=padx, pady=pady)
entry_transport_containerid = tk.Entry(edit_frame_transport, width=8)
entry_transport_containerid.grid(row=1, column=2, padx=padx, pady=pady)
entry_transport_aircraftid = tk.Entry(edit_frame_transport, width=4)
entry_transport_aircraftid.grid(row=1, column=3, padx=padx, pady=pady)

if __name__ == "__main__":
    main_window.mainloop()