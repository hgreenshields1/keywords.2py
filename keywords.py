# -*- coding: utf-8 -*-
import string
import re

from textblob import TextBlob
from autocorrect import Speller

keywords = ["biofabrication", "Biofabrication", "3D printing", "healthcare", "research", "3D printers", "their use",
            "additive manufacturing", "The term", "'biofabrication", "the early 1990s", "academic publications",
            "biomineralization bioengineering", "the term", "scope", "the marriage", "biology", "microfabrication",
            "the automated generation", "biologically functional products", "plastics", "living cells", "molecules",
            "living organisms", "bio-fabricated' meat", "bio-fabricated leather", "their use", "clinical healthcare",
            "lives", "biomineralization bioengineering", "biology and microfabrication"]


def NoPunctuation(words):
    noPunct = []
    for word in words:
        remove = dict.fromkeys(map(ord, '\n' + string.punctuation.replace('-', '')))
        noP = word.translate(remove)

        x = re.findall("- +", noP)
        y = re.findall("^- ", noP)
        z = re.findall(" -$", noP)
        if y:
            startDash = word.replace("- ", '')
            startDash = startDash.strip()
            noPunct.append(startDash)
        elif z:
            endDash = word.replace(" -", '')
            endDash = endDash.strip()
            noPunct.append(endDash)
        elif x:
            middleDash = word.replace(" - ", ' ')
            middleDash = middleDash.strip()
            noPunct.append(middleDash)
        else:
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
    check = Speller(lang='en')
    corrected = []
    for word in words:
        x = re.findall("-+", word)
        if x:
            isCorrect = 0
            split = word.split("-")
            for entity in split:
                a = TextBlob(entity)
                temp = str(a.correct())
                if temp != entity:
                    isCorrect = isCorrect + 1

            if isCorrect > 0:
                noDash = word.translate(str.maketrans('', '', string.punctuation))
                correct = check(noDash)
                corrected.append(correct)
            else:
                corrected.append(word)
        else:
            corrected.append(word)
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
