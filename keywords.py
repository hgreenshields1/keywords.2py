# -*- coding: utf-8 -*-
import string
import re
from spellchecker import SpellChecker
from textblob import TextBlob
from autocorrect import Speller

keywords = ["our energy supply", "smart grids", "Smart grids", "a key enabler", "a more sustainable power system",
            "real-time data gathering", "the intelligent control", "The aim", "a smart grid", "Yu", "Xue",
            "the behaviours", "actions", "all the stakeholders", "the energy supply chain",
            "sustainable, economic and secure electric energy", "economical and environmentally sustainable use",
            "the inception", "smart meter systems", "peer"]


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
            noThe = word.replace("the ", '')
            noThe = noThe.strip()
            withoutThe.append(noThe)
        else:
            withoutThe.append(word)
    return withoutThe


def removeA(words):
    withoutA = []
    lower = LowerCase(words)
    for word in lower:
        x = re.findall("a +", word)
        y = re.findall("^a ", word)
        if y:
            noA = word.replace("a ", '')
            noA = noA.strip()
            withoutA.append(noA)
        elif x:
            noA = word.replace(" a ", '')
            noA = noA.strip()
            withoutA.append(noA)
        else:
            withoutA.append(word)
    return withoutA


def removeOf(words):
    withoutOf = []
    lower = LowerCase(words)
    for word in lower:
        x = re.findall("of +", word)
        if x:
            noOf = word.replace("of ", '')
            noOf = noOf.strip()
            withoutOf.append(noOf)
        else:
            withoutOf.append(word)

    return withoutOf


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
    check = Speller(lang='en')
    corrected = []
    for word in words:
        correct = check(word)
        # correct = TextBlob(word)
        # correct = str(correct.correct())
        corrected.append(correct)

    return corrected


def removeSomeNumbers(words):
    noNumbers = []
    for word in words:
        split = word.split(" ")
        backTogether = ""
        for entity in split:

            chars = set('$%£€')
            if any((c in chars) for c in entity):
                continue
            else:
                backTogether = backTogether + " " + entity
                backTogether = backTogether.lstrip()
        if backTogether != "":
            noNumbers.append(backTogether)

    return noNumbers


def runAll():
    lower = LowerCase(keywords)
    noNum = removeSomeNumbers(lower)
    noThe = NoThe(noNum)
    noA = removeA(noThe)
    noOf = removeOf(noA)
    splitUp = splitAnd(noOf)
    noPunct = NoPunctuation(splitUp)
    correct = autoCorrect(noPunct)

    return correct


print(runAll())
