from collections import defaultdict, deque
from random import choice as randchoice



def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def parse_file(prgsnlen : int, file : open) -> {(str):[str]}:
    pattern_dict = defaultdict(set)
    gen = word_at_a_time(file)
    
    # Build initial list
    current_phrase = deque((next(gen) for x in range(prgsnlen)) , maxlen = prgsnlen)
    
    for chord in gen:

        pattern_dict[tuple(current_phrase)].add(chord)

        current_phrase.popleft()
        current_phrase.append(chord)

    return pattern_dict
            


def patt_as_str(pattern_dict : {(str):[str]}) -> str:
    
    word_lens = tuple(len(ls) for ls in pattern_dict.values())
    
    return ''.join("  " + str(phrase) + " can be followed by any of " + str(pattern_dict[phrase]) + '\n' for phrase in sorted(pattern_dict)) + "max/min list lengths = " + str(max(word_lens)) + '/' + str(min(word_lens)) + '\n'


def produce_text(pattern_dict : {(str):[str]}, start : [str], count : int) -> [str]:
    words = start[:]
    try:
        for x in range(count):

            words.append( randchoicechoice(pattern_dict[  tuple(words[-len(start):])  ]  ))
            
    except KeyError:
        words.append(None)

    return words
        

def input_chord( message , legal = lambda x: True):
    while True:
        g = input(message + ": ")
        if legal(g):
            return g
        print(f"'{g}' is not a legal chord.")

def input_int( message , legal = lambda x: True):
    while True:
        g = input(message + ": ")
        try:
            f = int(g)
            if legal(f):
                return f

        except ValueError:
            print(f"'{g}' is not a legal integer.")
        
if __name__ == '__main__':
    # Write script here
    

    with open(input("Select the file name to read: "), 'r') as the_file:
        prgsnlen = input_int("Select weight of progression", legal = (lambda x: x > 0))
        pattern_dict = parse_file(prgsnlen, the_file)
    print("Possible Proggressions\n" + patt_as_str(pattern_dict) + "\nSelect", prgsnlen, "words for start of list")

    starter = [input(f"Select word {x + 1}" , 
        is_legal = (lambda chd: any(chd in chdprog for chdprog in pattern_dict)))
        for x in range(prgsnlen)]
    
    words_len = input_int("Choose # of words for appending to list", legal = (lambda x: x > 0))
    print("Random text =", produce_text(pattern_dict, starter, words_len))
    



