import os.path
import argparse
import pyaudio
import sys
import time
from socketIO_client import SocketIO, LoggingNamespace

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from Audio.StreamToFrequency import StreamToFrequency
from Audio.Store import Store


class Generator:
    def __init__(self, args=None):

        self.arguments = args
        self.subdivision = 0.03
        self.isZero = True
        self.counter = 1
        self.past_pred = 0
        self.show_prediction = args.display_prediction
        self.new_note = False
        self.write_csv = args.write_csv
        self.socket = SocketIO('127.0.0.1', 8000, LoggingNamespace)
        self.volume_array = []
        self.past_predicted_values = {
            "note": 0,
            "volume": 0,
            "length": 0,
        }

        self.store = Store()
        self.detector = StreamToFrequency(store=self.store, show_volume=args.display_volume)

        self.play = args.play

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=44100,
                                  frames_per_buffer=2048,
                                  input=True,
                                  output=False,
                                  stream_callback=self.detector.callback)

    def send_to_socket(self, freq, vol):
            self.socket.emit('freq_change', {'freq': freq, 'vol': vol})

    def generate(self):
        while True:
            pred = self.store.values

            if self.store.note == self.past_pred:
                self.store.inc_length()
                self.new_note = False
            else:
                self.new_note = True
                self.store.reset()

            self.past_pred = self.store.note

            self.play_value(pred)

    def play_value(self, predicted_values):
        freq = predicted_values["note"]
        vol = predicted_values["volume"]
        self.send_to_socket(freq, vol)
        time.sleep(.01)

