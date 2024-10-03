import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

# Define the chromatic scale with sharps and flats
chromatic_scale = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

# Enharmonic equivalents for flats
enharmonic_equivalents = {
    'Cb': 'B',
    'Db': 'C#',
    'Eb': 'D#',
    'Fb': 'E',
    'Gb': 'F#',
    'Ab': 'G#',
    'Bb': 'A#',
    'E#': 'F',
    'B#': 'C'
}

# Available patterns
patterns = {
    'Chord': {
        'Major': [0, 4, 7],
        'Minor': [0, 3, 7],
        'Diminished': [0, 3, 6],
        'Augmented': [0, 4, 8],
        'Dominant 7th': [0, 4, 7, 10],
        'Major 7th': [0, 4, 7, 11],
        'Minor 7th': [0, 3, 7, 10],
        'Half-Diminished 7th': [0, 3, 6, 10],
        'Diminished 7th': [0, 3, 6, 9],
        'Suspended 2nd': [0, 2, 7],
        'Suspended 4th': [0, 5, 7],
    },
    'Scale': {
        'Major': [0, 2, 4, 5, 7, 9, 11],
        'Natural Minor': [0, 2, 3, 5, 7, 8, 10],
        'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
        'Melodic Minor': [0, 2, 3, 5, 7, 9, 11],
        'Pentatonic Major': [0, 2, 4, 7, 9],
        'Pentatonic Minor': [0, 3, 5, 7, 10],
        'Blues': [0, 3, 5, 6, 7, 10],
        # Add more scales as needed
    }
}

# Function to generate chords or scales
def generate_notes(root, pattern_type, pattern_name):
    # Handle flats by converting to their sharp equivalents
    root = enharmonic_equivalents.get(root, root)

    # Get the root index
    try:
        root_index = chromatic_scale.index(root)
    except ValueError:
        print(f"Error: Root note '{root}' is not valid.")
        return []

    # Get the intervals for the specified pattern
    if pattern_type not in patterns or pattern_name not in patterns[pattern_type]:
        print(f"Error: {pattern_type} '{pattern_name}' is not valid.")
        return []

    semitone_intervals = patterns[pattern_type][pattern_name]

    # Generate the notes
    notes = []
    for interval in semitone_intervals:
        note_index = (root_index + interval) % 12
        note = chromatic_scale[note_index]
        notes.append(note)

    return notes

# Function to get note positions on the fretboard
def get_note_positions(notes, tuning, num_frets=12):
    # Map of notes on the fretboard
    fretboard = {}
    num_strings = len(tuning)

    # Build the fretboard map
    for string_idx in range(num_strings):
        fretboard[string_idx] = {}
        open_note = tuning[string_idx]
        open_note = enharmonic_equivalents.get(open_note, open_note)
        try:
            note_index = chromatic_scale.index(open_note)
        except ValueError:
            print(f"Error: Tuning note '{open_note}' is not valid.")
            return []

        for fret in range(num_frets + 1):
            current_note_index = (note_index + fret) % 12
            current_note = chromatic_scale[current_note_index]
            fretboard[string_idx][fret] = current_note

    # Get positions of the specified notes
    note_positions = []
    for string_idx in fretboard:
        for fret in fretboard[string_idx]:
            note = fretboard[string_idx][fret]
            if note in notes:
                note_positions.append((fret, string_idx, note))

    return note_positions



