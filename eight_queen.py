#! /usr/bin/python

# This script it used to resolve the eight queen problem
import copy

count = 0
ansowers = []
def print_chess_board(queens):
    """
    print the chess board
    chess board is a 8X8 grid
    
    queens is a 8X8 matrix, with element's value being 1 is a queen. 0 is not a queen

    """
    #Print horizontal axis numbers:  0 1 2 3 4 5 6 7
    print(" ", end="")
    for i in range(8):
        print(" %d "%i, end="")
    print()

    #Print the matrix
    for i in range(8):
        print(i, end="")
        for j in range(8):
            queen=" "
            if queens[i][j] == 1 :
                queen="X"
            elif queens[i][j] == 2 :
                queen="*"
            else :
                queen=" "
                    
            print("[%s]"%queen,end="")
        print("")

def check_kill(i, j, queens):
    #print("kill ? %d%d\n"%(i, j))
    if queens[i][j] == 1: #There is other queen here, we can't kill her
        return False
    else:
        queens[i][j] = 2 # current queen can kill this
        return True


def check_piece(i, j, queens):
    if queens[i][j] != 1 : #There is not a queen here
        return True

    #print("check current queen pos %d%d\n"%(i, j))

    # check the horizon, k is the horizon
    for k in range(8):
        if k == j : # do not check it self
            continue
        if check_kill(i, k, queens) == False:
            return False;

    # check the vertical, k is the vertical
    for k in range(8):
        if k == i : # do not check it self
            continue
        if check_kill(k, j, queens) == False:
            return False;

    # check the 1 slash
    k = i - 1
    g = j - 1
    while k >= 0 and g >= 0:
        if check_kill(k, g, queens) == False:
            return False
        k -= 1
        g -= 1
                
    # check the 2 slash
    k = i - 1
    g = j + 1
    while k >= 0 and g < 8:
        if check_kill(k, g, queens) == False:
            return False
        k -= 1
        g += 1
                
    # check the 3 slash
    k = i + 1
    g = j - 1
    while k < 8 and g >= 0:
        if check_kill(k, g, queens) == False:
            return False
        k += 1
        g -= 1

    # check the 4 slash
    k = i + 1
    g = j + 1
    while k < 8 and g < 8:
        if check_kill(k, g, queens) == False:
            return False
        k += 1
        g += 1

    return True
                
                
def check_chess_board(queens):
    for i in range(8):
        for j in range(8):
            if not check_piece(i, j, queens) :
                return False 
    return True


def compare_ansower(a1, a2):
    for i in range(8):
        for j in range(8):
            if a1[i][j] != a2[i][j] :
                return False
    return True

def add_new_ansower(a1):
    global ansowers
    for i in ansowers:
        if compare_ansower(i, a1) == True:
            return False
    ansowers.append(copy.deepcopy(a1))
    return True


def find_eight_queen(f1, f2):
    # Inital a empty chess board
    queens=[[0 for i in range(8)] for i in range(8)]
    #print_chess_board(queens)

    queenPos=[(f1, f2)]
    queens[f1][f2] = 1

    recall=False

    while True:
        if recall == False and check_chess_board(queens): 
           # print_chess_board(queens)
           # print("Get here, allocate next queen")
            if len(queenPos) == 8:
                # We get a good ansower
                if add_new_ansower(queens) :
                    global ansowers
                    print("NO. %d"%len(ansowers))
                    print_chess_board(queens)

                # do not return here, we will get all ansower
                #return True


            gotNew = False
            for i in range(8):
                if gotNew:
                    break
                for j in range(8):
                    if queens[i][j] != 1 and queens[i][j] != 2:
                        queenPos.append((i, j))
                        queens[i][j] = 1;
                        gotNew = True
                        break
            if gotNew:
                continue

        #print("Get here, will modify the last queen position")
        if len(queenPos) == 0: # impossible 
            print("System Eror")
            return False 
	
        #unset the recall
        recall = False

        #cleen previous queen
        #print(queenPos[-1])
        queens[queenPos[-1][0]][queenPos[-1][1]] = 0
        for i in range(8):
            for j in range(8):
                if queens[i][j] == 2:
                    queens[i][j] = 0; 
        check_chess_board(queens)
        #print("After unset last queen")
        #print_chess_board(queens)

        gotNew = False
        #print((queenPos[-1][0] * 8) +  queenPos[-1][1] + 1, 64)
        for x in range((queenPos[-1][0] * 8) +  queenPos[-1][1] + 1, 64):
           # print("x=%d, x//8=%d, x%%8=%d\n"%(x, x//8, x%8))
            if queens[x//8][x%8] != 1 and queens[x//8][x%8] != 2:
                queenPos[-1] = (x//8, x%8);
                queens[x//8][x%8] = 1;
                gotNew = True
                break
        if gotNew:
            continue
        else:
           # print("get here, last queen position is end, will change the preview queen position")
            del queenPos[-1]
            recall = True;

def show_all_eight_queen():
    count = 1
    for i in range(8):
        for j in range(8):
           if find_eight_queen(i,j) :
                print(count)
                count += 1

if __name__ == "__main__" :
    find_eight_queen(0, 0)
