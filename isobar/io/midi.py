try:
    import mido
except:
    print "mido not found, no MIDI support available."

import isobar

MIDIIN_DEFAULT = "IAC Driver A"
MIDIOUT_DEFAULT = "IAC Driver A"


class MidiIn:

    def __init__(self, target=MIDIOUT_DEFAULT):
        self.midi = None
        # don't ignore MIDI clock messages (is on by default)
        # TODO: check
        # self.midi.ignore_types(timing=False)
        self.clocktarget = None

        ports = mido.get_input_names()
        if len(ports) == 0:
            raise Exception("No MIDI output ports found")

        for name in ports:
            if name == target:
                isobar.log("Found MIDI input (%s)", name)
                self.midi = mido.open_input(name, callback=self.callback)

        if self.midi is None:
            isobar.log("Could not find MIDI source %s, using default", target)
            self.midi = mido.open_input(callback=self.callback)

    def callback(self, message):
        print message

        if message.type is "clock":
            if self.clocktarget is not None:
                self.clocktarget.tick()

        if message.type is "start":
            # TODO: is this the right midi code?
            if self.clocktarget is not None:
                self.clocktarget.reset_to_beat()

        # print "%d %d (%d)" % (data_type, data_note, data_vel)

    def run(self):
        self.midi.callback = self.callback

    def poll(self):
        """ used in markov-learner -- can we refactor? """
        message = self.midi.receive()
        if not message:
            return

        print message

        if (message.type & 0x90) > 0 and message.velocity > 0:
            # note on
            return isobar.Note(message.note, message.velocity)

    def close(self):
        del self.midi


class MidiOut:

    def __init__(self, target=MIDIOUT_DEFAULT):
        self.midi = None
        self.debug = False
        ports = mido.get_output_names()
        if len(ports) == 0:
            raise Exception("No MIDI output ports found")

        for name in ports:
            if name == target:
                isobar.log("Found MIDI output (%s)" % name)
                self.midi = mido.open_output(name)

        if self.midi is None:
            print "Could not find MIDI target %s, using default" % target
            self.midi = mido.open_output()

    def tick(self, ticklen):
        pass

    def noteOn(self, note=60, velocity=64, channel=0):
        if self.debug:
            print "[midi] channel %d, noteOn: (%d, %d)" % (
                channel, note, velocity
            )
        msg = mido.Message(
            'note_on', channel=channel, note=note, velocity=velocity
        )
        self.midi.send(msg)

    def noteOff(self, note=60, channel=0):
        if self.debug:
            print "[midi] channel %d, noteOff: %d" % (channel, note)
        msg = mido.Message(
            'note_off', channel=channel, note=note
        )
        self.midi.send(msg)

    def allNotesOff(self, channel=0):
        if self.debug:
            print "[midi] channel %d, allNotesOff"
        self.midi.panic()

    def control(self, control=0, value=0, channel=0):
        print "*** [CTRL] channel %d, control %d: %d" % (channel, control, value)
        if self.debug:
            print "[midi] channel %d, control %d: %d" % (channel, control, value)
        msg = mido.Message(
            'control_change', channel=channel, control=control, value=value
        )
        self.midi.send(msg)

    def __destroy__(self):
        del self.midi
