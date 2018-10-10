from __future__ import print_function;
import copy;
import math;
from random import randint


class Node(): #each node is a node in the tree, it has a current state(data) and knows which symbol should be put next
    def __init__(self,data,nextSym):
        self.data = data;
        self.nextSym = nextSym;

def makeEmptyBoard(): #starting board
    board = [];
    board.append(['_','_','_']);
    board.append(['_','_','_']);
    board.append(['_','_','_']);
    return board;
    
def printBoard(board): #more visually aesthetic
    for row in board:
        for elem in row:
            print(elem + '|', end='');
        print('');
    print('----------');
        
def putX(board,row,col):
    if(board[row][col]=='_'):
        temp = copy.deepcopy(board);
        temp[row][col]='X';
        return temp;

def putO(board,row,col):
    if(board[row][col]=='_'):
        temp = copy.deepcopy(board);
        temp[row][col]='O';
        return temp;

def XWins(board):
    for row in board:
        if(row==['X','X','X']):
            return True;
    if(board[0][0]=='X' and board[1][0]=='X' and board[2][0]=='X'):
        return True;
    if(board[0][1]=='X' and board[1][1]=='X' and board[2][1]=='X'):
        return True;
    if(board[0][2]=='X' and board[1][2]=='X' and board[2][2]=='X'):
        return True;
    if(board[0][0]=='X' and board[1][1]=='X' and board[2][2]=='X'):
        return True;
    if(board[0][2]=='X' and board[1][1]=='X' and board[2][0]=='X'):
        return True;
    return False

def OWins(board):
    for row in board:
        if(row==['O','O','O']):
            return True;
    if(board[0][0]=='O' and board[1][0]=='O' and board[2][0]=='O'):
        return True;
    if(board[0][1]=='O' and board[1][1]=='O' and board[2][1]=='O'):
        return True;
    if(board[0][2]=='O' and board[1][2]=='O' and board[2][2]=='O'):
        return True;
    if(board[0][0]=='O' and board[1][1]=='O' and board[2][2]=='O'):
        return True;
    if(board[0][2]=='O' and board[1][1]=='O' and board[2][0]=='O'):
        return True;
    return False;

def noWin(board):
    return(not OWins(board) and not XWins(board) and not hasKids(board));

def hasKids(board):
    for row in board:
            if('_' in row):
                return True;
    return False;

def genKids(node):
        kids = [];
        if(node.nextSym == 'X'):
            for i in range(3):
                for j in range(3):
                    kid = Node(putX(node.data,i,j),'O');
                    if(kid.data==None): #so we dont add the current node as a kid
                        continue;
                    else:
                        kids.append(kid);
        else:
            for i in range(3):
                for j in range(3):
                    kid = Node(putO(node.data,i,j),'X');
                    if(kid.data==None): # same
                        continue;
                    else:
                        kids.append(kid);
        return kids;

def userMove(node,i,j):
    userNode = Node(putX(node.data,i,j),'O');
    return userNode;

def alphaBeta(node,depth,a,b,maxPlayer): #the real deal is here, the AI is unbeatable
    if(depth==0 or OWins(node.data) or XWins(node.data) or noWin(node.data)):
        if(OWins(node.data)):
            return -1;
        elif(XWins(node.data)):
            return 1;
        else:
            return 0;
    if(maxPlayer):
        v = -math.inf;
        kids = genKids(node);
        for kid in kids:
            v = max(v,alphaBeta(kid,depth-1,a,b,False));
            a = max(a,v);
            if(b<=a):
                break;
        return v;
    else:
        v = math.inf;
        kids = genKids(node);
        for kid in kids:
            v = min(v, alphaBeta(kid,depth-1,a,b,True));
            b = min(b,v);
            if(b<=a):
                break;
        return v;


def play(node): #this starts the game, we always play with X
    while(not XWins(node.data) or not OWins(node.data) or not noWin(node.data)):
        printBoard(node.data);
        i = int(input("choose row: ")) - 1;
        j = int(input("choose column: ")) - 1;
        while(i<0 or i>2 or j<0 or j>2 or node.data[i][j]!='_'):
            print("Invalid move,try again");
            printBoard(node.data);
            i = int(input("choose row: ")) - 1;
            j = int(input("choose column: ")) - 1;
        userPlay = userMove(node,i,j);
        printBoard(userPlay.data);
        if(XWins(userPlay.data)):
            print("YOU WIN");
            break;
        if(noWin(userPlay.data)):
            print("DRAW");
            break;
        kids = genKids(userPlay);
        bestKids = []; #means kids with heurisitc value of -1, тоест деца, с които ботът печели
        mediocreKids = []; #kids with heurisitc value of 0, тоест, деца с които ботът се бори за равенство
        for kid in kids:
            value = alphaBeta(kid,1000,-math.inf,math.inf,True);
            if(value==-1):
                bestKids.append(kid);
            elif(value==0):
                mediocreKids.append(kid);
        if(bestKids):
            print("best");
            print(bestKids);
            index = randint(0,len(bestKids)-1);
            node = bestKids[index];
        elif(mediocreKids and not bestKids):
            print("medi");
            print(mediocreKids)
            index = randint(0,len(mediocreKids)-1);
            node = mediocreKids[index];
        else:
            break;
        if(XWins(node.data)):
            printBoard(node.data);
            print("YOU WIN");
            break;
        elif(OWins(node.data)):
            printBoard(node.data);
            print("YOU LOSE");
            break;
        
#user input is from 0 to 2, where 0 means 1st row/column, 1 means 2nd row/column and 2 means 3rd row/column
start = Node(makeEmptyBoard(),'X'); #the empty board expects an X from us
play(start);
again = input("Do you wanna play again - y or n ?");
while(again=='y'):
    play(start);