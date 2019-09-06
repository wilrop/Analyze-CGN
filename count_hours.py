from pydub import AudioSegment
import pandas as pd

FILENAMES = {"dutch_train_data_small.csv": 0,
             "dutch_dev_data_small.csv": 0,
             "dutch_test_data_small.csv": 0,
             "flemish_train_data_small.csv": 0,
             "flemish_dev_data_small.csv": 0,
             "flemish_test_data_small.csv": 0,
             "train_data_small.csv": 0,
             "dev_data_small.csv": 0,
             "test_data_small.csv": 0,
             "dutch_train_data_non_overlapping.csv": 0,
             "dutch_dev_data_non_overlapping.csv": 0,
             "dutch_test_data_non_overlapping.csv": 0,
             "flemish_train_data_non_overlapping.csv": 0,
             "flemish_dev_data_non_overlapping.csv": 0,
             "flemish_test_data_non_overlapping.csv": 0,
             "train_data_non_overlapping.csv": 0,
             "dev_data_non_overlapping.csv": 0,
             "test_data_non_overlapping.csv": 0,
             "dutch_train_data_small_non_overlapping.csv": 0,
             "dutch_dev_data_small_non_overlapping.csv": 0,
             "dutch_test_data_small_non_overlapping.csv": 0,
             "flemish_train_data_small_non_overlapping.csv": 0,
             "flemish_dev_data_small_non_overlapping.csv": 0,
             "flemish_test_data_small_non_overlapping.csv": 0,
             "train_data_small_non_overlapping.csv": 0,
             "dev_data_small_non_overlapping.csv": 0,
             "test_data_small_non_overlapping.csv": 0,
             }


def count_hours():
    for file in FILENAMES:
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            path = row["wav_filename"]
            audio_file = AudioSegment.from_file(path)
            duration = audio_file.duration_seconds
            FILENAMES[file] = FILENAMES[file] + duration
        print(file + ": " + str(FILENAMES[file]/3600))


# This gets called when the python file is executed
if __name__ == "__main__":
    print("Starting the analysis of the data")
    count_hours()

    print("Completed successfully")