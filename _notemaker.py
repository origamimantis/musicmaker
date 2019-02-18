import random
from collections import namedtuple


FLAT  = -1
SHARP =  1

SCALEFILE = 'scales.txt'


NOTEVAL = {'Cb': (11,   1)  ,  'C' : ( 0,  -1)  ,  'C#': ( 1,   1),    # maps a given note to a starting value
           'Db': ( 1,  -1)  ,  'D' : ( 2,   1)  ,  'D#': ( 3,  -1),    # and accidental type ex Eb generally uses flats.
           'Eb': ( 3,  -1)  ,  'E' : ( 4,   1)  ,  'E#': ( 5,  -1),
           'Fb': ( 4,   1)  ,  'F' : ( 5,  -1)  ,  'F#': ( 6,   1),
           'Gb': ( 6,  -1)  ,  'G' : ( 7,   1)  ,  'G#': ( 8,  -1),
           'Ab': ( 8,  -1)  ,  'A' : ( 9,   1)  ,  'A#': (10,  -1),
           'Bb': (10,  -1)  ,  'B' : (11,   1)  ,  'B#': ( 0,  -1)}



RELNOTE = { 0 :  (  ('C', 0),('B', 1),(' ',-1)  ),   # C/B# ---- of the form natural enharm, sharp enharm, flat enharm.
            1 :  (  (' ', 0),('C', 1),('D',-1)  ),   # C#/Db
            2 :  (  ('D', 0),(' ', 1),(' ',-1)  ),   # D
            3 :  (  (' ', 0),('D', 1),('E',-1)  ),   # D#/Eb
            4 :  (  ('E', 0),(' ', 1),('F',-1)  ),   # E/Fb
            5 :  (  ('F', 0),('E', 1),(' ',-1)  ),   # F/E#
            6 :  (  (' ', 0),('F', 1),('G',-1)  ),   # F#/Gb
            7 :  (  ('G', 0),(' ', 1),(' ',-1)  ),   # G
            8 :  (  (' ', 0),('G', 1),('A',-1)  ),   # G#/Ab
            9 :  (  ('A', 0),(' ', 1),(' ',-1)  ),   # A
            10:  (  (' ', 0),('A', 1),('B',-1)  ),   # A#/Bb
            11:  (  ('B', 0),(' ', 1),('C',-1)  )}   # B/Cb

MODENUM = {}
MODESLIST = []

modefile = open(SCALEFILE)
modefilelist = modefile.readlines()
modefile.close()

for line in modefilelist:
    if line.startswith('///'):
        continue
    
    splits = line.strip().split()
    
    notessplits = [int(singlenote) for singlenote in splits[1].split(',')]
    
    MODENUM[splits[0]] = (len(notessplits), tuple(notessplits))
    MODESLIST.append(splits[0])


KEYMAP = { 'minor':9,
           'dorian':10,
           'phrygian':8,
           'lydian':1,
           'mixolydian':11,
           'aeolian':9,
           'locrian':7,
           'malkauns':9}


SYMTRANS = {'b' : FLAT, '#' : SHARP}

WEIGHT = 1

def create_mode(chosen_key, chosen_mode):
    
    l = []
    
    notuple = NOTEVAL[ chosen_key ]

    prefacc = notuple[1]
    
    for step in range( MODENUM[chosen_mode][0] ):
        x = (notuple[0] + MODENUM[chosen_mode][1][step]) % 12
        k = RELNOTE[x][prefacc] if RELNOTE[x][prefacc][0] != ' ' else RELNOTE[x][0]
        l.append(k)
    
    weightyl = l[0]*WEIGHT
    
    l.append(weightyl)
    return l


