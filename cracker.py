from wordle import Guesser

if __name__ == '__main__':
    wordle = Guesser(5, 'words_alpha.txt')
    print("Input \n0 for incorrect \n1 for correct \n2 for incorrect position")

    while True:
        word = wordle.makeGuess()
        good = input(f'Does "{word}" work? Y/n ')
        if len(good) > 0 and good.lower()[0] == 'n':
            continue
        if len(wordle.wordChoices) <= 1:
            print("No more word choices")
            break
        for i, l in enumerate(word):
            if l in wordle.correctPositions:
                continue
            setting = int(input(f"{l}: "))
            if setting == 0:
                wordle.addIncorrectLetters({l,})
            elif setting == 1:
                wordle.addCorrectPositions({l: [i]})
            elif setting == 2:
                wordle.addIncorrectPositions({l: [i]})