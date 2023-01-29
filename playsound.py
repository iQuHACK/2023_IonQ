from midiutil.MidiFile import MIDIFile
import pygame

bit_to_time = {
                '000': 4,
                '001': 3,
                '010': 2,
                '011': 1.5,
                '100': 1,
                '101': 0.75,
                '110': 0.5,
                '111': 0.25,
                }
note_to_midinum = {
                'C2': 48,
                'Db2': 49,
                'D2': 50,
                'Eb2': 51,
                'E2': 52,
                'F2': 53,
                'Gb2': 54,
                'G2': 55,
                'Ab2': 56,
                'A2': 57,
                'Bb2': 58,
                'B2': 59,
                'C3': 60,
                'Db3': 61,
                'D3': 62,
                'Eb3': 63,
                'E3': 64,
                'F3': 65,
                'Gb3': 66,
                'G3': 67,
                'Ab3': 68,
                'A3': 69,
                'Bb3': 70,
                'B3': 71,
                'C4': 72,
                'Db4': 73,
                'D4': 74,
                'Eb4': 75,
                'E4': 76,
                'F4': 77,
                'Gb4': 78,
                'G4': 79
                }

def get_pitch_and_duration(bits):
    '''Parse `bits` to output the pitch and duration of the note'''

    pitch = int(bits[3:], 2) + 48
    duration = bit_to_time[bits[0:3]]
    return pitch, duration

def play_music(midi_filename):
    '''Stream music_file in a blocking manner'''

    clock = pygame.time.Clock()
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(1) # check if playback has finished

def write_to_midi(bits_arr):
    '''Writes `bit_arr` into a MIDI file'''

    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, 'Sample Track')
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100
    time_count = 0
    for bits in bits_arr:
        pitch, duration = get_pitch_and_duration(bits)
        mf.addNote(track, channel, pitch, time_count, duration, volume)
        time_count += duration

    # write it to disk
    with open('output.mid', 'wb') as outf:
        mf.writeFile(outf)
        
    return 'output.mid'

def play_notes(midi_filename, vol = 1.0):
    '''Plays `midi_filename` at volume `vol` (between 0 and 1.0)'''

    # mixer config
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(vol)

    # listen for interruptions
    try:
        play_music(midi_filename)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit

if __name__ == "__main__":
    # Example: Bill Kill by SZA
    notes = ['Bb2', 'C3', 'Db3', 'Ab3', 'G3', 'G3', 'F3', 'Eb3', 'Bb2', 'C3']
    bits_arr = ['100' + bin(note_to_midinum[note] - 48).replace('0b','') for note in notes]
    play_notes(write_to_midi(bits_arr))