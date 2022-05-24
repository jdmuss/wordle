from datetime import datetime, timedelta

with open('wordle_words.txt', 'r') as in_file:
   words = [w.strip() for w in in_file]

today = datetime.today()
todays_word = 'elder'
wordle_start = today - timedelta(days=words.index(todays_word))

