from datetime import datetime, timedelta
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

class play_wordle():
    wordle_start_date = datetime(2021, 6, 3)
    def __init__(self, source_list='wordle_words_unsorted.txt'):
        self.wordle_dict = source_list
        self.reset_wordle(read_word_list=True)
    
    def reset_wordle(self, read_word_list=False):
        if read_word_list:
            self.read_dict()
        self.remaining_words = np.array(self.words)
        self.all_misses = set()

    def read_dict(self):
        with open(self.wordle_dict, 'r') as in_file:
            self.words = [w.strip() for w in in_file]
    
    def get_a_word(self, idx=0, random=False, today=False):
        if today:
            idx_today = (datetime.today() - self.wordle_start_date).days
            word = self.words[idx_today]
        elif random:
            word = self.words[random.range(len(self.words))]
        else:
            word = self.words[idx]
        return word
    
    def make_a_guess(self, my_guess=None):
        if my_guess:
            guess = input("Enter a five letter word: ")
        else:
            # Let the computer try to solve the wordle
            guess = random.choices(self.remaining_words, k=1)[0]
        self.process_guess(guess)
    
    def process_guess(self, my_guess):
        print(my_guess)
        self.remaining_words = self.remaining_words[~(self.remaining_words == my_guess)]
        print(1)
        self.misses, self.matches, self.exact_matches, self.inexact_matches = word_match(my_guess, self.todays_word)
        print(2)
        self.all_misses.update(self.misses)
        # Reduce the remaining words based on the match results
        print(3)
        self.remaining_words  = refine_list(self.misses, self.matches, self.exact_matches, self.inexact_matches, self.remaining_words)


'''
Start Code here
'''
wordle = play_wordle()
todays_word = wordle.get_a_word(today=True)
wordle.make_a_guess()



# Make another guess
guess = get_words(remaining_words)[0]
remaining_words = remaining_words[~(remaining_words == guess)]
misses, matches, exact_matches, inexact_matches = word_match(guess, todays_word)
all_misses.update(misses)
remaining_words  = refine_list(misses, matches, exact_matches, inexact_matches, remaining_words)
