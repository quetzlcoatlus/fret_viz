import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define the chromatic scale with sharps and flats
chromatic_scale = [
    'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
]

# Enharmonic equivalents for flats
enharmonic_equivalents = {
    'Bb': 'A#',
    'Db': 'C#',
    'Eb': 'D#',
    'Gb': 'F#',
    'Ab': 'G#'
}

# Function to generate triad notes
def generate_triad(root, chord_type):
    # Handle flats by converting to their sharp equivalents
    root = enharmonic_equivalents.get(root, root)
    
    # Get the root index
    try:
        root_index = chromatic_scale.index(root)
    except ValueError:
        print(f"Error: Root note '{root}' is not valid.")
        return []
    
    # Define intervals in semitones for each chord type
    intervals = {
        'Major': [0, 4, 7],       # Root, Major Third, Perfect Fifth
        'Minor': [0, 3, 7],       # Root, Minor Third, Perfect Fifth
        'Diminished': [0, 3, 6],  # Root, Minor Third, Diminished Fifth
    }
    
    # Get the intervals for the specified chord type
    if chord_type not in intervals:
        print(f"Error: Chord type '{chord_type}' is not valid.")
        return []
    
    semitone_intervals = intervals[chord_type]
    
    # Generate the triad notes
    triad_notes = []
    for interval in semitone_intervals:
        note_index = (root_index + interval) % 12
        note = chromatic_scale[note_index]
        triad_notes.append(note)
    
    return triad_notes

# Function to get note positions on the fretboard
def get_note_positions(notes, num_frets=12):
    # Map of notes on the fretboard
    fretboard = {
        6: {},  # String 6 (Low E)
        5: {},  # String 5 (A)
        4: {},  # String 4 (D)
        3: {},  # String 3 (G)
        2: {},  # String 2 (B)
        1: {},  # String 1 (High E)
    }
    
    # Open string notes
    open_strings = {
        6: 'E',
        5: 'A',
        4: 'D',
        3: 'G',
        2: 'B',
        1: 'E',
    }
    
    # Build the fretboard map
    for string in fretboard:
        open_note = open_strings[string]
        try:
            note_index = chromatic_scale.index(open_note)
        except ValueError:
            open_note = enharmonic_equivalents.get(open_note, open_note)
            note_index = chromatic_scale.index(open_note)
        
        for fret in range(num_frets + 1):
            current_note_index = (note_index + fret) % 12
            current_note = chromatic_scale[current_note_index]
            fretboard[string][fret] = current_note
        
    # Get positions of the specified notes
    note_positions = []
    for string in fretboard:
        for fret in fretboard[string]:
            note = fretboard[string][fret]
            if note in notes:
                note_positions.append((fret, string, note))
        
    return note_positions

# Function to draw the fretboard diagram
def draw_fretboard(note_positions, root, chord_type, notes, num_frets=12):
    num_strings = 6
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, num_frets)
    ax.set_ylim(0, num_strings)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Draw frets
    for fret in range(num_frets + 1):
        ax.add_line(plt.Line2D([fret, fret], [0, num_strings], color='black'))
    
    # Draw strings
    for string in range(num_strings):
        ax.add_line(plt.Line2D([0, num_frets], [string + 0.5, string + 0.5], color='black', linewidth=2))
    
    # Add fret numbers
    for fret in range(1, num_frets + 1):
        ax.text(fret - 0.5, num_strings + 0.3, str(fret), ha='center', va='center', fontsize=10)
    
    # Draw note markers
    for fret, string, note in note_positions:
        # Adjust for zero fret (open string)
        x = fret if fret > 0 else 0.1
        y = num_strings - string + 0.5
        # Determine color (root note in a different color)
        if note == notes[0]:
            color = 'red'       # Root note in red
        else:
            color = 'blue'      # Other chord tones in blue
        # Draw circle
        circle = patches.Circle((x - 0.5, y), 0.3, color=color, zorder=5)
        ax.add_patch(circle)
        # Add note text
        ax.text(x - 0.5, y, note, ha='center', va='center', color='white', fontsize=9, zorder=6)
    
    # Add title
    plt.title(f"{root} {chord_type} Triad on Guitar Fretboard", fontsize=14)
    plt.show()

# Main function to generate the fretboard diagram for any triad
def generate_triad_fretboard(root, chord_type, num_frets=12):
    # Generate triad notes
    notes = generate_triad(root, chord_type)
    if not notes:
        return
    # Get note positions on the fretboard
    note_positions = get_note_positions(notes, num_frets)
    # Draw the fretboard diagram
    draw_fretboard(note_positions, root, chord_type, notes, num_frets)

# Example usage
if __name__ == "__main__":
    # User inputs
    root_note = 'A'         # e.g., 'A', 'C#', 'Bb'
    chord_type = 'Minor'    # 'Major', 'Minor', or 'Diminished'
    
    # Generate the fretboard diagram
    generate_triad_fretboard(root_note, chord_type)
