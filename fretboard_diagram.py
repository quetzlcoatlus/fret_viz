import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import yaml  # Import PyYAML to read YAML files

# Function to load configurations from YAML files
def load_configurations():
    # Load patterns from patterns.yaml
    with open('patterns.yaml', 'r') as file:
        patterns = yaml.safe_load(file)
    
    # Load notes from notes.yaml
    with open('notes.yaml', 'r') as file:
        notes_config = yaml.safe_load(file)
        chromatic_scale = notes_config['chromatic_scale']
        enharmonic_equivalents = notes_config['enharmonic_equivalents']
    
    # Load visual settings from settings.yaml
    with open('settings.yaml', 'r') as file:
        visual_settings = yaml.safe_load(file)
    
    return patterns, chromatic_scale, enharmonic_equivalents, visual_settings

# Load configurations
patterns, chromatic_scale, enharmonic_equivalents, visual_settings = load_configurations()

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

# Function to draw the fretboard diagram
def draw_fretboard(note_positions, root, pattern_type, pattern_name, notes, tuning, num_frets=12):
    num_strings = len(tuning)
    
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(num_frets, num_strings))
    
    # Remove the figure background color to make it transparent
    # Or set to a desired color if preferred
    # fig.patch.set_facecolor('darkgrey')  # This line is optional or can be commented out
    
    # Adjust xlim and ylim to include space for tuning labels and title
    ax.set_xlim(-1, num_frets)
    ax.set_ylim(0, num_strings)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Load visual settings
    colors = visual_settings['colors']
    fonts = visual_settings['fonts']
    string_widths = visual_settings['string_widths']
    
    # If using a texture image
    if 'texture_image' in visual_settings and visual_settings['texture_image']:
        import matplotlib.image as mpimg
        texture_image = mpimg.imread(visual_settings['texture_image'])
        ax.imshow(texture_image, extent=[-1, num_frets, 0, num_strings], aspect='auto', zorder=0)
    else:
        # Set fretboard background color
        ax.set_facecolor(colors['fretboard_background'])
    
    # Draw frets
    for fret in range(num_frets + 1):
        ax.add_line(plt.Line2D([fret, fret], [0, num_strings], color=colors['fret_lines'], linewidth=1, zorder=1))
        if fret > 0:
            ax.text(fret - 0.5, num_strings + 0.1, str(fret), ha='center', va='center',
                    fontsize=fonts['fret_number_size'], color=colors['text_color'], zorder=2)
    
    # Draw fret markers
    fret_markers = visual_settings.get('fret_markers', [3, 5, 7, 9, 12, 15, 17, 19, 21])
    for marker in fret_markers:
        if marker <= num_frets:
            x = marker - 0.5
            y = num_strings / 2
            if marker == 12:
                # Double dot at 12th fret
                ax.add_patch(patches.Circle((x, y - 0.2), 0.1, color=colors['fret_marker'], zorder=3))
                ax.add_patch(patches.Circle((x, y + 0.2), 0.1, color=colors['fret_marker'], zorder=3))
            else:
                ax.add_patch(patches.Circle((x, y), 0.1, color=colors['fret_marker'], zorder=3))
    
    # Draw strings with varying thickness
    for idx in range(num_strings):
        y = idx + 0.5
        line_width = string_widths[idx % len(string_widths)]
        ax.add_line(plt.Line2D([0, num_frets], [y, y], color=colors['string_lines'], linewidth=line_width, zorder=4))
        # Add tuning labels
        open_note = tuning[idx]
        ax.text(-0.6, y, open_note, ha='right', va='center', fontsize=fonts['tuning_label_size'],
                color=colors['text_color'], zorder=5)
    
    # Note color mapping
    note_color_map = {}
    intervals = ['root', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh']
    for i, note in enumerate(notes):
        interval_name = intervals[i] if i < len(intervals) else 'others'
        note_color = colors['note_colors'].get(interval_name, colors['note_colors']['others'])
        note_color_map[note] = note_color
    
    # Draw note markers
    for fret, string_idx, note in note_positions:
        # Adjust for zero fret (open string)
        x = fret if fret > 0 else -0.1
        y = string_idx + 0.5
        # Determine color based on the note
        color = note_color_map.get(note, colors['note_colors']['others'])
        # Draw circle
        circle = patches.Circle((x - 0.5, y), 0.3, color=color, zorder=6)
        ax.add_patch(circle)
        # Increase font size for note labels
        ax.text(x - 0.5, y, note, ha='center', va='center', color=colors['note_label_text_color'],
                fontsize=fonts['note_label_size'], zorder=7)
    
    # Add nut
    ax.add_line(plt.Line2D([0, 0], [0, num_strings], color=colors['nut_color'], linewidth=3, zorder=4))
    
    # Adjust title position with padding
    plt.title(f"{root} {pattern_name} {pattern_type} on Guitar Fretboard",
              fontsize=fonts['title_size'], color=colors['title_color'], pad=20)
    
    # Adjust figure to prevent clipping of title
    fig.subplots_adjust(top=0.9)
    
    # Save the plot to a file with transparent background
    filename = f"{root}_{pattern_name}_{pattern_type}_fretboard.png".replace(' ', '_')
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='none', edgecolor='none')
    plt.close(fig)  # Close the figure to free memory
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
    import random
    
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
