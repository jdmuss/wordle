from collections import Counter
from datetime import datetime
import random
import numpy as np
import re

def get_words(word_list, n=1):
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
    return misses, matches, exact_matches, inexact_matches


def refine_list(misses, exact_matches, inexact_matches, word_list):
    # Remove words that contain letters not in the guess
    new_list = [word for word in word_list if misses.isdisjoint(word)]
    # Only keep words with exact matches in the guess
    if exact_matches:
        new_list = get_exact_matches(exact_matches, new_list)
    # Only keep words with inexact matches in the guess, but not in the missed position
    if inexact_matches:
        new_list = get_inexact_matches(inexact_matches, new_list)
    return np.array(new_list)


class play_wordle():
    wordle_start_date = datetime(2021, 6, 1)
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
            idx_today = (datetime.today() - self.wordle_start_date).days + 1
            self.todays_word = self.words[idx_today]
        elif random:
            self.todays_word = self.words[random.range(len(self.words))]
        else:
            self.todays_word = self.words[idx]
        return self.todays_word
    
    def make_a_guess(self, guess=None):
        if not guess:
            # Let the computer try to solve the wordle
            guess = random.choices(self.remaining_words, k=1)[0]
        self.process_guess(guess)
    
    def process_guess(self, my_guess, supress=True):
        self.remaining_words = self.remaining_words[~(self.remaining_words == my_guess)]
        self.misses, self.matches, self.exact_matches, self.inexact_matches = word_match(my_guess, self.todays_word)
        self.all_misses.update(self.misses)
        # Reduce the remaining words based on the match results
        self.remaining_words  = refine_list(self.misses, self.exact_matches, self.inexact_matches, self.remaining_words)
        if not supress:
            print(my_guess)
            if self.remaining_words.size == 0:
                print(f"Your word {my_guess} was today's word. You win!")
            else:
                print(f"Keep guessing, the pool still contains {self.remaining_words.size:,} words.")


'''
Start Code here
'''
def solve_wordle(seed=None, today=True):
    wordle = play_wordle()
    wordle.get_a_word(today=today)
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
solver_dist = [solve_wordle() for i in range(1000)]
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