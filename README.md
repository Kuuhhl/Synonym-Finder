# Synonym Finder
Synonym Finder is a GUI tool to easily replace words in your essay with their synonyms. Currently, the only supported language is German.

# Requirements
```
Python 3.8
spacy
```

# Installation
* Run `pip install spacy` to install spacy. We need it to process our language data.
* Run `python -m spacy download de_core_news_sm` to download the german language model.

# How to use it
* Open `main.py`.
* Navigate to your text-file.
* Follow the GUI instructions.
* The finished file will be output to the script directory as `output.txt`.

# TODO
* Improve visibility on long sentences
* Improve speed and responsiveness of GUI
* Add scrollbar to text
# Issues
If you have any issues, you can report them [here](https://github.com/Kuuhhl/Synonym-Finder/issues).
