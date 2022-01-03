import string
import random

def load_words(dictionaryFile):
    with open(dictionaryFile) as word_file:
        valid_words = set(word_file.read().split())

    badWords = set()
    for word in valid_words:
        for l in word:
            if l not in string.ascii_lowercase:
                badWords.add(word)
                break
    return valid_words - badWords



class Guesser:
    def __init__(self, wordSize, dictionaryFile):
        self.dictionary = set(i for i in load_words(dictionaryFile) if len(i) == wordSize)
        self.wordChoices = self.dictionary.copy()

        self.frequencies = self.letterFrequency(self.dictionary)
        self.scores = self.wordScore(self.dictionary, self.frequencies)

        self.incorrectLetters = set()
        self.correctPositions = {}
        self.incorrectPositions = {}
        
    def letterFrequency(self, dictionary):
        letters = {}
        for letter in string.ascii_lowercase:
            letters[letter] = 0

        t = 0
        for word in dictionary:
            for letter in word:
                letters[letter] += 1
                t += 1
        for letter in letters:
            letters[letter] /= t
        
        return letters

    def wordScore(self, dictionary, frequency):
        scores = {}
        for word in dictionary:
            scores[word] = 0
            for letter in word:
                scores[word] += frequency[letter]

        return scores

    def makeGuess(self):
        word = self.bestGuess()
        self.wordChoices.remove(word)
        return word

    def bestGuess(self):
        orderedWords = self.guesses()
        word = ""
        letters = 0

        i = 0
        while i < len(orderedWords):
            seen = set()
            for letter in orderedWords[i]:
                seen.add(letter)
            if len(seen) > letters:
                word = orderedWords[i]
                letters = len(set(word))
            i += 1
    
        return word

    def guesses(self):
        return sorted(list(self.wordChoices), key=self.scores.get, reverse=True)
    
    def addIncorrectLetters(self, letters):
        self.incorrectLetters = self.incorrectLetters.union(letters)
        
        goodWords = set()
        for word in self.wordChoices:
            passed = True
            for letter in self.incorrectLetters:
                if letter in word:
                    passed = False
                    break
            if passed:
                goodWords.add(word)
        
        self.wordChoices = goodWords
            

    def addIncorrectPositions(self, positions):
        for letter in positions:
            if letter in self.incorrectPositions:
                self.incorrectPositions[letter].extend(positions[letter])
            else:
                self.incorrectPositions[letter] = positions[letter]
        
        goodWords = set()
        for word in self.wordChoices:
            passed = True
            for letter in self.incorrectPositions:
                if letter not in word:
                    passed = False
                    break
                for position in self.incorrectPositions[letter]:
                    if word[position] == letter:
                        passed = False
                        break
            
            if passed:
                goodWords.add(word)

        self.wordChoices = goodWords

    def addCorrectPositions(self, positions):
        for letter in positions:
            if letter in self.correctPositions:
                self.correctPositions[letter].extend(positions[letter])
            else:
                self.correctPositions[letter] = positions[letter]

        goodWords = set()
        for word in self.wordChoices:
            passed = True
            for letter in self.correctPositions:
                for position in self.correctPositions[letter]:
                    if word[position] != letter:
                        passed = False
                        break
            
            if passed:
                goodWords.add(word)
        
        self.wordChoices = goodWords



class Game:
    def __init__(self, dictionaryFile, wordLength = 5, guesses = 6):
        self.dictionary = load_words(dictionaryFile)
        self.setup(wordLength, guesses)

    def setup(self, wordlength = 5, guesses = 6):
        self.wordLength = wordlength
        self.attempts = guesses

        self.guesses = []
        self.word = random.choice(self.dictionary)
        self.letters = set(self.word)

    def newGame(self, wordlength = 5, guesses = 6):
        self.setup(wordlength, guesses)
    
    def makeGuess(self, word):
        if len(word) != self.wordLength:
            return {'error': f"{word} is not {self.wordLength} long"}
        if word not in self.dictionary:
            return {'error': f"{word} is not in the word list"}

        self.guesses.append(word)

        codes = []
        for l1, l2 in zip(word, self.word):
            if l1 == l2:
                codes.append(1)
                continue
            if l1 in self.letters:
                codes.append(2)
            else:
                codes.append(0)
        
        return codes