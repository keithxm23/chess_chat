from move_parser import detect_move


def test_move(in_txt, expected_move):
    parsed = detect_move(in_txt)
    result = parsed == expected_move
    if result:
        print('T')
    else:
        print('F')
        print(parsed, expected_move)



test_move('Ke2','ke2')
test_move('c4','c4')
test_move('Bxd3','bd3')
test_move('B×d3','bd3')
test_move('ND1','nd1')
test_move('Nf5+','nf5')
test_move('H4','h4')



#TODO account for string with a space before or after the move
#e.g. "pawn c4"
# "qc2 is theory"
# "B×d3?"
# "Qe3 check then Qh6"
# "Rf4 Rd3"
# Nf5+
# H4
