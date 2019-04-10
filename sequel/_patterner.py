from collections import defaultdict, deque
from random import choice as randchoice
from _inputter import input_chord, input_int



def chord_gen(file : open):
    '''Generator that yields each chord in a file.'''

    for line in file:
        for item in line.split(','):
            yield frozenset(item.strip()[1:-1].split(';'))


def parse_file(pattern_dict: defaultdict , weight : int, the_file : open) -> {(str):[str]}:
    '''Reads a given file and generates a dictionary mapping partial progressions to possible chords.'''
    
    gen = chord_gen(the_file)
    
    current_phrase = deque((next(gen) for x in range(weight)) , maxlen = weight)
    
    for chord in gen:

        pattern_dict[tuple(current_phrase)].add(chord)

        current_phrase.popleft()
        current_phrase.append(chord)

            


def patt_as_str(pattern_dict : {(str):[str]}) -> str:
    
    prgsn_lens = tuple(len(ls) for ls in pattern_dict.values())
    
    return ''.join("  " + '[' + ', '.join(str(set(chd)) for chd in phrase) + "] precedes by any of [" + ', '.join(str(set(nex)) for nex in pattern_dict[phrase]) + ']\n' for phrase in pattern_dict)



def generate_prgsn(pattern_dict: {(str):[str]}, weight: int, total_len: int , curl: bool = False) -> [str]:
    '''Generates and returns list of chord progressions; with option to continue if next chord isn't found.'''
    
    prgsn = list(randchoice(tuple(pattern_dict.keys())))
   
    c = 0

    while c < total_len:
        try:
            prgsn.append( randchoice(tuple(pattern_dict[  tuple(prgsn[-weight:])  ]  )))
            c += 1
            
        except IndexError:
            if curl:
                prgsn.extend(  randchoice( tuple( pattern_dict.keys() ) )  )
                c += weight 
            else:
                prgsn.append(None)
                break

    return [set(chd) for chd in prgsn]


