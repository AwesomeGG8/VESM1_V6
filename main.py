board = [['-' for j in range(7)] for i in range(4)]

def is_winner():
    x_win = False
    o_win = False

    for j in range(7):
        column = [board[i][j] for i in range(4)]
        if column == ['X']*4:
            x_win = True
        if column == ['O']*4:
            o_win = True

    for i in range(4):
        for j in range(4):
            row = board[i][j:j+4]
            if row == ['X']*4:
                x_win = True
            if row == ['O']*4:
                o_win = True

    for x in range(4):
        diagonal = []
        for y in range(4):
            diagonal.append(board[y][x + y])
            if diagonal == ['X']*4:
                x_win = True
            if diagonal == ['O']*4:
                o_win = True
        
    for x in range(6, 2, -1):
        diagonal = []
        for y in range(4):
            diagonal.append(board[y][x - y])
            if diagonal == ['X']*4:
                x_win = True
            if diagonal == ['O']*4:
                o_win = True
    
    if x_win and o_win:
        return 'T'
    if x_win:
        return 'X'
    if o_win:
        return 'O'
    
    return ''

player = 'X'
while True:
    for row in board:
        for symbol in row:
            print(symbol, end='')
        print()

    column = int(input())
    if board[0][column] != '-':
        for i in range(3, 0, -1):
            board[i][column] = board[i - 1][column]
        board[0][column] = player
    else:
        for i in range(4):
            if board[i][column] == '-':
                board[i][column] = player

                if i != 0:
                    board[i - 1][column] = '-'
            else:
                break

    if player == 'X':
        player = 'O'
    else:
        player = 'X'

    result = is_winner()
    if result == 'X':
        print("WINNER IS X")
        break
    elif result == 'O':
        print("WINNER IS O")
        break
    elif result == 'T':
        print("IT'S A TIE")
        break

for row in board:
    for symbol in row:
        print(symbol, end='')
    print()