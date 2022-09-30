"""
simple_solver.py

Description:
    This is s "simple" brute-force Wordle solver.

Creation Date: 05-01-2022
Last Modified: 09-29-2022

Version: 1.0.2

Dependencies:
    Public: numpy
    Standard: collections, datetime, random, re
    Private: wordle_base

How to use:
    ToDo

Changes:
    xx-xx-2022

ToDo:
"""
from collections import Counter
from datetime import datetime
import random
import numpy as np
import re

from wordle_base import play_wordle, solver_template, solve_wordle, word_match
#-----------------------------------------------------
# Base functions:
#-----------------------------------------------------
def get_matches(match_str, word):
    return set([(m.group(), m.start()) for m in re.finditer(match_str, word)])


def get_exact_matches(exact_matches, word_list):
    regex_match = f"[{''.join(l for l, _ in exact_matches)}]"
    return [word for word in word_list if get_matches(regex_match, word).issuperset(exact_matches)]


def get_inexact_matches(inexact_matches, word_list):
    tmp_list = word_list
    for match in inexact_matches:
        regex_match = f"[{match[0]}]"
        tmp_list =[word for word in tmp_list if get_matches(regex_match, word) != [match]]
    return tmp_list
#-----------------------------------------------------
# Solver classe:
#-----------------------------------------------------
class simple_solver(solver_template):
    def __init__(self, *args, **kw):
        super(simple_solver, self).__init__(*args, **kw)
        self.remaining_words = np.array(self.words)
        self.all_misses = set()
    
    def make_a_guess(self, guess=None, verbose=True):
        if not guess:
            # Let the computer try to solve the wordle
            guess = random.choices(self.remaining_words, k=1)[0]
        self.process_guess(guess, verbose)
        return guess
    
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


if __name__ == 'main':
    solver_dist = [solve_wordle(simple_solver, today=True, idx=None, random=False) for i in range(1000)]
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
