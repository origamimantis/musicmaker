from datetime import date
from _keysig import KeySig

HEADERFILE = '_mxmlhead.txt'
KEYTPFILE = '_mxmlkstp.txt'


NEWLINE = '      </measure>\n    <measure number="" width="244.22">\n      <print new-system="yes">\n        <system-layout>\n          <system-margins>\n            <left-margin>0.00</left-margin>\n            <right-margin>0.00</right-margin>\n            </system-margins>\n          <system-distance>150.00</system-distance>\n          </system-layout>\n        </print>'



def _tupsetup1(title):
    today = date.today()
    
    ts = '    <work-title>%s</work-title>' % title
    ds = '      <encoding-date>%s</encoding-date>' % today
    ms = _get_creds(title)


    return ts,ds,ms,''
    
    
def _tupsetup2(partnum,note,mod,bpm):
    keysig = KeySig(note,mod)
    ps = '  <part id="P%d">' % partnum
    ks = '          <fifths>%s</fifths>' % keysig.fifths
    b1 = '            <per-minute>%s</per-minute>' % bpm
    b2 = '        <sound tempo="%s"/>' % bpm


    return ps,ks,b1,b2,''
   
    
    

def _get_creds(title:str):
    ms = '    <credit-words default-x="595.44" default-y="1626.67" justify="center" valign="top" font-size="24">%s</credit-words>\n' % title
    ms += '    </credit>\n'
    ms += '  <credit page="1">\n'
    ms += '    <credit-words default-x="595.44" default-y="1569.97" justify="center" valign="top" font-size="14">made with musicmaker by EZ</credit-words>'
    return ms



def get_header(title):
    '''I don't have the knowledge to write a musicxml header, so I copied it to a file.
       This function reads that file and returns its contents.'''
    
    setuptuple = _tupsetup1(title)

    header_file = None
    try:
        header_file = open(HEADERFILE)
        file_text = header_file.read()

    finally:
        header_file.close()
    
    text_list = file_text.split('-------------------------------------------------')
    
    header = ""
    for x in range(len(text_list)):
        header += text_list[x] + setuptuple[x]
    return header

def get_part_end():
    l = []
    l.append('      <barline location="right">')
    l.append('        <bar-style>light-heavy</bar-style>')
    l.append('        </barline>')
    l.append('      </measure>')
    l.append('    </part>\n')
    return '\n'.join(l)



def get_part_list(num):
    l = []
    l.append('  <part-list>')
    for x in range(1, num+1):
        l.append('    <score-part id="P%d">' % x)
        l.append('      <part-name>Piano</part-name>')
        l.append('      <part-abbreviation>Pno.</part-abbreviation>')
        l.append('      <score-instrument id="P%d-I1">' % x)
        l.append('        <instrument-name>Piano</instrument-name>')
        l.append('        </score-instrument>')
        l.append('      <midi-device id="P%d-I1" port="1"></midi-device>' % x)
        l.append('      <midi-instrument id="P%d-I1">' % x)
        l.append('        <midi-channel>%d</midi-channel>' % x)
        l.append('        <midi-program>1</midi-program>')
        l.append('        <volume>78.7402</volume>')
        l.append('        <pan>0</pan>')
        l.append('        </midi-instrument>')
        l.append('      </score-part>')
    l.append('    </part-list>\n')
    return '\n'.join(l)

def get_part_begin(partnum,note, mod,bpm):
    setuptuple = _tupsetup2(partnum,note,mod,bpm)

    kstp_file = None
    try:
        kstp_file = open(KEYTPFILE)
        file_text = kstp_file.read()

    finally:
        if kstp_file != None:
            kstp_file.close()

    text_list = file_text.split('-------------------------------------------------')

    kstp = ""

    for x in range(len(text_list)):
        kstp += text_list[x] + setuptuple[x]
    return kstp




def get_closer():
    return '  </score-partwise>'


YDICT = {    'D':-20,      # maps note key to vertical position on bar. top line = 0
             'C':-25,
             'B':-30,
             'E':-15,
             'F':-10,
             'G':-5,
             'A':0}


def construct_note(params, xpos, partnum)->[str]:
    '''constructs xml block for a single note or rest.'''
    temp = []
    if not params.rest:

        temp.append('      <note default-x="%s" default-y="%s">' % (xpos, -100*(partnum-1) + YDICT[params.step]))

        temp.append("        <pitch>")

        temp.append("          <step>%s</step>" % params.step)
        temp.append("          <alter>%s</alter>" % params.alter)
        temp.append("          <octave>%s</octave>" % params.octave)

        temp.append('          </pitch>')
    else:
        temp.append('      <note>')
        temp.append('        <rest/>')

    temp.append("        <duration>%s</duration>" % params.duration)
    temp.append("        <voice>1</voice>")
    temp.append("        <type>%s</type>" % params.type[0])
    if params.type[1]:
        temp.append("        <dot/>")

    temp.append("        <accidental>%s</accidental>" % params.accidental)
    temp.append("        <stem>down</stem>")

    temp.append("        </note>")
    return temp

