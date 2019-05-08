import sys
import os
from os import path
import soundfile as sf
import pandas as pd
import matplotlib.pyplot as plt

# The values gathered in processing the data will come in this dictionary. Every comp has another dictionary as value.
# This dictionary holds the different languages. Each language has as a value a list of durations for its audio files.
DIRECTORY = "Results"
VALUES = {"comp-a": {"nl": [], "vl": []},
          "comp-b": {"nl": [], "vl": []},
          "comp-c": {"nl": [], "vl": []},
          "comp-d": {"nl": [], "vl": []},
          "comp-e": {"nl": [], "vl": []},
          "comp-f": {"nl": [], "vl": []},
          "comp-g": {"nl": [], "vl": []},
          "comp-h": {"nl": [], "vl": []},
          "comp-i": {"nl": [], "vl": []},
          "comp-j": {"nl": [], "vl": []},
          "comp-k": {"nl": [], "vl": []},
          "comp-l": {"nl": [], "vl": []},
          "comp-m": {"nl": [], "vl": []},
          "comp-n": {"nl": [], "vl": []},
          "comp-o": {"nl": [], "vl": []}}


# The main procedure that gets called at the start of the program.
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

    # Analyze the entire dataset and every component
    analyze_all_and_components()
    # Analyze the languages (Flemish and Dutch)
    analyze_languages()


# This procedure will provide an analysis of each component and an overal analysis of the entire dataset.
def analyze_all_and_components():
    all_values = []
    # Loop over all components.
    for component in VALUES:
        langs = VALUES[component]
        component_values = []
        # Loop over the languages.
        for lang in langs:
            values = langs[lang]
            # Loop over all the values
            for value in values:
                all_values.append(value)
                component_values.append(value)
        print("Analyzing component: " + component)
        analyze_values(component_values, component)

    print("Analyzing the entire dataset")
    analyze_values(all_values, "All")


def analyze_languages():
    dutch_values = []
    flemish_values = []

    for component in VALUES:
        langs = VALUES[component]
        for lang in langs:
            values = langs[lang]
            for value in values:
                if lang == "nl":
                    dutch_values.append(value)
                else:
                    flemish_values.append(value)

    print("Analyzing the Dutch audio files")
    analyze_values(dutch_values, "Dutch")
    print("Analyzing the Flemish audio files")
    analyze_values(flemish_values, "Flemish")


# This procedure gets called with a list of values that it will analyze
def analyze_values(values, title):
    s = pd.Series(values)

    # Plot and save a histogram, afterwards close it again so we can continue with other plots
    s.hist()
    hist_title = "Hist " + title
    hist_file = path.join(DIRECTORY, hist_title)
    plt.title(hist_title)
    plt.savefig(hist_file)
    plt.close()

    # Plot and save a boxplot. We also close it just to be sure, in the future we might want to add more plots.
    s.plot.box()
    box_title = "Box " + title
    box_file = path.join(DIRECTORY, box_title)
    plt.title(box_title)
    plt.savefig(box_file)
    plt.close()

    description_title = "Description " + title + ".csv"
    description_file = path.join(DIRECTORY, description_title)
    description = s.describe()
    print(description)
    with open(description_file, 'w+') as f:
        description.to_csv(f, sep=',', encoding="ascii")


# This function takes care of one component of the data
def get_values_for_component(audio_path, comp):
    for x in os.listdir(audio_path):
        print("Processing the files for language: " + x)
        new_audio_path = path.join(audio_path, x)
        # This check is just to make sure the directory exists
        values = get_values_for_language(new_audio_path)
        VALUES[comp][x] = values


# This function processes one language of a component each time it gets called
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

        values.append(seconds)

    return values


# This gets called when the python file is executed
if __name__ == "__main__":
    print("Starting the analysis of the data")

    analyze_data(sys.argv[1])

    print("Completed successfully")