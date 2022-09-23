"""
wordle_guesser.py

Description:
    This code explores various software-based solutions of Wordle.

Creation Date: 05-01-2022?
Last Modified: 09-02-2022

Version: 1.0.2

Dependencies:
    Public: numpy
    Standard: collections, copy, datetime, random, re
    Private: 

How to use:
    ToDo

Changes:
    xx-xx-2022

ToDo:
    Pull the solver code out and let the play_wordle class accept any solver, and have it generate stats.
"""
from collections import Counter
from copy import copy
from datetime import datetime
import random
import numpy as np
import re

def get_words(word_list, n=1):
    """ This will get a random sample of n words from a word list (array)."""
    return random.choices(word_list, k=n)


def get_matches(match_str, word):
    return sorted([(m.group(), m.start()) for m in re.finditer(match_str, word)])


def get_exact_matches(exact_matches, word_list):
    regex_match = f"[{''.join(l for l, _ in exact_matches)}]"
    return [word for word in word_list if get_matches(regex_match, word) == sorted(exact_matches)]


def get_inexact_matches(inexact_matches, word_list):
    tmp_list = word_list
    for match in inexact_matches:
        regex_match = f"[{match[0]}]"
        tmp_list =[word for word in tmp_list if get_matches(regex_match, word) != [match]]
    return tmp_list


def word_match(guess, word):
    misses = set(guess).difference(word)
    matches = set(guess).intersection(word)
    exact_matches = [(l, guess.index(l)) for l in matches if guess.index(l) == word.index(l)]
    inexact_matches, _ = zip(*exact_matches) if exact_matches else (set(), None)
    inexact_matches = matches.difference(inexact_matches)
    inexact_matches = [(l, guess.index(l)) for l in inexact_matches]
    return misses, exact_matches, inexact_matches


class play_wordle():
    wordle_start_date = datetime(2021, 6, 3)
    def __init__(self, source_list='wordle_words_unsorted.txt'):
        self.wordle_dict = source_list
        self.reset_wordle(read_word_list=True)
        self.solver = None
    
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
            idx_today = (datetime.today() - self.wordle_start_date).days + 1
            self.todays_word = self.words[idx_today]
        elif random:
            self.todays_word = self.words[random.range(len(self.words))]
        else:
            self.todays_word = self.words[idx]
        return self.todays_word
    
    def make_a_guess(self, guess=None):
        # Enter new code, or get rid of this
        pass
        
    def process_guess(self, my_guess, supress=True):
        # Enter new code, or get rid of this
        pass
    
    def solve_wordle(self, seed=None, today=True, idx=None, random=False):
        # Fix this, or put it in the solver template
        if self.solver:
            word = self.get_a_word(today=today, idx=idx, random=random)
            if seed:
                guesses = 1
                self.solver.make_a_guess(seed)
            else:
                guesses = 0
                self.solver.make_a_guess()
            while self.solver.remaining_words.size > 0:
                self.solver.make_a_guess()
                guesses += 1
            return guesses
        else:
            print("Error: please load a solver model before runing the solver method.")


class simple_solver():
    def __init__(self, target_word, word_list):
        self.target_word = target_word
        self.words = copy(word_list)
        self.remaining_words = np.array(self.words)
        self.all_misses = set()
    
    def make_a_guess(self, guess=None, verbose=True):
        if not guess:
            # Let the computer try to solve the wordle
            guess = random.choices(self.remaining_words, k=1)[0]
        self.process_guess(guess, verbose)
    
    def refine_list(self, misses, exact_matches, inexact_matches):
        # Remove words that contain letters not in the guess
        new_list = [word for word in self.remaining_words if misses.isdisjoint(word)]
        # Only keep words with exact matches in the guess
        if exact_matches:
            new_list = get_exact_matches(exact_matches, new_list)
        # Only keep words with inexact matches in the guess, but not in the missed position
        if inexact_matches:
            new_list = get_inexact_matches(inexact_matches, new_list)
        self.remaining_words = np.array(new_list)

    def process_guess(self, my_guess, verbose=True):
        self.remaining_words = self.remaining_words[~(self.remaining_words == my_guess)]
        misses, exact_matches, inexact_matches = word_match(my_guess, self.target_word)
        self.all_misses.update(misses)
        # Reduce the remaining words based on the match results
        self.refine_list(misses, exact_matches, inexact_matches)
        if verbose:
            print(my_guess)
            if self.remaining_words.size == 0:
                print(f"Your word {my_guess} was today's word. You win!")
            else:
                print(f"Keep guessing, the pool still contains {self.remaining_words.size:,} words.")


'''
Start Code here
'''
def solve_wordle(seed=None, today=True, idx=None, random=False):
    wordle = play_wordle()
    wordle.get_a_word(today=today, idx=idx, random=random)
    if seed:
        guesses = 1
        wordle.make_a_guess(seed)
    else:
        guesses = 0
        wordle.make_a_guess()
    while wordle.remaining_words.size > 0:
        wordle.make_a_guess()
        guesses += 1
    return guesses


def remove_old_solver(seed=None, today=True, idx=None, random=False):
    wordle_start_date = datetime(2021, 6, 1)
    today_idx = (datetime.today() - wordle_start_date).days + 1
    wordle = play_wordle()
    wordle.words = wordle.words[today_idx:]
    if today:
        idx = 0
        today = False    
    wordle.get_a_word(today=today, idx=idx, random=random)
    if seed:
        guesses = 1
        wordle.make_a_guess(seed)
    else:
        guesses = 0
        wordle.make_a_guess()
    while wordle.remaining_words.size > 0:
        wordle.make_a_guess()
        guesses += 1
    return guesses

"""# todays_word = wordle.get_a_word(today=today)"""
# Prize --> idx = 457
solver_dist = [solve_wordle(seed='prize', today=True, idx=None, random=False) for i in range(1000)]
print("-"*40)
print("Simple Solver stats:")
print(f"Fastest: {min(solver_dist)} guesses")
print(f"Slowest: {max(solver_dist)} guesses")
print(f"Mean: {np.mean(solver_dist)} guesses")
print("-"*10)
print("Solution frequencies:")
print("guesses\tcounts")
for k, c in sorted(Counter(solver_dist).items()):
    print(f"{k}\t{c} times")
print("-"*40)

# Only new words in the draw:
solver_dist = [remove_old_solver(seed=None, today=True, idx=None, random=False) for i in range(1000)]
print("-"*40)
print("Simple Solver stats:")
print(f"Fastest: {min(solver_dist)} guesses")
print(f"Slowest: {max(solver_dist)} guesses")
print(f"Mean: {np.mean(solver_dist)} guesses")
print("-"*10)
print("Solution frequencies:")
print("guesses\tcounts")
for k, c in sorted(Counter(solver_dist).items()):
    print(f"{k}\t{c} times")
print("-"*40)


