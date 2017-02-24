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
            self.oppo_mark = '-'

        def utilityOfState(self,temp_board, old_move, currentMarker):
            bs = temp_board.block_status
            ply = self.mark
            nply = self.oppo_mark
            dash = '-'
            draw = 'd'

            #checking if a Game has been won or drawn or not after the current move
            #checking diagonals
            cntpd1=0 #count of playing diagonal1
            cntpd2=0 #count of playing diagonal2
            cntnd1=0 #count of opposite diagonal1
            cntnd2=0 #count of opposite diagonal2
            cntdd1=0 #count of dash diagonal1
            cntdd2=0 #count of dash diagonal2
            for i in range(4):						#counts the blocks won by x, o and drawn blocks
                for j in range(4):
                    if bs[i][j] == ply:
                        cntpd1 += 1
                    if bs[3-i][j] == ply:
                        cntpd2 += 1
                    if bs[i][j] == nply:
                        cntnd1 += 1
                    if bs[3-i][j] == nply:
                        cntnd2 += 1
                    if bs[i][j] == dash:
                        cntdd1 += 1
                    if bs[3-i][j] == dash:
                        cntdd2 += 1
            for i in range(4):
                row = bs[i]							#i'th row
                col = [x[i] for x in bs]			#i'th column
                #checking if i'th row or i'th column has been won or not
                if (row.count(ply) == 4):
                    return 10000
                if (col.count(ply) == 4):
                    return 10000
                if (row.count(nply) == 4):
                    return -10000
                if (col.count(nply) == 4):
                    return -10000

            if(currentMarker==ply):
                if (cntpd1 == 4 or cntpd2 == 4):
                    return 10000
                if (cntnd1 == 3 or cntpd2 == 1):
                    return 95000

# I don't why it's demanding such indentation! please check
                for i in range(4):
                    	row = bs[i]							#i'th row
                    	col = [x[i] for x in bs]			#i'th column
                        if (row.count(nply)==3 and row.count(ply)==1):
                            return 9500
                        if (row.count(ply)==3 and row.count(dash)==1) :
                            return 9000
                        if (col.count(nply)==3 and col.count(ply)==1) :
                            return 9500
                        if (col.count(ply)==3 and col.count(dash)==1):
                            return 9000
            else:
                if (cntnd1 == 4 or cntnd2 == 4):
                    return -10000

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
            if(currentMarker=='x'):
                nextMarker='o'
            else:
                nextMarker='x'
# commented for testing purpose
            # if((time.time() - self.start_time)>14.8):
            # 	value=self.utilityOfState(temp_board, old_move, nextMarker)
            #     print depth,time.time()-self.start_time
            # 	return value , bestRow, bestCol
            if(depth==self.uptoMaxDepth):
            	value=self.utilityOfState(temp_board, old_move, nextMarker)
            	return value , bestRow, bestCol
            row=old_move[0]%4
            col=old_move[1]%4

            if(depth%2==0):
                allowed_cells = temp_board.find_valid_move_cells(old_move)
                utility = 0
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker)
                    return value,bestRow,bestCol
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j] = currentMarker  #set the board index equal to your currentMarker
                    temp_block_status = temp_board.block_status
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
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
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker)
                    return value,bestRow,bestCol
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j]=currentMarker
                    temp_block_status = temp_board.block_status
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
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
            if(currentMarker=='x'):
                self.oppo_mark='o'
            else:
                self.oppo_mark='x'
            self.start_time = time.time()
            self.uptoMaxDepth=4
            tempRow=0
            tempCol=0
            temp_utility=0
            temp_board=copy.deepcopy(board)   #copy the state of the board
    #commented for testing purpose
            # while ((time.time() - self.start_time)<1):
                # self.uptoMaxDepth+=1
                # bestRow = tempRow
                # bestCol = tempCol
            utility, tempRow,tempCol= self.minimax(temp_board, old_move, currentMarker, 0, -100000.0, 100000.0, -100000.0, 100000.0,-1,-1)

            # print self.uptoMaxDepth
            # print "bestRow:",bestRow,"bestCol:",bestCol
            return (tempRow,tempCol) # return the bestRow and bestCol
