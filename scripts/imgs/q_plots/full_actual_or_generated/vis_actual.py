import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pretty_midi
import collections
import os

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

def plot_distributions(notes_dict, drop_percentile=2.5):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    colors = {'Q1': 'red', 'Q2': 'blue', 'Q3': 'yellow', 'Q4': 'green'}

    for col_idx, variable in enumerate(['pitch', 'velocity', 'step', 'duration']):
        # Get the maximum value across all Qs for the current variable
        max_val = max(np.percentile(notes_dict[q][variable], 100 - drop_percentile) for q in notes_dict)
        bins = np.linspace(0, max_val, 21)
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        # Normalize the counts for each Q
        normalized_Q_counts = {}
        for Q, notes in notes_dict.items():
            counts, _ = np.histogram(notes[variable], bins)
            normalized_Q_counts[Q] = counts / counts.sum()  # Normalize counts here

        # Sort the Q's by normalized count at each bin
        sorted_counts = np.array([[normalized_Q_counts[Q][b] for Q in sorted(normalized_Q_counts, key=lambda q: -normalized_Q_counts[q][b])] for b in range(len(bins)-1)])

        # Calculate the width of each bin
        bin_width = np.diff(bins)[0] - 0.1

        for b in range(len(bin_centers)):
            bottoms = 0
            for normalized_count, Q in zip(sorted_counts[b], sorted(normalized_Q_counts, key=lambda q: -normalized_Q_counts[q][b])):
                axes[col_idx // 2, col_idx % 2].bar(bin_centers[b], normalized_count, width=bin_width, bottom=bottoms, color=colors[f'Q{Q}'], label=f'Q{Q}' if b == 0 else "", alpha=1)
                bottoms += normalized_count

        axes[col_idx // 2, col_idx % 2].set_xlabel(variable)
        axes[col_idx // 2, col_idx % 2].legend()

    plt.tight_layout()
    plt.savefig('actual_normalized.png')   
    plt.show()


basedir = 'content'
notes_dict = {}

for Q in range(1, 5):
    df = pd.read_csv(f'{basedir}/EMOPIA_2.2_normalized_metadata_by_song.csv')
    df = df[df['DominantQ'] == Q]

    files = [f'Q{Q}_{song}' for song in df['songID']]
    notes_list = []

    for file in files:
        for i in range(10):
            file_variant = f'{file}_{i}.mid'
            file_path = os.path.join(f'{basedir}/midis/', file_variant)
            if os.path.exists(file_path):
                notes = midi_to_notes(file_path)
                notes_list.append(notes)
            else:
                break

    df_notes = pd.concat(notes_list, ignore_index=True)
    notes_dict[Q] = df_notes

plot_distributions(notes_dict)
