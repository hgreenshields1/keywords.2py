# -*- coding: utf-8 -*-
import string
import re
from spellchecker import SpellChecker
from textblob import TextBlob

keywords = ["ML",
            "datasets",
            "the dataset",
            "Machine learning",
            "the field",
            "computer science",
            "automated systems",
            "expert-written rules",
            "the key technologies",
            "the current fourth industrial revolution",
            "the ML market",
            "$6.9B",
            "a 43.8% compound annual growth rate",
            "The sub",
            "fields",
            "various ways",
            "A divide",
            "classical' machine learning techniques",
            "'deep learning",
            "(DL"]


def NoPunctuation(words):
    noPunct = []
    for word in words:
        noP = word.translate(str.maketrans('', '', string.punctuation))
        # remove = dict.fromkeys(map(ord, '\n' + string.punctuation.replace('-', '')))
        # noP = word.translate(remove)
        noPunct.append(noP)

    return noPunct


def LowerCase(words):
    lowerkeywords = []
    for word in words:
        lowerword = word.lower()
        lowerkeywords.append(lowerword)

    return lowerkeywords


def NoThe(words):
    withoutThe = []
    lower = LowerCase(words)
    for word in lower:
        x = re.findall("the +", word)
        if x:
            noThe = word.replace("the", '')
            noThe = noThe.strip()
            withoutThe.append(noThe)
        else:
            withoutThe.append(word)

    return withoutThe


def splitAnd(words):
    splitKeyWords = []
    for word in words:
        x = re.findall("and +", word)
        if x:
            split = word.split("and ")
            for entity in split:
                entity = entity.strip()
                splitKeyWords.append(entity)
        else:
            splitKeyWords.append(word)

    return splitKeyWords


def autoCorrect(words):
    # spell = SpellChecker()
    corrected = []
    for word in words:
        correct = TextBlob(word)
        correct = str(correct.correct())
        corrected.append(correct)

    return corrected


def runAll():
    lower = LowerCase(keywords)
    noThe = NoThe(lower)
    splitUp = splitAnd(noThe)
    noPunct = NoPunctuation(splitUp)
    correct = autoCorrect(noPunct)

    return correct


print(runAll())
