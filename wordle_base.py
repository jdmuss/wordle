"""
wordle_base.py

Description:
    This code is the base code against which to try various software-based solutions of Wordle.

Creation Date: 05-01-2022
Last Modified: 09-27-2022

Version: 1.0.2

Dependencies:
    Public: numpy
    Standard: copy, datetime, random
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
from copy import copy
from datetime import datetime
import random
import numpy as np
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
