import random
from collections import namedtuple
from math import ceil, sqrt
from _keysig import KeySig
import _xmlconstruct
import _notemaker

######### to-do: implement 'last accidental', although should work without. just looks weird.
#########        prompt to control octaves, as well as a dictionary containing keys:(octaverange)
#########        since octaves are set in musescore. This should prevent erratic jumping in the music.

NoteTuple = namedtuple('NoteTuple', ['step','alter','octave','duration','type','rest', 'accidental'])




DEFAULT_TITLE =    'my-score'
DEFAULT_MEASURES = '120'
DEFAULT_BPM =      '120'



class score():

    def xdict(note_type):
        return 5         # maps note duration to the amount of space taken up in a bar.
    
    new_line= _xmlconstruct.NEWLINE
    
    def __init__(self, title,num_instr):
        self.header = _xmlconstruct.get_header(title)
        self.closer = _xmlconstruct.get_closer()
        self.parts = _xmlconstruct.get_part_list(num_instr)
        self.notes = []
        self.measlen = 0
        self.xpos = 70.8
      
    def add_meas(self):
        self.notes.append(score.new_line)
        self.xpos = 0

    def add_note(self, params, partnum):
        '''creates a block for one note.'''
        
        self.xpos += score.xdict(params.duration)

        self.notes.append('\n'.join(_xmlconstruct.construct_note(params,self.xpos,partnum)))
    
    def create_instruments(self, num):
        self.instrlist = _xmlconstruct.get_part_list(num)

    def end_part(self):
        self.notes.append(_xmlconstruct.get_part_end())
    def add_part(self, partnum,note,mod,bpm):   ###### add xml text to end/start a new part.
        self.notes.append(_xmlconstruct.get_part_begin(partnum,note,mod, bpm))
        
    def compile(self, filename):
        '''writes the 'song' to a file.'''
        try:
            new_file = open(filename, 'w')
            new_file.write(self.header)
            new_file.write(self.parts)
            new_file.write('\n'.join(self.notes))
            new_file.write(self.closer)
            new_file.flush()
        except:
            print("error occurred.")
        finally:
            new_file.close()



    #step,alter,octave | duration,type




def _get_note():
    
    note = input("Enter key: ").strip()
    while note.lower() == "help" or note not in _notemaker.NOTEVAL.keys():
        if note.lower() == "help":
            _welcome()
        else:
            print("Invalid key.\n")
        note = input("Enter key: ").strip()
    return {'Cb':'B' , 'Fb':'E' , 'Gb':'F#',
            'A#':'Bb', 'B#':'C' , 'C#':'Db',
            'D#':'Eb', 'E#':'F' , 'G#':'Ab'}.get(note,note)

def _get_mod():
    mod = input("Enter scale: ").strip().lower()
    while mod == "help" or mod not in _notemaker.MODESLIST:        
        if mod == "help":
            _welcome()
        else:
            print("Invalid scale.\n")
        mod = input("Enter scale: ").strip().lower()
    
    return mod

def _get_filename():
    filename = ""
    illeg = ['/','\\','$','#','?','%','*',':','|','"',"'",'<','>','.',' ','\t','\n']
    badname = True
    while badname:
        badname = False
        filename = input("Enter filename to save to (without extension): ").strip()
        if filename.lower() == "help":
            _welcome()
            badname = True
            continue
        if not len(filename):
            badname = True
            print("Invalid name.\n")
            continue
        for ch in illeg:
            if ch in filename:
                badname = True
                print("Invalid name.\n")
                break

    return filename


def _get_title():
    title = input(f"Title of piece (default: {DEFAULT_TITLE}): ").strip()
    while title.lower() == "help":
        _welcome()
        title = input(f"Title of piece (default: {DEFAULT_TITLE}): ").strip()

    if title == "":
        title = DEFAULT_TITLE
    return title

def _get_meas():
    notes = input(f'Number of measures (default: {DEFAULT_MEASURES}): ').strip()
    while True:
        if notes.lower() == "help":
            _welcome()
        elif notes == "":
            notes = DEFAULT_MEASURES
            break
        elif not notes.isdigit():
            print("Invalid number.\n")
        else:
            break
        notes = input(f'Number of measures (default: {DEFAULT_MEASURES}): ').strip()
    return notes

def _get_bpm():
    bpm = input(f'Tempo, in quarter note beats per minute (default: {DEFAULT_BPM}): ').strip()
    while True:
        if bpm.lower() == "help":
            _welcome()
        elif bpm == "":
            bpm = DEFAULT_BPM
            break
        elif bpm.isdigit() and int(bpm) != 0:
            return bpm
        print("Invalid number.\n")
        bpm = input(f'Tempo, in quarter note beats per minute (default: {DEFAULT_BPM}): ').strip()
    return bpm

def _get_numparts():
    num = input('Number of parts: ').strip().lower()
    while True:
        if num == 'help':
            _welcome()
            continue
        elif num.isdigit() and int(num) != 0:
            num = int(num)
            return num
        print('Invalid number.\n')
        num = input('Number of parts: ').strip().lower()

def loop():

    # get information about the file to save to / the music in general.
    while True:
        filename = _get_filename()
        title = _get_title()
        num = _get_numparts()
        num_meas = _get_meas()
        bpm = _get_bpm()
        
        score_obj = score(title,num)
        
        redo = ""
        while redo != 'y' and redo != 'n' and redo != 'q':
            _confirmdet(filename, title,num, num_meas, bpm)
            redo = input().strip().lower()
        if redo == 'n':
            print('\nFile initialization cancelled. Re-enter information.\n')
            continue
        elif redo == 'q':
            print('\nMusic creation aborted.')
            print('Program will exit.')
            return
        else:
            break

    # create each part
    for x in range(1,num+1):
        result = create_part(x,num, filename, score_obj, title,bpm,num_meas)
        if result == None:
            return
        print(result)
    score_obj.compile(filename + ".musicxml")
    print(f"\n'{title}' successfully created as {filename}.musicxml in the current directory.")
    print("Program will exit.")


