from tkinter import *
from tkinter import ttk
import re
import spacy
import itertools


def writeChanges(sentence):
    if sentence == "":
        return
    with open("output.txt", "a") as f:
        f.write(f"{sentence} ")


def getIndexOfListValue(inputList, searchTerm):
    for index, value in enumerate(inputList):
        if value == searchTerm:
            return index


def removeChildrenOfFrame(inputFrame):
    [child.destroy() for child in inputFrame.winfo_children()]


def removeDuplicatesFromList(inputList):
    return list(set(inputList))


def joinLists(inputList):
    return list(itertools.chain.from_iterable(inputList))


def parseDict():
    with open("src/openthesaurus.txt", "r", encoding="UTF-8") as f:
        return [
            re.sub("\(.*?\)", "", line).strip().split(";") for line in f.readlines()
        ]


def splitSentences(text):
    return [sent.string.strip() for sent in nlp(text).sents]


def lemmatizeWord(word):
    return [token.lemma_ for token in nlp(word)][0]


def tokenizeText(text):
    return [token.text for token in nlp(text)]


def parseDict():
    with open("src/openthesaurus.txt", "r", encoding="UTF-8") as f:
        return [
            re.sub("\(.*?\)", "", line).strip().split(";") for line in f.readlines()
        ]


def getSynonyms(definitions, searchString):
    return [definition for definition in definitions if searchString in definition]


def getSentenceFromFrame(textFrame):
    sentence = []
    for child in textFrame.winfo_children():
        try:
            sentence.append(child.get())
        except:
            sentence.append(child["text"])
    return re.sub(r'\s([?.!,;"](?:\s|$))', r"\1", " ".join(sentence))


def continueToNext(sentences, sentenceNumber, textFrame, root):
    sentenceNumber += 1
    writeChanges(getSentenceFromFrame(textFrame))
    removeChildrenOfFrame(textFrame)
    populateTextArea(sentences, sentenceNumber, textFrame, root)


def populateTextArea(sentences, sentenceNumber, textFrame, root):
    nextSentenceButton = Button(
        root,
        text="Apply and continue",
        command=lambda: continueToNext(sentences, sentenceNumber, textFrame, root),
    )
    nextSentenceButton.grid(row=2, column=0, sticky="nesw", pady=(20, 0))

    sentence = sentences[sentenceNumber]

    # Loop over words of sentence
    for index, word in enumerate(tokenizeText(sentence)):
        word = word.strip()
        # join all Lists of synonyms per word; remove duplicates
        synonyms = removeDuplicatesFromList(
            joinLists(getSynonyms(parseDict(), lemmatizeWord(word)))
        )
        if synonyms == []:
            textLabel = Label(textFrame, text=word)
            textLabel.grid(row=1, column=index, sticky="nesw")
            continue
        # replace lemmatized word with default text if it is in combobox
        try:
            synonyms.remove(lemmatizeWord(word))
        except ValueError:
            pass
        synonyms.insert(0, word)
        # remove duplicates
        synonyms = removeDuplicatesFromList(synonyms)
        # Create ComboBox
        comboBoxSynonyms = ttk.Combobox(textFrame, values=synonyms)
        # Place it in Grid
        comboBoxSynonyms.grid(row=1, column=index, sticky="nesw")
        # set value of ComboBox to default text
        for index, value in enumerate(comboBoxSynonyms["values"]):
            if value == word:
                comboBoxSynonyms.current(index)
                break


def main():
    global nlp
    nlp = spacy.load("de_core_news_sm")
    try:
        with open("original.txt", "r", encoding="UTF-8") as f:
            text = f.read().replace("\n", "")
    except FileNotFoundError:
        exit("Please create a file called 'original.txt'")
    sentences = splitSentences(text)

    root = Tk()
    textFrame = Frame(master=root)
    textFrame.grid(row=1, column=0)

    continueToNext(sentences, -1, textFrame, root)

    root.mainloop()


main()