#!/usr/bin/env python
import sys
from copy import deepcopy

def get_valid_moves(board):
    possible_moves = [(2,-1),(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(1,-2,),(-1,-2)]
    valid_moves = []
    cur = board.current_pos
    for m in possible_moves:
        pros_move = (cur[0]+m[0],cur[1]+m[1])
        if board.in_range(pros_move): valid_moves.append(pros_move)
    return filter(lambda x: board.valid(x), valid_moves)

# assumes move is valid
def move(board,pos):
    new_board = deepcopy(board)
    new_board.switch(pos)
    new_board.current_pos = pos
    return new_board

# ----------------------------------------------------------

class ChessBoard(object):
    move = move
    get_valid_moves = get_valid_moves

    def switch(self,(x,y)):
        self.board[x][y] = not self.board[x][y]

    def reset(self,(xpos,ypos)):
        board = []
        xlen,ylen = self.boardsize
        for x in range(xlen):
            board.append(map(lambda x: False, range(ylen)))
        board[xpos][ypos] = True
        self.board = board
        self.current_pos = (xpos,ypos)

    def __init__(self,pos=None,dim=(8,8),isopen=False):
        self.start = pos
        self.isopen = isopen
        self.boardsize = dim
        self.reset(pos)

    def valid(self,(x,y)):
        return not self.board[x][y] or (not self.isopen and (x,y) == self.start and self.isfull())

    def in_range(self,(x,y)):
        return (x in range(8)) and (y in range(8))

    def isfull(self):
        return all(map(lambda x: all(x), self.board)) 

    def __str__(self):
        output = ""
        switch = {True: "[X] ", False: "[ ] "}
        for j in range(self.boardsize[1]):
            for i in range(self.boardsize[0]):
                if (i,j) != self.current_pos:
                    output += switch[self.board[i][j]]
                else:
                    output += " K  "
            output = output.rstrip()+'\n'
        return output.rstrip()

# ----------------------------------------------------------

def find_tour(board,running):
    valid_moves = get_valid_moves(board)
    if not valid_moves and (not board.isfull() or not board.isopen): 
        return None
    elif not valid_moves and isopen:
        return running
    elif board.isfull() and not isopen:
        running.append(board.start)
        return running

    min_moves = min(map(lambda x: len(get_valid_moves(move(board,x))), valid_moves))
    valid_moves = filter(lambda x: len(get_valid_moves(move(board,x))) == min_moves, valid_moves)

    for m in valid_moves:
        running.append(m)
        seq = find_tour(move(board,m),running)
        if seq: return seq
    return None

def usage():
    print "ERROR: wrong number of parameters."
    print "Usage: knights_tour.py [-c] [-s X Y] x-cor y-cor"
    print "     -c      Find a closed tour"
    print "     -s X Y  Use a board of size X by Y"
    print "     x-cor   Starting x coordinate of knight (0-based)"
    print "     y-cor   Starting y coordinate of knight (0-based)"
    sys.exit(-1)
    
if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 7: usage()
    isopen = True
    dim = (8,8) 

    for i in range(len(sys.argv)):
        if sys.argv[i] == "-c": 
            isopen = False
        elif sys.argv[i] == "-s":
            if i+2 < len(sys.argv):
                dim = (int(sys.argv[i+1]), int(sys.argv[i+2]))
            else:
                usage()

    # According to Wikipedia:
    # "For any m x n board with m less than or equal to n, a closed knight's tour is always possible
    # unless one or more of these three conditions are met:
    #   1. m and n are both odd; m and n are not both 1
    #   2. m = 1, 2, or 4; m and n are not both 1
    #   3. m = 3 and n = 4, 6, or 8."
    if not isopen:
        m,n = dim
        if m > n: n,m = m,n
        if (m % 2 == 1 and n % 2 == 1 and (m != 1 and n != 1)) or \
           (m in [1,2,4] and (m!= 1 and n != 1)) or \
           (m == 3 and n in [4,6,8]):
            print "No closed tour possible with dimensions {0} by {1}.".format(m,n)
            sys.exit(0)

    start = (int(sys.argv[-2]),int(sys.argv[-1]))

    board = ChessBoard(start,dim,isopen)
    print "Starting board:"
    print board
    print

    move_seq = find_tour(board,[])

    for m in move_seq:
        print "Moving to", m
        board = move(board,m)
        print board
        raw_input()
