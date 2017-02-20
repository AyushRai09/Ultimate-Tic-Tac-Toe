import random
import copy
import sys
import time

class Player1:
        def __init__ (self):
            self.uptoMaxDepth=5
            self.num=0

        def utilityOfState(self,board, old_move, currentMarker):
            return 0;

        def minimax(self,board,old_move,currentMarker,depth, alpha,beta, parentAlpha, parentBeta, bestRow, bestCol):
            if(depth==self.uptoMaxDepth):
            	value=self.utilityOfState(board, old_move, currentMarker)
                ######THIS utilityOfState  IS THE HEURISTIC FUNCTION. NO SUCH FUNCTION EXISTS AS OF NOW.
            	return value , bestRow,bestCol
            row=old_move[0]%4 #this will give the row of the block in which we are going to play next.
            col=old_move[1]%4 #this will give the col of the block in which we are going to play next.
            if(currentMarker=='x'):
                nextMarker='o' #this is done in order to figure out what the opponent is going to play with, 'x' or 'o' in the next move.
            else:
                nextMarker='x'
            #IF the node is MAX node
            if(depth%2==0):
                for i in range(4*row,4*row+4):
                    for j in range(4*col, 4*col+4):
                        if(board[i][j]=='-') :
                            new_move=[i,j];
                            board[i][j]=currentMarker  #set the board index equal to your currentMarker
                            beta=parentBeta    #for a max node, beta is equal to the beta of it's parent node
                            if(alpha<beta):  #only call if this condition exists, otherwise prune it. That's why in the else condition, "break" is used.
                                utility,bestRow,bestCol=self.minimax(board,new_move,nextMarker,depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                                if(alpha<utility): #if the new utility is found to be more than current alpha, then of course aplha>=utility. So now, the new worst case is that alpha=utility
                                    alpha=utility
                                    bestRow=i  #store the best row and col coordinates.
                                    bestCol=j
                            else:
                                print depth," row:",row," col:",col," i:",i," j:",j
                                break
            	return alpha,bestRow,bestCol  # return the alpha value found among all it's children
            else :
                for i in range(4*row, 4*row+4):
                    for j in range (4*col, 4*col+4):
                        if(board[i][j]=='-'):
                            new_move=[i,j];
                            board[i][j]=currentMarker
                            alpha=parentAlpha
                            if(alpha<beta):
                                utility,bestRow,bestCol=self.minimax(board,new_move,nextMarker, depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                                if(beta>utility):
                                    beta=utility
                                    bestRow=i
                                    bestCol=j
                            else:
                                print depth,i,j
                                break
                return beta,bestRow,bestCol


        def move(self,board,old_move,currentMarker):
            if old_move == (-1,-1):
                return (8,8) #if your turn is first, mark the center of the board.

            temp_board=copy.deepcopy(board)   #copy the state of the board
            utility, bestRow,bestCol= self.minimax(temp_board.board_status, old_move, currentMarker, 0, -100000.0, 100000.0, -100000.0, 100000.0,-1,-1)
            #send it minimax function with self-explanatory args
            return (bestRow,bestCol) # return the bestRow and bestCol
#board is the copy of the original current board state which is filled by 'x' and 'o'
#old_move is the move of your opponent
#currentMarker is the marker that you are playing with. Either 'x' or 'o'
#maximizer is boolean value. "True" means you are standing at MAX node and "False" means otherwise.
#depth is the current level where you are standing at. Root node has depth level=0
#alpha is the worst value that MAX player can afford
#beta is the worst value MIN player can afford
#parentAlpha is the alpha of the parent.
#parentBeta is the beta of the parent node.
#bestRow is the row number of our next move
#bestCol is the col number of or next move
