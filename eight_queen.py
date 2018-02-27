#! /usr/bin/python

# This script it used to resolve the eight queen problem

def print_chess_board():
    """
    print the chess board
    chess board is a 8X8 grid
    """
    #Print horizontal axis numbers: 1 2 3 4 5 6 7 8
    print(" ", end="")
    for i in range(1, 9):
        print(" %d "%i, end="")
    print()

    #Print the matrix
    for i in range(8):
        print(i+1, end="")
        for j in range(8):
            print("[ ]",end="")
        print("")


if __name__ == "__main__" :
    print_chess_board()
    print("Failed to resolve Eight Queen problem")
