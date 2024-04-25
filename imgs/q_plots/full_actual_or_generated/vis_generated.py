import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pretty_midi
import collections

def midi_to_notes(midi_file: str) -> pd.DataFrame:
    pm = pretty_midi.PrettyMIDI(midi_file)
    instrument = pm.instruments[0]
    notes = collections.defaultdict(list)
    sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
    prev_start = sorted_notes[0].start

    for note in sorted_notes:
        start = note.start
        end = note.end
        notes['pitch'].append(note.pitch)
        notes['velocity'].append(note.velocity)
        notes['start'].append(start)
        notes['end'].append(end)
        notes['step'].append(start - prev_start)
        notes['duration'].append(end - start)
        prev_start = start

    return pd.DataFrame({name: np.array(value) for name, value in notes.items()})

def plot_distributions(notes_dict):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    colors = ['red', 'blue', 'yellow', 'green']
    labels = ['Q1 - Generated', 'Q2 - Generated', 'Q3 - Generated', 'Q4 - Generated']
    variables = ['pitch', 'velocity', 'step', 'duration']

    for col_idx, variable in enumerate(variables):
        max_val = max(notes[variable].max() for notes in notes_dict.values())
        bins = np.linspace(0, max_val, 21)
        
        if variable == 'pitch' or variable == 'velocity':
            bins = np.linspace(0, 128, 21)
        elif variable == 'step':
            bins = np.linspace(0, 1, 8)
        elif variable == 'duration':
            bins = np.linspace(0, 8, 21)

        bin_width = np.diff(bins)[0] - 0.1
        all_data = []

        # Collect data for each quarter and normalize
        for i, (label, notes) in enumerate(notes_dict.items()):
            counts, _ = np.histogram(notes[variable], bins)
            normalized_counts = counts / counts.sum()  # Normalization step
            all_data.append((labels[i], normalized_counts))

        # Sort bars within each bin
        for i, edge in enumerate(bins[:-1]):
            bars_at_i = [(label, normalized_counts[i]) for label, normalized_counts in all_data]
            bars_at_i.sort(key=lambda x: x[1], reverse=True)  # Sort by height descending

            # Plot each bar at this bin
            for j, (label, count) in enumerate(bars_at_i):
                axes[col_idx // 2, col_idx % 2].bar(edge, count, width=bin_width, align='edge', color=colors[j], label=label if i == 0 else "")

        axes[col_idx // 2, col_idx % 2].set_xlabel(variable)
        axes[col_idx // 2, col_idx % 2].set_ylabel('Proportion')
    
    # Add the legend outside the loop to avoid duplication
    handles, labels = axes[0, 0].get_legend_handles_labels()
    unique_labels = {label: handle for label, handle in zip(labels, handles) if label.endswith('Generated')}
    axes[0, 0].legend(unique_labels.values(), unique_labels.keys(), loc='best')

    plt.tight_layout()
    plt.savefig('generated_comparison_normalized.png')
    plt.show()

# Direct file paths
file_paths = {
    'Q1': 'Q1.mid',
    'Q2': 'Q2.mid',
    'Q3': 'Q3.mid',
    'Q4': 'Q4.mid'
}

notes_dict = {Q: midi_to_notes(file) for Q, file in file_paths.items()}

plot_distributions(notes_dict)
