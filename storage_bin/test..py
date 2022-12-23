import re


# remove duplicates from this list
bad_patterns = [r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'bitch*', r'bastard*',' ho |hoe',r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'masterb*',r'mastu',r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','ejaculate','jew*','islamic','atheist',r'rapist*|rape*',r'pedo*','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','yahwey','yeshua',r'israel*',r'sex*', r'porn*',r'fuck*',r'-ass*','ass','shit',r'damn*',r'ass|asse*',r'cock*',r'whor*',r'nigg*',r'slut*','blowjob',r'fagg*',r'boob|boob*', r'breast*|jugs', r'cunt*', r'puss*', r'dick*', 'naked', r'nud*', r'nipple*',r'penis|penal|peni*','god','jesus','christ','bible','church','religion','pray','prayer','faith','lord','allah','muslim','islam','allah','islamic','atheist','atheism','atheists','atheist','atheists','christian','christianity','christians','christian','christians','gay',r'tit*|titt*', 'fellatio', 'fuck', 'nigger','lynch']

# bad patterns with no dupes
unique = [] # init
unique = [word for word in bad_patterns if word not in unique]
