""" My system generates and evaluates it own poem. The evaluation is based on
how many lines the poem is. I made the generation because I really enjoy the
aesthetic of multiple lines. Ergo, the more lines there are the higher the score
is! The system takes in a series of Dr. Suess poems and makes a word dictionary.
The dictionary maps every word to another dictionary of potential next words and
their frequency they appear. So for example, we would have:
    { 'when': {'you': 4, 'your': 2, 'our': 1, "she's": 1}, 'and': {'blue,': 1, 'i': 12, 'too': 1} }
which means the statement "when you" appears 4 times and "and i" appears 12 times.
The system picks a random first word from the keys in the dictionary. Then based
on these frequencies, it probabilistically chooses the next words in the poem. And
generates a poem - breaking it up by line by line to give an extra meaning.
Then it evaluates the poem and reads it off in Alex's voice!
"""
import os
import glob
import random
import re

word_table = {}


def say_poem(poem):
    """ Uses the terminal and Alex to read aloud the poem."""
    os.system("say -v Alex -r 140" + poem)


def readInPoems(folder):
    """ Returns a list of of all the words in order they were in the poems."""
    allPoems = ""
    for filename in glob.glob(folder):
        open_poem = open(filename)
        poem_lines = open_poem.read()
        allPoems = allPoems + poem_lines
        allPoems = allPoems.replace('"', " ")

    return re.split("\s+|\n|", allPoems.lower())


def addFrequency(word, frequencies):
    """ If the word is already in the frequency map, it updates the value to
    reflect one more appearance. If not, we add this word to the frequency
    dictionary and map it to 1. Returns the frequencies."""
    if word not in frequencies:
        frequencies[word] = 1
    else:
        frequencies[word] = frequencies[word] + 1
    return frequencies

def addWord(word, next_word):
    """ If the word is already in word table then we add the next word to its
    corresponding frequency map, by calling on the above method. If the word
    is not in the table then we create a new frequency map and map the word
    to the empty frequency map and call the method."""
    if word not in word_table:
        frequency = {}
        addFrequency(next_word, frequency)
        word_table[word] = frequency
    else:
        frequency = word_table[word]
        word_table[word] = addFrequency(next_word, frequency)


def getTotal(frequency):
    """ Returns the total amount of frequencies."""
    total = 0
    for word in frequency:
        total += frequency[word]
    return total


def pickNextHelper(frequency):
    """ Given a particular word's frequency table, this method calculates the
    next word probabilistically. After calculating the total of the frequencies,
    it produces a random number and then loops through the frequencies, adding
    up until the counter exceeds the random integer and returns it. If this fails
    it will return None."""
    total = getTotal(frequency)
    counter = 0
    randomInt = random.randint(0, total)
    for word in frequency:
        counter += frequency[word]
        if counter >= randomInt:
            return word
    return None


def pickNextWord(current_word):
    """ This is a helper method that double checks that the current word has
    a next word. If the word is in the table, it directs to the next method."""
    if current_word not in word_table:
        return None
    else:
        return pickNextHelper(word_table[current_word])


def makeWordDictionary(filenames):
    """ Goes through the list of all the words and extracts the current word and
    the next word. Then it adds the pair to the word dictionary. After all of the
    words, it returns the word table."""
    allPoems = readInPoems(filenames)
    for num in range(0, len(allPoems) - 1):
        word = allPoems[num]
        next_word = allPoems[num + 1]
        addWord(word, next_word)
    print(word_table)
    return word_table


def makePoem(table):
    """ The method first picks the first word randomly from the keys of
     the word table. Then it goes through and uses the methods above to
     pick next word based on the table. It returns the finished poem."""
    current_word = random.choice(list(table))
    poem = [current_word]
    for x in range(0, 20):
        next_word = pickNextWord(current_word)
        poem.append(next_word)
        current_word = next_word
    return poem


def evaluate_and_format(poem):
    """ Calculates number of lines based on the next lines due to punctuation.
    And then it returns a list of the string poem and the fitness."""
    format = ""
    basic = ""
    lines = 0
    for word in poem:
        format = format + " " + word
        basic = basic + " " + word
        if len(word) != 0:
            if word[-1] == "." or word[-1] == "!" or word[-1] == "," or word[-1] == "?":
                format = format + "\n"
                lines = lines + 1
    return [lines, format, basic]


if __name__ == '__main__':
    """ Goes through all the methods necessary and finally says the new poem."""
    table = makeWordDictionary("childrensPoems/*")
    poem = makePoem(table)
    lines_and_format = evaluate_and_format(poem)
    print(lines_and_format[1])
    say_poem(lines_and_format[2])
