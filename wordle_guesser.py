import random
import numpy as np
import re # ToDo redo with regex


def get_words(word_list, n=1):
    return random.choices(word_list, k=n)


def word_match(guess, word):
    misses = set(guess).difference(word)
    matches = set(guess).intersection(word)
    exact_matches = [(l, guess.index(l)) for l in matches if guess.index(l) == word.index(l)]
    inexact_matches, _ = zip(*exact_matches) if exact_matches else (set(), None)
    inexact_matches = matches.difference(inexact_matches)
    inexact_matches = [(l, guess.index(l)) for l in inexact_matches]
    return misses, matches, exact_matches, inexact_matches


def refine_list(misses, matches, exact_matches, inexact_matches, word_list):
    # Remove words that contain letters not in the guess
    new_list = [word for word in word_list if misses.isdisjoint(word)]
    # Only keep words with letters in the guess
    new_list = [word for word in new_list if matches.intersection(word)]
    # Only keep words with exact matches in the guess
    if exact_matches:
        new_list = [word for word in new_list for l, i in exact_matches if word[i] == l]
    # Only keep words with inexact matches in the guess, but not in the missed position
    if inexact_matches:
        new_list = [word for word in new_list for l, i in inexact_matches if l in word and word[i] != l]
    return new_list


'''
Start Code here
'''
with open('wordle_words.txt', 'r') as in_file:
   words = [w.strip() for w in in_file]

remaining_words = np.array(words)
all_misses = set()

todays_word = get_words(words)[0]

guess = input("Enter a five letter word: ")
remaining_words = remaining_words[~(remaining_words == guess)]

misses, matches, exact_matches, inexact_matches = word_match(guess, todays_word)
all_misses.update(misses)
# Reduce the remaining words based on the match results
remaining_words  = refine_list(misses, matches, exact_matches, inexact_matches, remaining_words)

# Make another guess
guess = get_words(remaining_words)[0]
remaining_words = remaining_words[~(remaining_words == guess)]
misses, matches, exact_matches, inexact_matches = word_match(guess, todays_word)
all_misses.update(misses)
remaining_words  = refine_list(misses, matches, exact_matches, inexact_matches, remaining_words)
