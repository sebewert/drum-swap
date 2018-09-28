from medleydb import mix


def remix_drums(mtrack, new_drum, output_path):
    drum_stems = []
    other_stems = []

    # not perfect - doesn't handle more than one drum stems case
    for s in mtrack.stems.values():
        if 'drum set' in s.instrument:
            drum_stems.append(s)
        else:
            other_stems.append(s.stem_idx)

    mix.mix_multitrack(
        mtrack,
        output_path,
        stem_indices=other_stems,
        additional_files=[(new_drum, drum_stems[0].mixing_coefficient)]
    )
