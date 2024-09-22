import numpy as np
import os, requests

if not os.path.exists('en.txt'):
    resp = requests.get('https://raw.githubusercontent.com/lorenbrichter/Words/master/Words/en.txt')
    with open('en.txt', 'wb') as f:
        f.write(resp.content)

with open('en.txt', 'r') as f:
    # Read word list, newline character is the spliter
    word_list = np.array(f.read().split('\n'))

# Get the length of each word in the word list
word_lengths = np.vectorize(len)(word_list)

def getRandomWord(length):
    # Find all words that match the length
    indices = np.where(word_lengths == length)[0]
    
    # If not found
    if len(indices) == 0:
        return None
    
    # Choose one word randomly
    random_index = np.random.choice(indices)

    return str(word_list[random_index])

def isWordInList(word):
    # Check if the word is in the word list
    return word in word_list
