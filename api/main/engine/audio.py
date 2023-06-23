from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
import numpy as np
import time

# This class implements audio analyzing.
class AudioAnalyzer:

    username = ""
    voice_file = ""
    dialog_file = ""

    time_calc = False

    wav_voice = None
    wav_dialog = None

    processed_wav_voice = None
    processed_wav_dialog = None

    encoder = None
    similarity_dict = None
    dialog_wav_splits = None

    def __init__(self, voice_file, dialog_file, username):
        # initialize voice and dialog file.
        self.voice_file = voice_file
        self.dialog_file = dialog_file
        self.username = username

    def read_files(self):
        if not self.voice_file:
            print("Voice file is required.")
            return

        if not self.dialog_file:
            print("Dialog file is required.")
            return
        
        if self.time_calc:
            start_time = time.time()

        self.wav_voice = Path("api/uploads", self.voice_file)
        self.wav_dialog = Path("api/uploads", self.dialog_file)

        if self.time_calc:
            print("--- %s seconds (Reading audio files) ---" % (time.time() - start_time))

    def preprocess_files(self):
        if self.time_calc:
            start_time = time.time()

        self.processed_wav_voice = preprocess_wav(self.wav_voice)
        self.processed_wav_dialog = preprocess_wav(self.wav_dialog)

        if self.time_calc:
            print("--- %s seconds (Preprocessing audio files) ---" % (time.time() - start_time))

    def calc_utterances(self):
        if self.time_calc:
            start_time = time.time()

        self.encoder = VoiceEncoder("cpu")

        embed, partial_embeds, wav_splits = self.encoder.embed_utterance(self.processed_wav_dialog, return_partials=True)
        speaker_embeds = self.encoder.embed_utterance(self.processed_wav_voice)

        self.similarity_dict = { self.username: partial_embeds @ speaker_embeds }
        self.dialog_wav_splits = wav_splits

        if self.time_calc:
            print("--- %s seconds (Calculating utterances for audio files) ---" % (time.time() - start_time))

    def calc_similarities(self):
        first_person = 0
        audience = 0

        for i in range(0, len(self.dialog_wav_splits)):
            similarities = [s[i] for s in self.similarity_dict.values()]
            best = np.argmax(similarities)
            name, similarity = list(self.similarity_dict.keys())[best], similarities[best]
            if similarity > 0.65:
                first_person = first_person + 1
            else: 
                audience = audience + 1

        return { "voice": first_person / len(self.dialog_wav_splits) # Speaker 1
                    , "username": self.username
                    , "audience": audience / len(self.dialog_wav_splits) # Speaker 2
                }