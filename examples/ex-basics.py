#!/usr/bin/python
import isobar as iso

# create a repeating sequence with scalar transposition:
# [ 36, 38, 43, 39, ... ]
a = iso.PSeq([0, 2, 7, 3]) + 36

# apply pattern-wise transposition
# [ 36, 50, 43, 51, ... ]
a = a + iso.PSeq([0, 12])

# create a geometric chromatic series, repeated back and forth
b = iso.PSeries(0, 1, 12) + 72
b = iso.PPingPong(b)
b = iso.PLoop(b)

# create an velocity series, with emphasis every 4th note,
# plus a random walk to create gradual dynamic changes
amp = iso.PSeq([50, 35, 25, 35]) + iso.PBrown(0, 1, -20, 20)

# a Timeline schedules events at a given BPM.
# by default, send these over the first MIDI output.
output_device = iso.io.midi.MidiOut("IAC Driver IAC Bus 1")
timeline = iso.Timeline(120, device=output_device, debug=True)

# assign each of our Patterns to particular properties
timeline.sched({'note': a, 'dur': 1, 'gate': 2})

timeline.run()
