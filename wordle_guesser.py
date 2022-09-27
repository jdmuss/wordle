"""
wordle_guesser.py

Description:
    This code explores various software-based solutions of Wordle.

Creation Date: 05-01-2022?
Last Modified: 09-27-2022

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
    1) Finish the doc strings.
    2) Make a stats generation function?
    3) Make a plotting function.
    4) Make a graphical solver.
"""
from collections import Counter
from copy import copy
from datetime import datetime
import random
import numpy as np
import re
#-----------------------------------------------------
# Base classes:
#-----------------------------------------------------
class solver_template(object):
    """
    This solver template loads the target word and the word list. The 'make_a_guess' function is stubbed
    out to accept a guess, and print messages if the 'verbose' parameter is set to true.

    Parameters
    ----------
    target_word: str
        the word that the solver is trying to guess.
    word_list: list
       the list of words from which to draw. Wordle uses a list of 14,855 five letter words by default.
    """
    def __init__(self, target_word, word_list):
        self.target_word = target_word
        self.words = copy(word_list)
    
    def make_a_guess(self, guess=None, verbose=False):
        """
        This is the stubbed function to accept a guess, and print messages if the 'verbose' parameter is set to true.

        Parameters
        ----------
        guess: str
            if specified, a single guess for the solver (default=None, i.e. let the solver make it's own guess).
        verbose: bool
            a directive of whether or not to print messages to the console.

        Returns
        ----------
        guess
            the guess made by the solver (or provided to the solver)
        """
        return guess


class play_wordle():
    wordle_start_date = datetime(2021, 6, 19)
    def __init__(self, source_list='wordle_words.txt'):
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
            self.todays_word = self.words[idx_today]
        elif random:
            self.todays_word = self.words[random.range(len(self.words))]
        else:
            self.todays_word = self.words[idx]
        return self.todays_word
#-----------------------------------------------------
# Base functions:
#-----------------------------------------------------
def get_words(word_list, n=1):
    """ This will get a random sample of n words from a word list (array)."""
    return random.choices(word_list, k=n)


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


def word_match(guess, target):
    """
    This function compares a guessed word against a target word and returns information about which
    letters in the guess missed and matched letters in the target.

    Parameters
    ----------
    guess: str
        the solver's guess at the wordle word
    target: str
       the wordle word that the solver is trying to find

    Returns
    ----------
    misses:set
        a list of letters that were in the guessed word, but not in the target word
    exact_matches:list
        a list of letters that were in both the guessed and target words, and in the same place
    inexact_matches:list
        a list of letters that were in both the guessed and target words, but not in the same place
    """
    misses = set(guess).difference(target)
    matches = set(guess).intersection(target)
    exact_matches = [(letter, idx) for idx, letter in enumerate(guess) if letter == target[idx]]
    inexact_matches, _ = zip(*exact_matches) if exact_matches else (set(), None)
    inexact_matches = matches.difference(inexact_matches)
    inexact_matches = [(l, guess.index(l)) for l in inexact_matches]
    return misses, exact_matches, inexact_matches


def solve_wordle(solver_class, seed=None, today=True, idx=None, random=False, verbose=False):
    wordle = play_wordle()
    word = wordle.get_a_word(today=today, idx=idx, random=random)
    solver = solver_class(word, wordle.words)
    if seed:
        guesses = 1
        solver.make_a_guess(seed, verbose=verbose)
    else:
        guesses = 0
        solver.make_a_guess(verbose=verbose)
    while solver.remaining_words.size > 0:
        solver.make_a_guess(verbose=verbose)
        guesses += 1
    return guesses
#-----------------------------------------------------
# Solver classes:
#-----------------------------------------------------
class simple_solver(solver_template):
    def __init__(self):
        super(simple_solver, self).__init()
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


'''
Start Code here
'''
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


