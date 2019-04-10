from pathlib     import Path
from collections import defaultdict
from _reader     import parse_file, update_dict
from _patterner  import patt_as_str, generate_prgsn
from _inputter   import input_int


if __name__ == '__main__':
   
    pattern_dict = defaultdict(set)
    
    weight = input_int("Select weight of progression", legal = (lambda x: x > 0))

    print("Parsing the files...\n")

    update_dict( pattern_dict , weight )    

    print("Possible Progressions\n" + patt_as_str(pattern_dict))


    words_len = input_int("Choose number of chords in the progression", legal = (lambda x: x >= weight))

    print("Generating progression...\n")

    try:
        the_progression, lol = generate_prgsn(pattern_dict, weight, words_len, True)
    except IndexError:
        the_progression, lol  = None, None
    
    k = open('yeet', 'w')

    print("Random progression =")
    for y in lol:
        k.write(str(y) + '\n')

    print('yuh')
    k.close()
    



