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
            self.originalBoard=[]


        def utilityOfState(self,temp_board, old_move, currentMarker,baseUtility):
            bs = temp_board.block_status
            ply = self.mark
            nply = self.oppo_mark
            dash = '-'
            draw = 'd'
#Writing heuristic values for block level
##################################################################################
            block_sum=0

            topToDown=[]
            downToTop=[]
            topToDown.append(bs[0][0])
            topToDown.append(bs[1][1])
            topToDown.append(bs[2][2])
            topToDown.append(bs[3][3])

            downToTop.append(bs[3][0])
            downToTop.append(bs[2][1])
            downToTop.append(bs[1][2])
            downToTop.append(bs[0][3])

            trans_block=zip(*bs) #calculating the transpose of teh orginal bs.

            if(downToTop.count(ply)==4 or topToDown.count(ply)==4):
                block_sum+=14500005
            if((downToTop.count(nply)==3 and downToTop.count(ply)==1) or (topToDown.count(nply)==3 and topToDown.count(ply)==1)):
                block_sum+=1500001
            if((downToTop.count(ply)==3 and downToTop.count(nply)==0) or (topToDown.count(ply)==3 and topToDown.count(nply)==0)):
                block_sum+=1400000
            if((downToTop.count(ply)==2 and downToTop.count(nply)==1) or (topToDown.count(ply)==2 and topToDown.count(nply)==1)):
                block_sum+=550000
            if((downToTop.count(ply)==2 and downToTop.count(nply)==0) or (topToDown.count(ply)==2 and topToDown.count(nply)==0)):
                block_sum+=150000


            if(downToTop.count(nply)==4 or topToDown.count(nply)==4):
                block_sum-=14500005
            if((downToTop.count(nply)==3 and downToTop.count(ply)==0) or (topToDown.count(nply)==3 and topToDown.count(ply)==0)):
                block_sum-=1400000
            if((downToTop.count(nply)==2 and downToTop.count(ply)==0) or (topToDown.count(nply)==2 and topToDown.count(ply)==0)):
                block_sum-=150000

            for i in range(4):
                if(bs[i].count(ply)==4): #myself winning cases from here
                    block_sum+=14500005
                if(bs[i].count(nply)==3 and bs[i].count(ply)==1):
                    block_sum+=1500001 #stopping opponent is very  important, note that it is even more important than completing my own one block
                if(bs[i].count(ply)==3 and bs[i].count(ply)==0):
                    block_sum+=1400000
                if(bs[i].count(nply)==2 and bs[i].count(ply)==1):
                    block_sum+=500000
                if(bs[i].count(ply)==2 and bs[i].count(nply)==0):
                    if((i==1 or i==2) and (bs[i][1]==ply and bs[i][2]==ply)):
                        block_sum+=100000
                    elif(i==1 or i==2):
                        block_sum+=90000
                    if((i==0 or i==3) and (bs[i][0]==ply and bs[i][3]==ply)):
                        block_sum+=100000
                    elif(i==0 or i==3):
                        block_sum+=90000

                if(bs[i].count(nply)==4): ########opponent winning cases from here
                        block_sum-=14500005
                if(bs[i].count(nply)==3 and bs[i].count(ply)==0):
                        block_sum-=1400001
                if(bs[i].count(nply)==2 and bs[i].count(ply)==0):
                        if((i==1 or i==2) and (bs[i][1]==nply and bs[i][2]==nply)):
                            block_sum-=100000
                        elif(i==1 or i==2):
                            block_sum-=90000
                        if((i==0 or i==3) and (bs[i][0]==nply and bs[i][3]==nply)):
                            block_sum-=100000
                        elif(i==0 or i==3):
                            block_sum-=90000

                if(trans_block[i].count(ply)==4): #now doing the same thing as above but doing it in the columns
                    block_sum+=14500005
                if(trans_block[i].count(nply)==3 and trans_block[i].count(ply)==1):
                    block_sum+=1500001 #stopping opponent is very  important, note that it is even more important than completing my own one block
                if(trans_block[i].count(ply)==3 and trans_block[i].count(ply)==0):
                    block_sum+=1400001
                if(trans_block[i].count(nply)==2 and trans_block[i].count(ply)==1):
                    block_sum+=500000
                if(trans_block[i].count(ply)==2 and trans_block[i].count(nply)==0):
                    if((i==1 or i==2) and (trans_block[i][1]==ply and trans_block[i][2]==ply)):
                        block_sum+=100000
                    elif(i==1 or i==2):
                        block_sum+=90000
                    if((i==0 or i==3) and (trans_block[i][0]==ply and trans_block[i][3]==ply)):
                        block_sum+=100000
                    elif(i==0 or i==3):
                        block_sum+=90000

                if(trans_block[i].count(nply)==4): ########opponent winning cases from here
                        block_sum-=14500005
                if(trans_block[i].count(nply)==3 and trans_block[i].count(ply)==0):
                        block_sum-=1400001
                if(trans_block[i].count(nply)==2 and trans_block[i].count(ply)==0):
                        if((i==1 or i==2) and (trans_block[i][1]==nply and trans_block[i][2]==nply)):
                            block_sum-=100000
                        elif(i==1 or i==2):
                            block_sum-=90000
                        if((i==0 or i==3) and (trans_block[i][0]==nply and trans_block[i][3]==nply)):
                            block_sum-=100000
                        elif(i==0 or i==3):
                            block_sum-=90000

