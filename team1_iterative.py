import random
import copy
import sys
import time

class Player1:
        def __init__ (self):
            self.uptoMaxDepth = 2
            self.num = 0
            self.start_time = time.time()
            self.mark = '-'

        def utilityOfState(self,temp_board, old_move, currentMarker):
            return random.randrange(-100,100);

        def check_block_status(self,board,old_move,new_move,ply):
            x = new_move[0]/4
    		y = new_move[1]/4
    		fl = 0
    		bs = board.board_status

    		#checking if a block has been won or drawn or not after the current move
    		for i in range(4):
    			#checking for horizontal pattern(i'th row)
    			if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
    				board.block_status[x][y] = ply
    				return 'win'
    			#checking for vertical pattern(i'th column)
    			if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
    				board.block_status[x][y] = ply
    				return 'win'

    		#checking for diagnol pattern
    		if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
    			board.block_status[x][y] = ply
    			return 'win'
    		if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
    			board.block_status[x][y] = ply
    			return 'win'

    		#checking if a block has any more cells left or has it been drawn
    		for i in range(4):
    			for j in range(4):
    				if bs[4*x+i][4*y+j] =='-':
    					return 'left'
    		board.block_status[x][y] = 'd'
    		return 'draw'


        def minimax(self,temp_board,old_move,currentMarker,depth, alpha,beta, parentAlpha, parentBeta, bestRow, bestCol):
            if((time.time() - self.start_time)>9):
            	value=self.utilityOfState(temp_board, old_move, currentMarker)
            	return value , bestRow, bestCol
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
                    temp_block_status = temp_board.block_status
                    check_block_status(temp_board,old_move,new_move,currentMarker)
                    beta=parentBeta    #for a max node, beta is equal to the beta of it's parent node
                    if(alpha<beta):  #only call if this condition exists, otherwise prune it. That's why in the else condition, "break" is used.
                        utility,tempRow,tempCol = self.minimax(temp_board,new_move,nextMarker,depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                        if(alpha<utility): #if the new utility is found to be more than current alpha, then of course alpha>=utility. So now, the new worst case is that alpha=utility
                            alpha=utility
                            bestRow=i  #store the best row and col coordinates.
                            bestCol=j
                    else:
                        temp_board.board_status[i][j] = "-"
                        temp_board.block_status = temp_block_status
                        break
                    temp_board.block_status = temp_block_status
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
                    temp_block_status = temp_board.block_status
                    check_block_status(temp_board,old_move,new_move,currentMarker)
                    alpha=parentAlpha
                    if(alpha<beta):
                        utility,tempRow,tempCol=self.minimax(temp_board,new_move,nextMarker, depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol)
                        if(beta>utility):
                            beta=utility
                            bestRow=i
                            bestCol=j
                    else:
                        temp_board.block_status = temp_block_status
                        temp_board.board_status[i][j] = "-"
                        break
                    temp_board.block_status = temp_block_status
                    temp_board.board_status[i][j] = "-"
                return beta,bestRow,bestCol

        def move(self,board,old_move,currentMarker):
            if old_move == (-1,-1):
                return (5,5)
            self.mark = currentMarker
            self.start_time = time.time()
            self.uptoMaxDepth=4
            bestRow=0
            bestCol=0
            temp_utility=0
            temp_board=copy.deepcopy(board)   #copy the state of the board
            while ((time.time() - self.start_time)<8):
                self.uptoMaxDepth+=1
                tempRow=bestRow
                tempCol=bestCol
                utility, bestRow,bestCol= self.minimax(temp_board, old_move, currentMarker, 0, -100000.0, 100000.0, -100000.0, 100000.0,-1,-1)

            print self.uptoMaxDepth
            # print bestRow,bestCol
            return (tempRow,tempCol) # return the bestRow and bestCol
