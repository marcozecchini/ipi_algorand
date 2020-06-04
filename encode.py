import base64
import json 

rights = {
    "PR": 'PERFORMING RIGHT',
    "MP": 'MOTION PICTURE EXHIBITION RIGHT',
    "PT": 'THEATRICAL PERFORMING RIGHT',
    "MA": 'MECHANICAL RIGHT RADIO',
    "TB": 'TELEVISION BROADCAST RIGHT',
    "MT": 'MECHANICAL RIGHT TV',
    "OD": 'MAKING AVAILABLE RIGHT-INTERACTIVE',
    "OB": 'MAKING AVAILABLE RIGHT-NON INTERACTIVE',
    "RT": 'RETRANSMISSION RIGHT',
    "TP": 'RIGHT OF RETRANSMISSION OF PERFORMANCE',
    "TO": 'RIGHT OF PUBLIC PERFORMANCE OF RADIO BROADCAST',
    "TV": 'RIGHT OF PUBLIC PERFORMANCE OF TV BROADCAST',
    "PC": 'RIGHT OF PUBLIC PERFORMANCE OF A RECORDING',
    "MR": 'MECHANICAL RIGHT SOUND CARRIER',
    "MV": 'MECHANICAL RIGHT VIDEO',
    "MD": 'MECHANICAL RIGHT-INTERACTIVE',
    "MB": 'MECHANICAL RIGHT-NON INTERACTIVE',
    "RP": 'REPRODUCTION RIGHT',
    "SY": 'SYNCHRONISATION RIGHT',
    "DB": 'DATABASE RIGHT',
    "BT": 'BLANK TAPE REMUNERATION',
    "RB": 'REPROGRAPHY REMUNERATION',
    "RL": 'RENTAL AND LENDING RIGHT',
    "RR": 'RESALE RIGHT (DROIT DE SUITE)',
    "ER": 'EDUCATIONAL RIGHT'
}
rights_list = list(rights.keys())

cclasses = {
    "MW": 'MUSICAL WORK',
    "DM": 'DRAMATICO-MUSICAL WORK',
    "LW": 'LITERARY WORK',
    "LF": 'LITERARY FICTION WORK',
    "LN": 'LITERARY NON FICTION WORK',
    "DW": 'DRAMATIC WORK',
    "CW": 'CHOREOGRAPHIC WORK',
    "AV": 'AUDIO-VISUAL WORK',
    "AF": 'FICTION AUDIO-VISUAL WORK',
    "AD": 'DOCUMENTARY AUDIO-VISUAL WORK',
    "MM": 'MULTIMEDIA WORK',
    "IS": 'INFORMATION SYSTEM',
    "WA": 'WORK OF ART',
    "PH": 'PHOTOGRAPHIC WORK',
    "AC": 'ARCHITECTURAL WORK'
}
cclasses_list = list(cclasses.keys())


roles = {
    "AG": 'GRAPHIC DESIGNER',
    "AS": 'AUTHOR OF SCREENPLAY/AUTHOR OF DIALOGUE',
    "AT": 'ARCHITECT',
    "CP": 'AUTHOR COMPUTER GRAPHIC',
    "CT": 'CARTOONIST',
    "DG": 'DESIGNER',
    "DS": 'AUTHOR OF SUBTITLES/DUBBING',
    "DW": 'DRAWER,GRAPHIC ARTIST',
    "FA": 'AUTHOR OF FINE ART',
    "JO": 'JOURNALIST',
    "LY": 'LYRICIST/LIBRETTIST',
    "MC": 'MUSICAL CREATOR (COMPOSER)',
    "PH": 'PHOTOGRAPHER',
    "PW": 'PLAYWRIGHT',
    "RE": 'FILM DIRECTOR',
    "WP": 'AUTHOR/POET',
    "EB": 'BOOK PUBLISHER',
    "EM": 'MUSIC PUBLISHER',
    "EP": 'NEWSPAPER PUBLISHER',
    "AP": 'ANALYST/PROGRAMMER',
    "CD": 'COSTUME-DESIGNER',
    "CG": 'CHOREOGRAPHER',
    "CM": 'DIRECTOR OF PHOTOGRAPHY/CINEMATOGRAPH',
    "DA": 'DATA ARCHITECT',
    "DD": 'DUBBING DIRECTOR',
    "EJ": 'JOURNAL/PERIODICAL/MAGAZINE PUBLISHER',
    "ET": 'FILM EDITOR',
    "FD": 'FILM DISTRIBUTOR',
    "MD": 'MULTIMEDIA DIRECTOR',
    "MS": 'STAGE DIRECTOR',
    "PC": 'PRODUCER',
    "PD": 'PRODUCTION DESIGNER (SET-DESIGNER)',
    "PR": 'PRESS AGENCY',
    "ST": 'SOUND ENGINEER'
}
roles_list = list(roles.keys())

country = ''
with open('country2.json') as json_file:
    country = json.load(json_file)

country_list = list(country.keys())


codes = list(range(ord('A'), ord('Z')+1))
codes += list(range(ord('a'), ord('z')+1))
codes += list(range(ord('0'), ord('9')+1))
codes.extend((ord('+'), ord('/')))

remap = dict(zip(range(64), codes))
backmap = dict(zip(codes, range(64)))

def countrytobits(country_list, selected_list):
    result = []
    res_string = ""
    for i in range(0, len(country_list)):
        result.append(int(country_list[i]  in selected_list))
        res_string += str(int(country_list[i] in selected_list))

    return result

def frombits(bits, length=8):
    chars = []
    for b in range(int(len(bits) / length)):
        byte = bits[b*length:(b+1)*length]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def frombitsto64(bits, length=6):
    chars = []

    for b in range(int(len(bits) / length)):
        byte = bits[b*length:(b+1)*length]
        chars.append(chr(remap[int(''.join([str(bit) for bit in byte]), 2)]))
    return ''.join(chars)


def countrytovector(country_list, selected_list):
    vector = countrytobits(country_list, selected_list)
    message_bytes = frombitsto64(vector,6)
    return message_bytes

def vectortocountry(country_lists, vector):
    bin_vec = ''
    result = ''
    for c in vector:
        temp = bin(backmap[ord(c)])[2:]
        for _ in range(len(temp), 6):
            bin_vec += '0'
        for i in range(0, len(temp)):
            bin_vec += temp[i]
    
    for i in range(0, len(bin_vec)):
        if bin_vec[i] == '1':
            result += country_list[i]+","
    return result[:len(result)-1]
