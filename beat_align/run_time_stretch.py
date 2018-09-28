import librosa as lr
import numpy as np
import soundfile as sf
import pyrubberband as prb
import argparse
import os

FILENAME1 = 'data/MDBDrums/MDB Drums/audio/drum_only/MusicDelta_80sRock_Drum.wav'
FILENAME2 = 'data/MDBDrums/MDB Drums/audio/drum_only/MusicDelta_Beatles_Drum.wav'

def _get_cmdline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename1", type=str,
                        help="Filename 1. Will yield target timeline")
    parser.add_argument("--filename2", type=str,
                        help="Filename 2. Will be time stretched to run "
                             "synchronously to file 1.")
    parser.add_argument("--filename_out", type=str, default='',
                        help="Output filename")

    return parser.parse_args()

def main():

    args = _get_cmdline_args()

    # Loading the wav files
    y1, sr = lr.load(args.filename1, sr=44100)
    y2, _  = lr.load(args.filename2, sr=44100)

    # Using librosa to extract tempo and beat positions from the loaded data
    tempo1_bpm, beat_pos1_sec = lr.beat.beat_track(y1, sr=sr, units='time')
    if tempo1_bpm == 0:
        print(f'Beat tracking failed for file {filename}')

    tempo2_bpm, beat_pos2_sec = lr.beat.beat_track(y2, sr=sr, units='time')
    if tempo2_bpm == 0:
        print(f'Beat tracking failed for file {filename}')

    # Append/loop copies of file2 to itself to get a similar amount of beats
    num_beats1 = beat_pos1_sec.size
    num_beats2 = beat_pos2_sec.size
    len2_sec = y2.size / sr
    y2_new = y2
    beat_pos2_sec_new = beat_pos2_sec
    for k in range(np.ceil(num_beats1 / num_beats2).astype(int)-1):
        y2_new = np.concatenate( (y2_new, y2) )
        beat_pos2_sec_new = np.concatenate( (beat_pos2_sec_new, beat_pos2_sec + (k+1) * len2_sec) )

    # Cut the (looped) file 2 to have the same number of beats
    if beat_pos2_sec_new.size > beat_pos1_sec.size:
        cut_pos_sec = beat_pos2_sec_new[beat_pos1_sec.size]
        y2_new = y2_new[:int(cut_pos_sec * sr)]
        beat_pos2_sec_new = beat_pos2_sec_new[:beat_pos1_sec.size]

    # Call rubberband (transpose signal due to different memory layout as used by librosa)
    time_map = [ (int(t0*sr), int(t1*sr)) for (t0, t1) in zip(beat_pos2_sec_new.tolist(),beat_pos1_sec.tolist()) ]
    time_map.append( (int(y2_new.size), int(y1.size)) )
    y2_new_stretched = prb.timemap_stretch(np.transpose(y2_new), sr, time_map)

    # Writing to file
    filename_out = args.filename_out
    if len(filename_out) == 0:
        filename_out = 'stretched_to_' + os.path.basename(args.filename1) + '_from_' + os.path.basename(args.filename2) + '_.wav'
    sf.write(filename_out, y2_new_stretched, sr)

if __name__ == '__main__':
    main()
