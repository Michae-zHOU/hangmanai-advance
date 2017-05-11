import numpy
import random

class Word:
    word = ''
    num = 0
    freq = 0.0

def hangman():
    f = open('hw1_word_counts_05.txt', 'r')
    sum = 0
    words = []
    for line in f:
        info = line.split(' ')
        word = Word()
        word.word = info[0]
        word.num = int(info[1])
        words.append(word)
        sum += word.num
    
    for word in words:
        word.freq = word.num/sum

    words.sort(key = lambda x: x.freq, reverse=False)
    print("sum: "+ str(sum))
    print("Least: ")
    for i in range(0,10):
        print(words[i].word+":"+str(words[i].freq))
    print("Most: ")
    for i in range(len(words)-11,len(words)-1):
        print(words[i].word+":"+str(words[i].freq))
    return [words,sum]

def getRandomWord(gameData):
    randomNumber = random.randint(0,gameData[1])
    i = 0
    while randomNumber > 0 and i < len(gameData[0]):
        randomNumber -= gameData[0][i].num
        i += 1
    return gameData[0][i-1].word

def getWordList(currWord,dict,letterTried):
    list = []
    for word in dict:
        satisfy = 1
        for i in range(0,5):
            if currWord[i] == '_' and letterTried.count(word.word[i]) > 0:
                satisfy = 0
            if currWord[i] != '_' and word.word[i] != currWord[i]:
                satisfy = 0
        if satisfy == 1:
            list.append(word)
    return list

def getWord(wordList,letterTried,currWord):
    list = getWordList(currWord,wordList,letterTried)
    r = random.randint(0,len(list))
    return list[r].word

def getDenominatorFrequency(wordList):
    sum = 0
    for word in wordList:
        sum += word.freq
    return sum

def getAlphabetFrequency(denominator,wordList,letterTried):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    sum = 0
    list = {}
    for j in range(0,26):
        list[alphabet[j]] = 0
    for word in wordList:
        already = []
        for i in range(0,5):
            if letterTried.count(word.word[i]) == 0 and word.word[i] not in already:
                list[word.word[i]] += word.freq/denominator
                already.append(word.word[i])
    return list

def main():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Hangman = hangman()
    letterTried = []
    currWord = '_____'
    dict = getWordList(currWord,Hangman[0],letterTried)
    word = getWord(dict,letterTried,currWord)
    countTrial = 0
    while currWord.find('_')!= -1:
        print("Letters Tried: "+str(letterTried))
        dict = getWordList(currWord,dict,letterTried)
        denominator = getDenominatorFrequency(dict)
        alphabetList = getAlphabetFrequency(denominator,dict,letterTried)
        
        maxAlp = 'A'
        maxNum = 0
        for x in range(0,26):
            w = alphabetList[alphabet[x]]
            print(alphabet[x]+" : "+str(w))
            if w > maxNum:
                maxAlp = alphabet[x]
                maxNum = w
        print("Next Best Guess: "+maxAlp+" - "+str(maxNum))
        
        print("Word:"+word)
        letterGuess = input('Guess: ')
        if(len(letterGuess) != 1):
            continue
        countTrial += 1
        print("#"+str(countTrial)+" guess(es), guessing letter "+letterGuess)
        if letterTried.count(letterGuess) == 1:
            continue
        else:
            letterTried.append(letterGuess)
        for i in range(0,len(word)):
            if word[i] == letterGuess:
                currlist = list(currWord)
                currlist[i] = letterGuess
                currWord = ''.join(currlist)
        print(currWord)

    print("Cong!")

if __name__ == "__main__":
    main()
