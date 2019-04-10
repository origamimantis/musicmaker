from pathlib     import Path
from collections import defaultdict
from _patterner  import parse_file, patt_as_str, generate_prgsn
from _inputter   import input_int

if __name__ == '__main__':
   
    pattern_dict = defaultdict(set)
    
    weight = input_int("Select weight of progression", legal = (lambda x: x > 0))

    print("Parsing the files...\n")
    
    for progfile in Path("files").iterdir():

        with open(progfile, 'r') as the_file:
            try:
                parse_file( pattern_dict, weight, the_file)
            except RuntimeError:
                pass

    print("Possible Progressions\n" + patt_as_str(pattern_dict))


    words_len = input_int("Choose # of words for appending to list", legal = (lambda x: x > 0))

    print("Generating progression...\n")
    curl = True
    try:
        the_progression = generate_prgsn(pattern_dict, weight, words_len, True)
    except IndexError:
        the_progression = None
    print("Random progression =", the_progression)
    