def create_part(partnum, totalparts, filename, score_obj:'score object',title, bpm, num_meas)-> str or None:
    
    _start_part(partnum, totalparts)

    # receive input on how to make the part
    while True: 
        note = _get_note()
        mod = _get_mod()
        redo = ""
        while redo != 'y' and redo != 'n' and redo != 'q':
            _confirm(note,mod, partnum, totalparts)
            redo = input().strip().lower()
        if redo == 'n':
            print('\nPart creation cancelled. Re-enter information.\n')
            continue
        elif redo == 'q':
            print('\nMusic creation aborted.')
            print('Program will exit.')
            return
        else:
            break
    print()

    # actually make the part
    score_obj.add_part(partnum,note, mod, bpm) 
    scale = _notemaker.create_mode(note, mod)
    num_meas = int(num_meas)
    _make_part(note,mod,scale,num_meas, score_obj,partnum)
    
    return f'Part {partnum} successfully created.\n'
# step,alter,octave,duration,type,,rest,accidental


def _make_part(note, mod, scale, num_meas, score_obj,partnum): 
    for meas in range(num_meas):
        count = 0
        while count < 4:
            note_list = _generate_note(note,mod, scale)
            for v in note_list:
                if (count + v.duration) <= 4:

                    score_obj.add_note(v, partnum)
                    count += v.duration
                else:
                    for f in _handle_extras(v,4-count):
                        
                        score_obj.add_note(f,partnum)
                        count += f.duration
                    break
        if meas != num_meas:
            score_obj.add_meas()
    score_obj.end_part()


def _handle_extras(v,time):
    l = []
    for div in [2,1,0.5,0.25]:
        d = time // div
        m = time % div
        if time == div:
            l.append(NoteTuple(v.step,v.alter,v.octave,div,_get_ntype(div),False,v.accidental))
            time = m
    return l

def _generate_note(key:str,mode:str, scale:[(str,int)])-> [NoteTuple]:
    length = [2,1,0.5,0.25]

    rhythms = [(1,),
               (1,1,2),
               (2,1,1),
               (1,2,1),
               (1,1,1,1),
               (3,1)]

    al_ac = {-1:'flat',1:'sharp',0:'natural'}
    
    
    
    rhy = random.choice(rhythms)
    doof = []
    durbase = random.choice(length[ rhy != (1,) :])

    
    for part in rhy:

        step, alter = random.choice(scale)

        is_rest = random.choice([0,0,0,0,0,1])
        octave = random.choice([3,3,3,3,3,3,3,3,3,3,3,4,4])
        dur = part * durbase
        ntype = _get_ntype(dur)
        
        doof.append(NoteTuple(step, alter, octave, dur,ntype,is_rest, al_ac[alter]))
    return doof

def _get_ntype(dur:str, dotted:bool = False)-> str:
    
    if dotted:
        dur /= 1.5
    if   round(dur * 400) == 100:
        ntype = '16th', dotted
    elif round(dur * 200) == 100:
        ntype = 'eighth',dotted
    elif round(dur * 100) == 100:
        ntype = 'quarter',dotted
    elif round(dur *  50) == 100:
        ntype = 'half',dotted
    else:
        ntype = _get_ntype(dur, dotted=True)
    return ntype


def _welcome():
    
    modesplit = 6
    print()
    print('-------------------WELCOME TO MUSICMAKER------------------')
    print()
    print("    Filenames cannot contain the following characters:")
    print("               /\\$#?%*:|\"'.,<> and spaces.")
    print()
    print("    Keys: One letter from 'A','B','C','D','E','F','G'.")
    print("        Optional suffix 'b' (flat) or '#' (sharp).")
    print()
    print('                          Scales:')
    print('  ' + '\n  '.join(   ', '.join(  _notemaker.MODESLIST[ modesplit*x : modesplit*(x+1) ]  )  for x in range( ceil( len(_notemaker.MODESLIST)/modesplit ) )   ) )
    print()
    print("            Type 'help' to reopen this window.")
    print('----------------------------------------------------------')
    print()



def _start_part(partnum, totalparts):
    print()
    print('----------------------------------------------------------')
    print(f'Part {partnum} / {totalparts}:')
    print()


def _confirmdet(fn,t,num, num_meas,bpm):
    print()
    print('--------------------FILE CONFIRMATION-----------------------')
    print(f'      File Name:              {fn}.musicxml')
    print(f'      Title:                  {t}')
    print(f'      Parts:                  {num}')
    print(f'      Length:                 {num_meas} measures')
    print(f'      Tempo (quarter notes):  {bpm} bpm')
    print('----------------------------------------------------------')
    print("'y' to confirm, 'n' to re-enter info, or 'q' to exit program.")


def _confirm(n,m,partnum, totalparts):
    print()
    print('--------------------PART CONFIRMATION---------------------')
    print(f'                    Part:   {partnum} / {totalparts}')
    print(f'                    Key:    {n}')
    print(f'                    Scale:  {m}')
    print('----------------------------------------------------------')
    print("'y' to confirm, 'n' to re-enter info, or 'q' to exit program.")





if __name__ == "__main__":
    _welcome() 
    loop()