################################################################################
#Rules for the cell level filling.
            row_up=0
            row_down=4
            col_left=0
            col_right=4;
            array_sum=0
            while(row_down<=16):
                long_arr=temp_board.board_status[row_up:row_down]
                col_left=0
                col_right=4
                while(col_right<=16):
                    required_arr=[]
                    for i in range(4):
                        required_arr.append([])
                        temp_arr=long_arr[i][col_left:col_right]
                        required_arr[i]=temp_arr
                    backslash=[]
                    forwardslash=[]
                    two1case=[]
                    reversetwo1case=[]
                    # print "long_arr:",long_arr
                    # print "required_arr:",required_arr
                    transpose_arr=zip(*required_arr)
                    # print "transpose_arr:",transpose_arr
                    # print "\n"
                    backslash.append(required_arr[0][0])
                    backslash.append(required_arr[1][1])
                    backslash.append(required_arr[2][2])
                    backslash.append(required_arr[3][3])

                    forwardslash.append(required_arr[3][0])
                    forwardslash.append(required_arr[2][1])
                    forwardslash.append(required_arr[1][2])
                    forwardslash.append(required_arr[0][3])
                    #########################################################
                    #Doing this for the two1case and three1case in the diagonals
                    two1case.append(self.originalBoard[row_up][col_left])#Shape similar to backslash
                    two1case.append(self.originalBoard[row_up+1][col_left+1])
                    two1case.append(self.originalBoard[row_up+2][col_left+2])
                    two1case.append(self.originalBoard[row_up+3][col_left+3])

                    reversetwo1case.append(self.originalBoard[row_down-1][col_left])#Shape similar to forwardslash
                    reversetwo1case.append(self.originalBoard[row_down-2][col_left+1])
                    reversetwo1case.append(self.originalBoard[row_down-3][col_left+2])
                    reversetwo1case.append(self.originalBoard[row_down-4][col_left+3])
                    # print "Hello Ayush"
                    #########################################################
                    if(backslash.count(ply)==4 or forwardslash.count(ply)==4):
                        array_sum+=10000
                    if((backslash.count(nply)==3 and backslash.count(ply)==1) or (forwardslash.count(nply)==3 and forwardslash.count(ply) ==1)):
                        array_sum+=950
                    if((backslash.count(ply)==3 and backslash.count(nply)==0) or (forwardslash.count(ply)==3 and forwardslash.count(nply)==0)):
                        array_sum+=920#I gave it a sum of 950 whereas for the row or column sum calculation below, I have given it 900 because filling three markers in diagonal is better than filling three in same row or column
                    if((backslash.count(ply)==2 and backslash.count(nply)==0) or (forwardslash.count(ply)==2 and forwardslash.count(nply)==0)):
                        array_sum+=82 #This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
                    if((backslash.count(nply)==2 and backslash.count(ply)==1) or (forwardslash.count(nply)==2 and forwardslash.count(ply) ==1)):
                        array_sum+=6.5
                    if(backslash.count(ply)==1 or forwardslash.count(ply)==1):
                        array_sum+=1
                    if(backslash.count(nply)==4 or forwardslash.count(nply)==4):
                        array_sum-=10000
                    if(backslash.count(ply)==3 and backslash.count(nply)==1): #Cases of mine 3, his 1 were left out earlier, now included.
                        if(two1case.count(nply)==0):
                            array_sum-=950
                    if(forwardslash.count(ply)==3 and forwardslash.count(nply)==1):
                        if(reversetwo1case.count(nply)==0):
                            array_sum-=950
                    if((backslash.count(nply)==3 and backslash.count(ply)==0) or (forwardslash.count(nply)==3 and forwardslash.count(ply)==0)):
                        array_sum-=900#I gave it a sum of 95 whereas for the row or column sum calculation below, I have given it 90 because filling three markers in diagonal is better than filling three in same row or column
                    if((backslash.count(nply)==2 and backslash.count(ply)==0) or (forwardslash.count(nply)==2 and forwardslash.count(ply)==0)):
                        array_sum-=80
                    if(backslash.count(ply)==2 and backslash.count(ply)==1): #Cases of mine 2, his 1 were left out earlier, now included.
                        if(two1case.count(nply)==0):
                            array_sum-=6.5
                    if(forwardslash.count(ply)==2 and forwardslash.count(nply)==1):
                        if(reversetwo1case.count(nply)==0):
                            array_sum-=6.5



                    for i in range(4):
                        if(required_arr[i].count(ply)==4): ##me winning checking the rows
                            array_sum+=10000
                        if(required_arr[i].count(nply)==3 and required_arr[i].count(ply)==1):
                            array_sum+=950
                        if(required_arr[i].count(ply)==3 and required_arr[i].count(nply)==0):
                            array_sum+=900
                        if(required_arr[i].count(ply)==2 and required_arr[i].count(nply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum+=80
                            else:             #if the markers found are in boundary rows
                                array_sum+=75
                        if(required_arr[i].count(nply)==2 and required_arr[i].count(ply)==1):
                            array_sum+=6.5
                        # if(required_arr[i].count(ply)==1 and required_arr[i].count(nply)==0):
                        #     array_sum+=50
                        if(required_arr[i].count(nply)==4): ##opponent winning checking the rows
                            array_sum-=10000
                        if(required_arr[i].count(ply)==3 and required_arr[i].count(nply)==1):
                            if(self.originalBoard[row_up+i][col_left]!=nply and self.originalBoard[row_up+i][col_left+1]!=nply and self.originalBoard[row_up+i][col_left+2]!=nply and self.originalBoard[row_up+i][col_left+3]!=nply):
                                array_sum-=950
                        if(required_arr[i].count(nply)==3 and required_arr[i].count(ply)==0):
                            array_sum-=900
                        if(required_arr[i].count(nply)==2 and required_arr[i].count(ply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum-=80
                            else:             #if the markers found are in boundary rows
                                array_sum-=75
                        if(required_arr[i].count(ply)==2 and required_arr[i].count(nply)==1):
                            if(self.originalBoard[row_up+i][col_left]!=nply and self.originalBoard[row_up+i][col_left+1]!=nply and self.originalBoard[row_up+i][col_left+2]!=nply and self.originalBoard[row_up+i][col_left+3]!=nply):
                                array_sum-=6.5

                        # if(required_arr[i].count(nply)==1 and required_arr[i].count(ply)==0):
                        #     array_sum-=50


                        if(transpose_arr[i].count(ply)==4):#doing the above eight things for the columns
                            array_sum+=10000
                        if(transpose_arr[i].count(nply)==3 and transpose_arr[i].count(ply)==1):
                            array_sum+=950
                        if(transpose_arr[i].count(ply)==3 and transpose_arr[i].count(nply)==0):
                            array_sum+=900
                        if(transpose_arr[i].count(ply)==2 and transpose_arr[i].count(nply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum+=80
                            else:             #if the markers found are in boundary rows
                                array_sum+=75
                        if(transpose_arr[i].count(nply)==2 and transpose_arr[i].count(ply)==1):
                            array_sum+=6.5
                        # if(transpose_arr[i].count(ply)==1 and transpose_arr[i].count(nply)==0):
                        #     array_sum+=70
                        if(transpose_arr[i].count(nply)==4):
                            array_sum-=10000
                        if(transpose_arr[i].count(ply)==3 and transpose_arr.count(nply)==1):
                            if(self.originalBoard[row_up][col_left+i]!=nply and self.originalBoard[row_up+1][col_left+i]!=nply and self.originalBoard[row_up+2][col_left+i]!=nply and self.originalBoard[row_up+3][col_lefti]!=nply):
                                array_sum-=950
                        if(transpose_arr[i].count(nply)==3 and transpose_arr[i].count(ply)==0):
                            array_sum-=900
                        if(transpose_arr[i].count(nply)==2 and transpose_arr[i].count(ply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum-=80
                            else:             #if the markers found are in boundary rows
                                array_sum-=75
                        if(transpose_arr[i].count(ply)==2 and transpose_arr[i].count(nply)==1):
                            if(self.originalBoard[row_up][col_left+i]!=nply and self.originalBoard[row_up+1][col_left+i]!=nply and self.originalBoard[row_up+2][col_left+i]!=nply and self.originalBoard[row_up+3][col_left+i]!=nply):
                                array_sum-=6.5
                        # if(transpose_arr[i].count(nply)==1 and transpose_arr[i].count(ply)==0):
                        #     array_sum-=50
                    col_left+=4
                    col_right+=4
                row_up+=4;
                row_down+=4;
            # if(array_sum>200000):
            #     print "old_move:",old_move
            #     while(True):
            #         print "array_sum:",array_sum
            #print "returned utility:", array_sum-baseUtility
            return  block_sum+array_sum-baseUtility

                        #else: array_sum remains the same. It is a draw, basically with zero utility, neither you win nor you loose.




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


        def minimax(self,temp_board,old_move,currentMarker,depth, alpha,beta, parentAlpha, parentBeta, bestRow, bestCol,baseUtility):
            # print "hello",depth
            if(currentMarker=='x'):
                nextMarker='o'
            else:
                nextMarker='x'
# commented for testing purpose
            if((time.time() - self.start_time)>14.8):
             	value=self.utilityOfState(temp_board, old_move, nextMarker,baseUtility)
            #     print depth,time.time()-self.start_time
             	return value , bestRow, bestCol
            # print "DEPTH:",depth
            if(depth==self.uptoMaxDepth):
            	value=self.utilityOfState(temp_board, old_move, nextMarker,baseUtility)
            	return value , bestRow, bestCol
            row=old_move[0]%4
            col=old_move[1]%4

            if(depth%2==0):
                allowed_cells = temp_board.find_valid_move_cells(old_move)
                random.shuffle(allowed_cells)
                utility = 0
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker,baseUtility)
                    return value,bestRow,bestCol
                beta=parentBeta    #for a max node, beta is equal to the beta of it's parent node
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j] = currentMarker  #set the board index equal to your currentMarker
                    temp_block_status = copy.deepcopy(temp_board.block_status)
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
                    if(alpha<beta):  #only call if this condition exists, otherwise prune it. That's why in the else condition, "break" is used.
                        utility,tempRow,tempCol = self.minimax(temp_board,new_move,nextMarker,depth+1, -1000000000.0, 1000000000.0, alpha, beta, bestRow, bestCol,baseUtility)
                        if(alpha<utility): #if the new utility is found to be more than current alpha, then of course alpha>=utility. So now, the new worst case is that alpha=utility
                            alpha=utility
                            bestRow=i  #store the best row and col coordinates.
                            bestCol=j
                    else:
                        temp_board.board_status[i][j] = "-" #returning from recursion, so make the state as it was before.
                        temp_board.block_status = copy.deepcopy(temp_block_status) #returning from recursion, so make the state as it was before.
                        break
                    temp_board.block_status = copy.deepcopy(temp_block_status)
                    temp_board.board_status[i][j] = '-';  #set the board index equal to your currentMarker
            	return alpha,bestRow,bestCol  # return the alpha value found among all it's children
            else :
                allowed_cells=temp_board.find_valid_move_cells(old_move)
                random.shuffle(allowed_cells)
                utility = 0
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker,baseUtility)
                    return value,bestRow,bestCol
                alpha=parentAlpha
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j]=currentMarker
                    temp_block_status = copy.deepcopy(temp_board.block_status)
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
                    if(alpha<beta):
                        utility,tempRow,tempCol=self.minimax(temp_board,new_move,nextMarker, depth+1, -1000000000.0, 1000000000.0, alpha, beta, bestRow, bestCol,baseUtility)
                        if(beta>utility):
                            beta=utility
                            bestRow=i
                            bestCol=j
                    else:
                        temp_board.block_status = copy.deepcopy(temp_block_status)
                        temp_board.board_status[i][j] = "-"
                        break
                    temp_board.block_status = copy.deepcopy(temp_block_status)
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
            self.uptoMaxDepth=1
            temp1Row=0
            temp1Col=0
            temp_utility=0
            temp_board=copy.deepcopy(board)   #copy the state of the board
            self.originalBoard=copy.deepcopy(board.board_status)
            flag=0
            baseUtility=self.utilityOfState(temp_board,old_move,currentMarker,0)
            while ((time.time() - self.start_time)<14 and self.uptoMaxDepth<=256):
                bestRow = temp1Row
                bestCol = temp1Col
                utility, temp1Row,temp1Col= self.minimax(temp_board, old_move, currentMarker, 0, -1000000000.0, 1000000000.0, -1000000000.0, 1000000000.0,-1,-1,baseUtility)
                print "depth:",self.uptoMaxDepth,"utility:",utility,"bestRow:",temp1Row,"bestCol:",temp1Col
                flag+=1
                self.uptoMaxDepth+=1
            if(flag>=2):
                print "Depth",self.uptoMaxDepth-2
                print "bestRow:",bestRow,"bestCol:",bestCol
                return (bestRow,bestCol) # return the bestRow and bestCol
            else:
                print "Depth",self.uptoMaxDepth-2
                print "bestRow:",temp1Row,"bestCol:",temp1Col
                return (temp1Row,temp1Col)