def draw_fretboard(note_positions, root, pattern_type, pattern_name, notes, tuning, num_frets=12):
    num_strings = len(tuning)

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(num_frets, num_strings))

    # Set the background color of the figure (surrounding area)
    fig.patch.set_facecolor('darkgrey')  # Set the figure background to dark grey

    # Set the background color of the axes (fretboard area)
    fretboard_color = '#deb887'  # A wood-like color (BurlyWood)
    ax.set_facecolor(fretboard_color)

    # Adjust xlim to include space for tuning labels
    ax.set_xlim(-1, num_frets)
    ax.set_ylim(0, num_strings)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw frets
    for fret in range(num_frets + 1):
        ax.add_line(plt.Line2D([fret, fret], [0, num_strings], color='black', linewidth=1))
        if fret > 0:
            # Adjusted y-position to prevent overlapping with the title
            ax.text(fret - 0.5, num_strings + 0.1, str(fret), ha='center', va='center', fontsize=10, color='white')

    # Draw fret markers
    fret_markers = [3, 5, 7, 9, 12, 15, 17, 19, 21]
    for marker in fret_markers:
        if marker <= num_frets:
            x = marker - 0.5
            y = num_strings / 2
            if marker == 12:
                # Double dot at 12th fret
                ax.add_patch(patches.Circle((x, y - 0.2), 0.1, color='white', zorder=4))
                ax.add_patch(patches.Circle((x, y + 0.2), 0.1, color='white', zorder=4))
            else:
                ax.add_patch(patches.Circle((x, y), 0.1, color='white', zorder=4))

    # Draw strings with varying thickness
    string_widths = [2.5, 2, 1.5, 1, 0.8, 0.6]
    for idx in range(num_strings):
        y = idx + 0.5
        line_width = string_widths[idx % len(string_widths)]
        ax.add_line(plt.Line2D([0, num_frets], [y, y], color='black', linewidth=line_width))
        # Add tuning labels (strings from bottom to top)
        open_note = tuning[idx]
        # Adjusted x-position to prevent duplication and overlap
        ax.text(-0.6, y, open_note, ha='right', va='center', fontsize=12, color='white')

    # Draw note markers
    for fret, string_idx, note in note_positions:
        # Adjust for zero fret (open string)
        x = fret if fret > 0 else -0.1
        y = string_idx + 0.5
        # Determine color based on the note's interval
        if note == notes[0]:
            color = 'red'       # Root note
        elif len(notes) >= 2 and note == notes[1]:
            color = 'orange'    # Second or minor third
        elif len(notes) >= 3 and note == notes[2]:
            color = 'blue'      # Third or perfect fifth
        elif len(notes) >= 4 and note == notes[3]:
            color = 'green'     # Fourth note (e.g., seventh)
        else:
            color = 'gray'      # Other notes
        # Draw circle
        circle = patches.Circle((x - 0.5, y), 0.3, color=color, zorder=5)
        ax.add_patch(circle)
        # Increase font size for note labels
        ax.text(x - 0.5, y, note, ha='center', va='center', color='white', fontsize=12, zorder=6)

    # Add nut
    ax.add_line(plt.Line2D([0, 0], [0, num_strings], color='black', linewidth=3))

    # Adjust title position with padding
    plt.title(f"{root} {pattern_name} {pattern_type} on Guitar Fretboard", fontsize=14, color='white', pad=20)

    # Adjust figure to prevent clipping of title
    fig.subplots_adjust(top=0.9)

    # Save the plot to a file without overriding the axes facecolor
    filename = f"{root}_{pattern_name}_{pattern_type}_fretboard.png".replace(' ', '_')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
    print(f"Diagram saved as '{filename}'")


# Main function to generate the fretboard diagram
def generate_fretboard_diagram(root, pattern_type, pattern_name, tuning, num_frets=12):
    # Generate notes
    notes = generate_notes(root, pattern_type, pattern_name)
    if not notes:
        return
    # Get note positions on the fretboard
    note_positions = get_note_positions(notes, tuning, num_frets)
    if not note_positions:
        return
    # Draw the fretboard diagram
    draw_fretboard(note_positions, root, pattern_type, pattern_name, notes, tuning, num_frets)

# Helper function to parse tuning from string
def parse_tuning(tuning_str):
    tuning = tuning_str.split(',')
    tuning = [note.strip() for note in tuning]
    return tuning

