from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from fretboard_diagram import load_configurations, generate_fretboard_diagram, parse_tuning

import yaml

# Load configurations
patterns, chromatic_scale, enharmonic_equivalents, visual_settings = load_configurations()

main_window = Tk() # main window of the app
main_window.title("Fretboard Visualizer")
main_window.geometry("1025x725")

frame = ttk.Frame(main_window, padding=10)
frame.pack(side=TOP)

field_frame = ttk.Frame(frame, padding=10)
field_frame.grid() # grid widget holds the labels

plot_frame = ttk.Frame(main_window, padding=10)
plot_frame.pack(side=BOTTOM, fill=BOTH)

# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# can change any of the parameters for the fretboard_diagram.py script in the GUI
# - root == dropdown

root_note = StringVar()
root_note.set('C') # set default
root_options = chromatic_scale # dropdown options
root_dropdown = ttk.Combobox(field_frame, width=10, values=root_options, textvariable=root_note)
ttk.Label(field_frame, text="Root Note:").grid(column=0, row=0)
root_dropdown.grid(column=1, row=0)

# - pattern type (chord/scale) == dropdown

pattern_type = StringVar()
pattern_type.set('Chord')
pattern_type_options = [
    "Chord",
    "Scale",
]
pattern_type_dropdown = ttk.Combobox(field_frame, width=10, values=pattern_type_options, textvariable=pattern_type)
ttk.Label(field_frame, text="Pattern Type:").grid(column=0, row=1)
pattern_type_dropdown.grid(column=1, row=1)

# - pattern name (e.g. Major, Minor, etc.) == dropdown

pattern_name = StringVar()
pattern_name_entry = ttk.Combobox(field_frame, width=10, values=list(patterns['Chord'].keys()) + list(patterns['Scale'].keys()), textvariable=pattern_name)
ttk.Label(field_frame, text="Pattern Name:").grid(column=0, row=2)
pattern_name_entry.grid(column=1, row=2)

# - tuning == string input field

tuning = StringVar()
tuning.set('E,A,D,G,B,E')
tuning_entry = ttk.Entry(field_frame, width=10, textvariable=tuning)
ttk.Label(field_frame, text="Tuning:").grid(column=0, row=3)
tuning_entry.grid(column=1, row=3)

# - frets to display (default=12)

frets = IntVar()
frets.set(12)
fret_entry = ttk.Entry(field_frame, width=10, textvariable=frets)
ttk.Label(field_frame, text="Frets to display:").grid(column=0, row=4)
fret_entry.grid(column=1, row=4)


# generate button that makes a fretboard diagram and displays it on screen
# takes all the parameters it'd normally take in command line and calls the script
# puts the generated fretboard in plot_frame

def generate_gui_fretboard():
    # need to cast all the variables to string except for frets

    rn = root_note.get()
    pt = pattern_type.get()
    pn = pattern_name.get()
    t = parse_tuning(tuning.get())
    f = frets.get()

    figure = generate_fretboard_diagram(rn, pt, pn, t, f)
    # want to put the diagram on the screen

    # clear the plot frame
    # for widget in plot_frame.winfo_children():
    #     widget.destroy()

    for widget in plot_frame.winfo_children():
        widget.destroy()


    canvas = FigureCanvasTkAgg(figure, plot_frame)
    canvas.draw()
    plot_widget = canvas.get_tk_widget()

    # plot_frame.grid_columnconfigure(2, weight=1)
    # plot_frame.grid_rowconfigure(0, weight=1)

    plot_widget.grid(column=2, row=0, sticky='w')




generate_button = ttk.Button(field_frame, text="Generate Fretboard", command=generate_gui_fretboard)
generate_button.grid(column=0,row=5)

# generate the fretboard using the inputted data
# display it in the window

main_window.mainloop()