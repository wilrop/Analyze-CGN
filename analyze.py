import sys
import os
from os import path
import soundfile as sf
import pandas as pd

MAX_SECS = 10
MIN_SECS = 3
VALUES = {"comp-a": {"nl": [], "vl": []},
          "comp-b": {"nl": [], "vl": []},
          "comp-c": {"nl": [], "vl": []},
          "comp-d": {"nl": [], "vl": []},
          }


def analyze_data(target):
    # Check to see if we get a correct path
    if not path.isdir(target):
        print("Could not locate the target")
    else:
        print("Found top level directory in: ", target)

    print("Locating the sound files and corresponding annotations")

    # Go to the audio directory
    audio_path = path.join(target, "data/audio/wav")

    # We first iterate over all the files and place their duration in the dictionary so we can later analyze them
    for x in os.listdir(audio_path):
        new_audio_path = path.join(audio_path, x)
        # If we find a correct directory we need to enter
        if os.path.isdir(new_audio_path) and x.startswith("comp"):
            print("---------------------------------------------------------")
            print("Entering directory " + x)
            get_values_for_component(new_audio_path, x)
            print("---------------------------------------------------------")

    analyze_all_and_components()
    analyze_languages()


def analyze_all_and_components():
    all_values = []
    for component in VALUES:
        component_values = []
        for lang in component:
            for value in lang:
                all_values.append(value)
                component_values.append(value)
        analyze_values(component_values)

    analyze_values(all_values)


def analyze_languages():
    dutch_values = []
    flemish_values = []

    for component in VALUES:
        for lang in component:
            for value in lang:
                if lang == "nl":
                    dutch_values.append(value)
                else:
                    flemish_values.append(value)

    analyze_values(dutch_values)
    analyze_values(flemish_values)


def analyze_values(values):
    df = pd.DataFrame(values)

    df.describe()
    df.boxplot()


# This function takes care of one component of the data
def get_values_for_component(audio_path, comp):
    for x in os.listdir(audio_path):
        print("Processing the files for language: " + x)
        new_audio_path = path.join(audio_path, x)
        # This check is just to make sure the directory exists
        values = get_values_for_language(new_audio_path)
        VALUES[comp][x] = values


# This function processes one language each time it gets called
def get_values_for_language(audio_path):
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

        if seconds > MAX_SECS or seconds < MIN_SECS:
            pass
        else:
            values.append(seconds)

    return values


if __name__ == "__main__":
    print("Starting the analysis of the data")

    analyze_data(sys.argv[1])

    print("Completed successfully")