import re

import re
# adding import alias recommended
bad_patterns = r"sex*| porn*|fuck*|-ass*|ass|shit|damn*|ass|asse*|cock*|whor*|nigg*|slut*|blowjob|fagg*|boob|boob*| bitch*| bastard*| ho |hoe|breast*|jugs| cunt*| puss*| dick*| naked| nud*| masterb*|mastu|nipple*|penis|penal|peni*|god|jesus|christ|bible|church|religion|pray|praye|faith|lord|allah|muslim|islam|allah|ejaculate|jew*|islamic|atheist|rapist*|rape*|pedo*|atheism|atheists|atheist|atheists|christian|christianity|christians|christian|christians|gay|tit*|titt*|islamic|atheist|atheism|atheists|atheist|atheists|christian|christianity|christians|christian|christians|yahwey|yeshua|israel*|sex*| porn*|fuck*|-ass*|ass|shit|slut*|blowjob|fagg*|boob|boob*| breast*|jugs| cunt*| puss*| dick*| naked| nud*| nipple*|penis|penal|peni*|islamic|atheist|atheism|atheists|atheist|atheists|christian|christianity|christians|christian|christians|gay|tit*|titt*| fellatio| fuck| nigg*|lynch|erotic*|genit*|balls|nipples"

replacements = {
    'sex*': 'affection',
    'porn*': 'adult entertainment',
    'fuck*': 'intercourse',
    '-ass*': 'rear end',
    'ass': 'rear end',
    'shit': 'feces',
    'damn*': 'darn',
    'ass|asse*': 'rear end',
    'cock*': 'male bird',
    'whor*': 'prostitute',
    'nigg*': 'racial slur',
    'slut*': 'promiscuous person',
    'blowjob': 'oral sex',
    'fagg*': 'homosexual',
    'boob|boob*': 'breast',
    'bitch*': 'mean woman',
    'bastard*': 'illegitimate child',
    'ho |hoe': 'prostitute',
    'breast*|jugs': 'chest',
    'cunt*': 'vulva',
    'puss*': 'vagina',
    'dick*': 'penis',
    'naked': 'unclothed',
    'nud*': 'unclothed',
    'masterb*': 'self-gratification',
    'mastu': 'self-gratification',
    'god':'deity',
    'jesus':'religious figure',
    'christ':'religious figure',
    'bible':'religious text',
    'church':'place of worship',
    'religion':'set of beliefs',
    'pray':'to communicate with a deity',
    'prayer':'a conversation with a deity',
    'faith':'belief',
    'lord':'captain',
    'allah':'a diety',
    'gay':'homosexual',
    'rapist*|rape*': 'sexual assault',
    'pedo*': 'child sexual abuse(r)',
    'yahwey':'a deity',
    'yeshua':'a religious figure'
}


# replace the

def check_for_badwords(definition, bad_patterns):
    # define a dictionary of replacements for the bad words





pattern = r'word*|the second|kite'

# to make the game more fun we can replace words with less inflamatory ones.


def check_for_badwords(definition, bad_patterns):
    definition = definition.lower()
    # if any of the buzzwords are found return true else false


    return


def check_for_good_patterns(definition, title):
    # check both title and definition for good patterns
    good_patterns = [r'\b\w+phobia\.?\b', r'\bslang\b', r'\bacronymn\b', r'\bmeme\b']


    if any(re.match(r'\b' + word + r'\b', definition) for word in good_patterns):
        print(f'Found a good pattern in the definition: {definition}')
        return True
    elif any(re.match(r'\b' + word + r'\b', title) for word in good_patterns):
        print(f'Found a good pattern in the title: {title}')
        return True
    else:
        return False
