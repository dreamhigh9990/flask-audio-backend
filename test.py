from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
import numpy as np

# DEMO 02: we'll show how this similarity measure can be used to perform speaker diarization
# (telling who is speaking when in a recording).


## Get reference audios
# Load the interview audio from disk
# Source for the interview: https://www.youtube.com/watch?v=X2zqiX6yL3I
import time

start_time = time.time()

wav_first = Path("audio_data", "Kyle Gass.mp3")
wav_second = Path("audio_data", "Sean Evans.mp3")
wav_fpath = Path("audio_data", "X2zqiX6yL3I.mp3")

print("--- %s seconds(read file) ---" % (time.time() - start_time))

wav = preprocess_wav(wav_fpath)
wav1 = preprocess_wav(wav_first)
wav2 = preprocess_wav(wav_second)

print("--- %s seconds(preprocess) ---" % (time.time() - start_time))
# Cut some segments from single speakers as reference audio
# segments = [[0, 5.5], [6.5, 12], [17, 25]]
# segments = [[0, 5.5]]
segments = [[0, 5.5], [6.5, 12]]
speaker_names = ["Kyle Gass", "Sean Evans", "Jack Black"]
# speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]
speaker_wavs = [wav1, wav2]

## Compare speaker embeds to the continuous embedding of the interview
# Derive a continuous embedding of the interview. We put a rate of 16, meaning that an 
# embedding is generated every 0.0625 seconds. It is good to have a higher rate for speaker 
# diarization, but it is not so useful for when you only need a summary embedding of the 
# entire utterance. A rate of 2 would have been enough, but 16 is nice for the sake of the 
# demonstration. 
# We'll exceptionally force to run this on CPU, because it uses a lot of RAM and most GPUs 
# won't have enough. There's a speed drawback, but it remains reasonable.
encoder = VoiceEncoder("cpu")
print("Running the continuous embedding on cpu, this might take a while...")
# _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True)

print("--- %s seconds(encoder) ---" % (time.time() - start_time))

# Get the continuous similarity for every speaker. It amounts to a dot product between the 
# embedding of the speaker and the continuous embedding of the interview
speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in 
                   zip(speaker_names, speaker_embeds)}

print("--- %s seconds(calculate simulation) ---" % (time.time() - start_time))

## Run the interactive demo
# interactive_diarization(similarity_dict, wav, wav_splits)
first_person = 0
second_person = 0
for i in range(0, len(wav_splits)):
    similarities = [s[i] for s in similarity_dict.values()]
    best = np.argmax(similarities)
    name, similarity = list(similarity_dict.keys())[best], similarities[best]
    if similarity > 0.65:
        if best == 0:
            first_person = first_person + 1
        elif best == 1:
            second_person = second_person + 1

print("First Person: {0}".format(first_person / len(wav_splits)))
print("Second Person: {0}".format(second_person / len(wav_splits)))