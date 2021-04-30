import re


PATTERN = re.compile('^([Oo0](-[Oo0]){1,2}|[KkQqRrBbNn]?[a-h]?[1-8]?x?[a-h][1-8](\=[QRBN])?[+#]?){1}$')

def detect_move(move):
  # check for "Go Nb5"
    move = move.lower()
    move = move.strip()
    move = move.replace('x','')
    move = move.replace('0','o')
    move = move.replace('×','')
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


