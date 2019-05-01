"""Import file contain the stop words"""
from .stop_words import WORDS_FRENCH

class Parsing:
    """The class makes it possible to parse in the list of words the question of the user
    A constructor is used by allowing the user to indicate the number of letters"""
    def __init__(self, phrase, nb_letter, result=""):
        # Word list splitting
        self.phrase = phrase.split()
        self.result = result
        self.nb_letter = nb_letter

    def parser(self):
        myList = []
        for l in self.phrase:
            if l not in WORDS_FRENCH and len(l) > self.nb_letter:
                myList.append(l + " ")
                self.result = "".join(myList)
                self.result = self.result.lower()
                for ch in ["l'", "d'"]:
                    if ch in self.result :
                        self.result = self.result.replace(ch,"")

        return self.result
