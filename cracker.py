import string
class Wordle:
    def load_words(self):
        with open(self.dictionaryFile) as word_file:
            valid_words = set(word_file.read().split())

        badWords = set()
        for word in valid_words:
            for l in word:
                if l not in string.ascii_lowercase:
                    badWords.add(word)
                    break
        return valid_words - badWords


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

    def bestWord(self):
        orderedWords = sorted(list(self.wordChoices), key=self.scores.get, reverse=True)

        words = []
        i = 0
        while i < len(orderedWords):
            seen = set()
            for letter in orderedWords[i]:
                seen.add(letter)
            if len(seen) == 5:
                words.append(orderedWords[i])
            i += 1
        self.wordChoices.remove(words[0])
        return words[0]

    def __init__(self, wordSize, dictionaryFile):
        self.dictionaryFile = dictionaryFile
        self.dictionary = set(i for i in self.load_words() if len(i) == wordSize)
        self.wordChoices = self.dictionary.copy()

        self.frequencies = self.letterFrequency(self.dictionary)
        self.scores = self.wordScore(self.dictionary, self.frequencies)

        self.incorrectLetters = set()
        self.correctPositions = {}
        self.incorrectPositions = {}
    
    def addIncorrectLetters(self, letters):
        self.incorrectLetters = self.incorrectLetters.union(letters)
    def addIncorrectPositions(self, positions):
        for letter in positions:
            if letter in self.incorrectPositions:
                self.incorrectPositions[letter].extend(positions[letter])
            else:
                self.incorrectPositions[letter] = positions[letter]
    def addCorrectPositions(self, positions):
        for letter in positions:
            if letter in self.correctPositions:
                self.correctPositions[letter].extend(positions[letter])
            else:
                self.correctPositions[letter] = positions[letter]

    def updateWordChoices(self):
        goodWords = set()

        for word in self.wordChoices:
            passed = True
            for letter in self.incorrectLetters:
                if letter in word:
                    passed = False
                    break
            for letter in self.incorrectPositions:
                if letter not in word:
                    passed = False
                    break
                for position in self.incorrectPositions[letter]:
                    if word[position] == letter:
                        passed = False
                        break
            for letter in self.correctPositions:
                if letter not in word:
                    passed = False
                    break
                for position in self.correctPositions[letter]:
                    if word[position] != letter:
                        passed = False
                        break
            
            if passed:
                goodWords.add(word)
        
        self.wordChoices = goodWords


wordle = Wordle(5, 'words_alpha.txt')
print("Input \n0 for correct \n1 for incorrect \n2 for incorrect position")

while True:
    word = wordle.bestWord()
    good = input(f'Try "{word}" ')
    if int(good) == 0:
        continue
    for i, l in enumerate(word):
        setting = int(input(f"{l}: "))
        if setting == 1:
            wordle.addIncorrectLetters({l,})
        elif setting == 0:
            wordle.addCorrectPositions({l: [i]})
        elif setting == 2:
            wordle.addIncorrectPositions({l: [i]})

    wordle.updateWordChoices()