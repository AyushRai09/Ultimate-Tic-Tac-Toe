import random
import copy
import sys
import time

class Player1:
        def __init__ (self):
            self.uptoMaxDepth=5
            self.num=0

        def utilityOfState(self,temp_board, old_move, currentMarker):
            return 0;

        def minimax(self,temp_board,old_move,currentMarker,depth, alpha,beta, parentAlpha, parentBeta, bestRow, bestCol):
            if(depth==self.uptoMaxDepth):
            	value=self.utilityOfState(temp_board, old_move, currentMarker)
            	return value , bestRow, bestCol
            row=old_move[0]%4
            col=old_move[1]%4
            if(currentMarker=='x'):
                nextMarker='o'
            else:
                nextMarker='x'
            if(depth%2==0):
                allowed_cells = temp_board.find_valid_move_cells(old_move)
                utility = 0
                if(len(allowed_cells)==0 and depth!=self.uptoMaxDepth):
                    value=self.utilityOfState(temp_board,old_move,currentMarker)
                    return value,bestRow,bestCol
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j] = currentMarker  #set the board index equal to your currentMarker
                    beta=parentBeta    #for a max node, beta is equal to the beta of it's parent node
                    if(alpha<beta):  #only call if this condition exists, otherwise prune it. That's why in the else condition, "break" is used.
                        utility,tempRow,tempCol = self.minimax(temp_board,new_move,nextMarker,depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                        if(alpha<utility): #if the new utility is found to be more than current alpha, then of course alpha>=utility. So now, the new worst case is that alpha=utility
                            alpha=utility
                            bestRow=i  #store the best row and col coordinates.
                            bestCol=j
                    else:
                        temp_board.board_status[i][j] = "-"
                        break
                    temp_board.board_status[i][j] = '-';  #set the board index equal to your currentMarker
            	return alpha,bestRow,bestCol  # return the alpha value found among all it's children
            else :
                allowed_cells=temp_board.find_valid_move_cells(old_move)
                utility = 0
                if(len(allowed_cells)==0 and depth!=self.uptoMaxDepth):
                    value=self.utilityOfState(temp_board,old_move,currentMarker)
                    return value,bestRow,bestCol
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j]=currentMarker
                    alpha=parentAlpha
                    if(alpha<beta):
                        utility,tempRow,tempCol=self.minimax(temp_board,new_move,nextMarker, depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                        if(beta>utility):
                            beta=utility
                            bestRow=i
                            bestCol=j
                    else:
                        temp_board.board_status[i][j] = "-"
                        break
                    temp_board.board_status[i][j] = "-"
                return beta,bestRow,bestCol

        def move(self,board,old_move,currentMarker):
            if old_move == (-1,-1):
                return (5,5)

            temp_board=copy.deepcopy(board)   #copy the state of the board
            utility, bestRow,bestCol= self.minimax(temp_board, old_move, currentMarker, 0, -100000.0, 100000.0, -100000.0, 100000.0,-1,-1)
            # print bestRow,bestCol
            return (bestRow,bestCol) # return the bestRow and bestCol