# Function to handle practice mode
def practice_mode(tuning, num_frets, randomize_params):
    # Lists of possible root notes and patterns
    root_notes = chromatic_scale.copy()
    pattern_types = ['Chord', 'Scale']
    pattern_names = {
        'Chord': list(patterns['Chord'].keys()),
        'Scale': list(patterns['Scale'].keys())
    }

    while True:
        # Randomize parameters based on user selection
        if 'root' in randomize_params:
            root = random.choice(root_notes)
        else:
            root = input("Enter root note (e.g., C, F#, Bb): ").strip()
        if 'pattern_type' in randomize_params:
            pattern_type = random.choice(pattern_types)
        else:
            pattern_type = input("Enter pattern type ('Chord' or 'Scale'): ").strip()
        if 'pattern_name' in randomize_params:
            pattern_name = random.choice(pattern_names[pattern_type])
        else:
            pattern_name = input(f"Enter {pattern_type} name (e.g., 'Major', 'Minor 7th'): ").strip()

        print(f"\nGenerating diagram for {root} {pattern_name} {pattern_type}...\n")
        generate_fretboard_diagram(root, pattern_type, pattern_name, tuning, num_frets)

        # Ask if the user wants to continue
        continue_practice = input("Generate another diagram? (y/n): ").strip().lower()
        if continue_practice != 'y':
            break

# Entry point of the script
if __name__ == "__main__":
    # Default settings
    default_tuning = ['E', 'A', 'D', 'G', 'B', 'E']  # Standard 6-string guitar tuning
    num_frets = 12
    randomize_params = []

    # Check command-line arguments
    if '--practice' in sys.argv:
        # Practice mode activated
        tuning_input = input("Enter tuning (comma-separated), or press Enter for standard tuning: ").strip()
        tuning = parse_tuning(tuning_input) if tuning_input else default_tuning
        num_frets_input = input("Enter number of frets to display (default is 12): ").strip()
        num_frets = int(num_frets_input) if num_frets_input else num_frets

        # Ask user which parameters to randomize
        print("\nWhich parameters would you like to randomize?")
        print("Enter 'y' for yes, 'n' for no.")
        randomize_root = input("Randomize root note? (y/n): ").strip().lower() == 'y'
        randomize_pattern_type = input("Randomize pattern type? (y/n): ").strip().lower() == 'y'
        randomize_pattern_name = input("Randomize pattern name? (y/n): ").strip().lower() == 'y'

        if randomize_root:
            randomize_params.append('root')
        if randomize_pattern_type:
            randomize_params.append('pattern_type')
        if randomize_pattern_name:
            randomize_params.append('pattern_name')

        # Start practice mode
        practice_mode(tuning, num_frets, randomize_params)

    else:
        # Normal mode
        if len(sys.argv) >= 4:
            root_note = sys.argv[1]
            pattern_type = sys.argv[2]  # 'Chord' or 'Scale'
            pattern_name = sys.argv[3]
            if len(sys.argv) >= 5:
                tuning = parse_tuning(sys.argv[4])
            else:
                tuning = default_tuning
            if len(sys.argv) >= 6:
                num_frets = int(sys.argv[5])
        else:
            # Prompt user for input
            root_note = input("Enter root note (e.g., C, F#, Bb): ").strip()
            pattern_type = input("Enter pattern type ('Chord' or 'Scale'): ").strip()
            pattern_name = input("Enter pattern name (e.g., 'Major', 'Minor 7th', 'Pentatonic Minor'): ").strip()
            tuning_input = input("Enter tuning (comma-separated), or press Enter for standard tuning: ").strip()
            tuning = parse_tuning(tuning_input) if tuning_input else default_tuning
            num_frets_input = input("Enter number of frets to display (default is 12): ").strip()
            num_frets = int(num_frets_input) if num_frets_input else num_frets

        # Generate the fretboard diagram
        generate_fretboard_diagram(root_note, pattern_type, pattern_name, tuning, num_frets)
