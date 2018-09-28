import librosa as lr
import glob
import os
import json

# DATA_DIR = 'data/MDBDrums/MDB Drums/audio/drum_only/'
# RESULTS_FILENAME = 'results_drum_only.json'

DATA_DIR = 'data/MDBDrums/MDB Drums/audio/full_mix/'
RESULTS_FILENAME = 'results_full_mix.json'

def main():
    filename_list = glob.glob(os.path.join(DATA_DIR,'*.wav'))

    results = list()
    for filename in filename_list:
        print('Working on file: ' + filename)

        # Loading the wav file into a numpy array
        y, sr = lr.load(filename)

        # Using librosa to extract tempo and beat positions from the loaded data
        tempo_bpm, beat_pos_sec = lr.beat.beat_track(y, sr=sr, units='time')

        if tempo_bpm == 0:
            #TODO: this should be more elaborate
            print(f'Beat tracking failed for file {filename}')

        results.append([os.path.basename(filename), tempo_bpm, beat_pos_sec.tolist()])

    with open(RESULTS_FILENAME, "w") as file_handle:
        json.dump(results, file_handle, indent=2, sort_keys=True,)

if __name__ == '__main__':
    main()
