import sys
import os
from os import path
import soundfile as sf
import pandas as pd

FILENAME = "data.csv"

# The main procedure that gets called at the start of the program.
def analyze_data(target):
    # Check to see if we get a correct path
    if not path.isdir(target):
        print("Could not locate the target")
    else:
        print("Found top level directory in: ", target)

    print("Locating the sound files and corresponding annotations")

    data = pd.DataFrame()

    # Go to the audio directory
    audio_path = path.join(target, "data/audio/wav")

    # We first iterate over all the files and place their duration in the dictionary so we can later analyze them
    for x in os.listdir(audio_path):
        new_audio_path = path.join(audio_path, x)
        # If we find a correct directory we need to enter
        if os.path.isdir(new_audio_path) and x.startswith("comp"):
            print("---------------------------------------------------------")
            print("Entering directory " + x)
            new_data = get_values_for_component(new_audio_path, x)
            data = data.append(new_data)
            print("---------------------------------------------------------")

    with open(FILENAME, 'w+') as f:
        # We only want to write the header the first time, hence the quick check "header = ..."
        data.to_csv(f, sep=',', header=True, index=False, encoding="ascii")


# This function takes care of one component of the data
def get_values_for_component(audio_path, comp):
    data = pd.DataFrame()

    for x in os.listdir(audio_path):
        print("Processing the files for language: " + x)
        new_audio_path = path.join(audio_path, x)
        # This check is just to make sure the directory exists
        new_data = get_values_for_language(new_audio_path, x, comp)
        data = data.append(new_data)

    return data


# This function processes one language of a component each time it gets called
def get_values_for_language(audio_path, lang, comp):
    files = os.listdir(audio_path)
    values = []

    # Check all speech files for validity
    for file in files:
        final_path = path.join(audio_path, file)

        # Calculate the length of the speech file
        speech = sf.SoundFile(final_path)
        samples = len(speech)
        sample_rate = speech.samplerate
        seconds = samples/sample_rate

        values.append(seconds)

    processed_data = {
        'component': [comp] * len(values),
        'language': [lang] * len(values),
        'length': values
    }

    # A data frame of all the processed data
    df = pd.DataFrame(processed_data, columns=['component', 'language', 'length'])

    return df


# This gets called when the python file is executed
if __name__ == "__main__":
    print("Starting the analysis of the data")

    analyze_data(sys.argv[1])

    print("Completed successfully")