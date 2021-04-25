import re

#TODO account for string with a space before or after the move
#e.g. "pawn c4"
# "qc2 is theory"
# "B×d3?"
# "Qe3 check then Qh6"
# "Rf4 Rd3"
# ND1
# Nf5+
# H4

PATTERN = re.compile('^([Oo0](-[Oo0]){1,2}|[KkQqRrBbNn]?[a-h]?[1-8]?x?[a-h][1-8](\=[QRBN])?[+#]?){1}$')

def detect_move(move):
  # check for "Go Nb5"
    move = move.replace('x','')
    move = move.replace('#','')
    move = move.replace('+','')
    move = move.replace('?','')
    move = move.replace('!','')
    move = move.replace('.','')

    matches = PATTERN.findall(move)
    if len(matches) == 0:
        return None
    #print('found move')
    #print(matches)
    return matches[0][0].lower()


