with open('wordle_words.csv') as in_file:
   words = in_file.read().strip().replace('"','').split(',')

with open('wordle_words_unsorted.txt', 'w') as out_file:
   print(*words, sep=('\n'), file=out_file)

with open('training_words.txt', 'w') as out_file:
   print(*training, sep=('\n'), file=out_file)
   
with open('test_words.txt', 'w') as out_file:
   print(*test, sep=('\n'), file=out_file)

with open('wordle_words.txt', 'w') as out_file:
   print(*sorted(words), sep=('\n'), file=out_file)
