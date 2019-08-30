# A project for analyzing the data in the Corpus Gesproken Nederlands (CGN)
This project contains scripts and python notebooks used in the process of analyzing the data in the CGN. 

## analyze.py
This script first fills a dictionary with the audio file lengths. Afterwards it performs some basic analysis on this dictionary. For each component, the two languages and the combined dataset it will generate a description and save a histogram and boxplot.
This script was later discarded, because of the added computational cost of going over all audio files in the corpus every time. 
Its role has been filed by the other files in this project. This script however still technically works.

## gather_data.py
This script will go over the entire corpus, collecting for every audio file the component it came from, its language and the length of this file.
Finally, it will write this data to a new file. Its role is purely in collecting all of the data so that can later be used for actual analysis.

## Python notebooks: analyze_complete_CGN.ipynb and analyze_split_CGN.ipynb
These interactive python notebooks fulfill the second part of analyze.py, namely that they generate descriptions and histograms for portions of the data. As the names might show, the first notebook operates on the complete dataset and the second notebook on the dataset after splitting. There is no actual necessity to have two separate notebooks for these, but it adds ease of use.

