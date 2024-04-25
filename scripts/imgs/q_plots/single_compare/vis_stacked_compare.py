import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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

def plot_distributions(notes_dict, notes_df, q):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    colors = {'Q1': 'red','Q2': 'blue', 'Q3': 'yellow', 'Q4': 'green', 'Generated': 'slategrey'}

    # Flags to ensure labels are added only once
    label_added_actual = False
    label_added_generated = False

    for col_idx, variable in enumerate(['pitch', 'velocity', 'step', 'duration']):
        max_val = max([notes[variable].max() for notes in notes_dict.values()] + [notes_df[variable].max()])
        bins = np.linspace(0, max_val, 21)
        if variable == 'pitch':
            bins = np.linspace(0, 128, 21)
        elif variable == 'velocity':
            bins = np.linspace(0, 128, 21)
        elif variable == 'step':
            bins = np.linspace(0, 1, 8)
        elif variable == 'duration':
            bins = np.linspace(0, 8, 21)

        bin_width = np.diff(bins)[0] - 0.1

        # Collect the normalized counts for the actual Q4 data
        actual_counts, _ = np.histogram(notes_dict[q][variable], bins)
        actual_counts_normalized = actual_counts / actual_counts.sum()

        # Collect the normalized counts for the generated data
        generated_counts, _ = np.histogram(notes_df[variable], bins)
        generated_counts_normalized = generated_counts / generated_counts.sum()

        # Plot the bar with the larger count first for each bin
        for bin_edge, actual_count, generated_count in zip(bins[:-1], actual_counts_normalized, generated_counts_normalized):
            if actual_count > generated_count:
                if not label_added_actual:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, actual_count, width=bin_width, align='edge', color=colors[f'Q{q}'], label=f'Q{q} - Actual')
                    label_added_actual = True
                else:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, actual_count, width=bin_width, align='edge', color=colors[f'Q{q}'])
                
                if not label_added_generated:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, generated_count, width=bin_width, align='edge', color=colors['Generated'], label=f'Q{q} - Generated')
                    label_added_generated = True
                else:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, generated_count, width=bin_width, align='edge', color=colors['Generated'])
            else:
                if not label_added_generated:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, generated_count, width=bin_width, align='edge', color=colors['Generated'], label=f'Q{q} - Generated')
                    label_added_generated = True
                else:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, generated_count, width=bin_width, align='edge', color=colors['Generated'])

                if not label_added_actual:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, actual_count, width=bin_width, align='edge', color=colors[f'Q{q}'], label=f'Q{q} - Actual')
                    label_added_actual = True
                else:
                    axes[col_idx // 2, col_idx % 2].bar(bin_edge, actual_count, width=bin_width, align='edge', color=colors[f'Q{q}'])

        axes[col_idx // 2, col_idx % 2].set_xlabel(variable)
        axes[col_idx // 2, col_idx % 2].set_ylabel('Proportion')

    # Add the legend outside of the loop, and just once
    axes[0, 0].legend()

    plt.tight_layout()
    plt.savefig(f'Q{q}_compare.png')
    plt.show()


basedir = 'content'
notes_dict = {}

# Direct file paths
file_paths = {
    'Q1': 'Q1.mid',
    'Q2': 'Q2.mid',
    'Q3': 'Q3.mid',
    'Q4': 'Q4.mid'
}

for q in range (1,5):
    df = pd.read_csv(f'{basedir}/EMOPIA_2.2_normalized_metadata_by_song.csv')
    df = df[df['DominantQ'] == q]

    files = [f'Q{q}_{song}' for song in df['songID']]
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
    notes_dict[q] = df_notes


    df = midi_to_notes(f'Q{q}.mid')
    plot_distributions(notes_dict, df, q=q)
