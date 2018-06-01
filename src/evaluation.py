board1 = [[4,2,0,0], [2,2,0,0], [0,0,0,0], [0,0,0,0]]
board2 = [[2,4,0,0], [0,0,2,2], [0,0,0,0], [0,0,0,0]]

def sideStick(board):
    sumtop = sum(board[0])
    sumbottom = sum(board[-1])
    sumleft = sum([board[i][0] for i in range(len(board))])
    sumright = sum([board[i][-1] for i in range(len(board))])

    maxtop = max(board[0])
    maxbottom = max(board[-1])
    maxleft = max([board[i][0] for i in range(len(board))])
    maxright = max([board[i][-1] for i in range(len(board))])

    score = (sumtop + sumbottom + sumleft + sumright) - (maxtop + maxbottom + maxleft + maxright)

    return score

def slopedBoard(board):
    rowmax = [max(board[i]) for i in range(len(board))]
    maxtile = max(rowmax)

    rowpos = round(rowmax.index(maxtile)/(len(board)-1))
    colpos = round(board[rowmax.index(maxtile)].index(maxtile)/(len(board)-1))

    if(rowpos == 0 and colpos ==0):
        ## topleft
        weightmatrix = [[i+j for i in range(len(board)-1,-1,-1)] for j in range(len(board)-1,-1,-1)]
    elif(rowpos == 1 and colpos ==0):
        ## bottomleft
        weightmatrix = [[i+j for i in range(len(board)-1,-1,-1)] for j in range(len(board))]
    elif(rowpos == 0 and colpos == 1):
        ## topright
        weightmatrix = [[i+j for i in range(len(board))] for j in range(len(board)-1,-1,-1)]
    else:
        ## bottomright
        weightmatrix = [[i+j for i in range(len(board))] for j in range(len(board))]

    weighted_matrix = [[0 for i in range(len(board))] for j in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board)):
            ## row i board * column j weightmatrix
            weighted_matrix[i][j] = sum([board[i][k]*weightmatrix[k][j] for k in range(len(board))])
    mysum = 0
    for i in range(len(weighted_matrix)):
        mysum += sum(weighted_matrix[i])

    return mysum
