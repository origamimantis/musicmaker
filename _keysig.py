import _notemaker


class KeySig():
    '''stores data about the key signature, along with previously used accidentals.'''
    def __init__(self, key:str, mod):
        keysig = {'A':0,
                       'B':0,
                       'C':0,
                       'D':0,
                       'E':0,
                       'F':0,
                       'G':0}
        notelist = ['A','E','B','F#','Db','Ab','Eb','Bb','F','C','G','D']
        key = notelist[ ( notelist.index(key)  +  _notemaker.KEYMAP.get(mod, 0)) % 12 ]
        if key == "C":
            _keylist = [0]

        elif key == "F":
            _keylist = [-1,'B']
        elif key == "Bb":
            _keylist = [-1,'B','E']
        elif key == 'Eb':
            _keylist = [-1,'B','E','A']
        elif key == 'Ab':
            _keylist = [-1,'B','E','A','D']
        elif key == 'Db':
            _keylist = [-1,'B','E','A','D','G']
        elif key == 'Gb':
            _keylist = [-1,'B','E','A','D','G','C']

        elif key == "G":
            _keylist = [1,'F']
        elif key == "D":
            _keylist = [1,'F','C']
        elif key == 'A':
            _keylist = [1,'F','C','G']
        elif key == 'E':
            _keylist = [1,'F','C','G','D']
        elif key == 'B':
            _keylist = [1,'F','C','G','D','A']
        elif key == 'F#':
            _keylist = [1,'F','C','G','D','A','E']

        else:
            return

        for x in _keylist[1:]:
            keysig[x] = _keylist[0]
        
        self.keysig = keysig
        self.fifths = _keylist[0]*(len(_keylist)-1)

