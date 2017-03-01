import random
import copy
import sys
import time

# matrix=[[0 for x in range(4)] for y in range(4)]
# matrix[0][0]=1
# matrix[0][1]=1
# matrix[0][2]=1
# matrix[0][3]=1
# matrix[1][0]=1
# matrix[1][1]=1
# matrix[1][2]=1
# matrix[1][3]=1
# matrix[2][0]=1
# matrix[2][1]=1
# matrix[2][2]=1
# matrix[2][3]=1
# matrix[3][0]=1
# matrix[3][1]=1
# matrix[3][2]=1
# matrix[3][3]=1


class Player1:
        def __init__ (self):
            self.uptoMaxDepth = 2
            self.num = 0
            self.start_time = time.time()
            self.mark = '-'
            self.oppo_mark = '-'


        def utilityOfState(self,temp_board, old_move, currentMarker,baseUtility):
            bs = temp_board.block_status
            ply = self.mark
            nply = self.oppo_mark
            dash = '-'
            draw = 'd'
#Writing heuristic values for block level
##################################################################################
            block_sum=0
            #To be removed ...................
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            # This is 82 whereas same case in column and rows give 80 reward. This is so,because I am valuing diagonals to be more important than rows and columns
            #To be removed.....................
            trans_block=zip(*bs)
            for i in range(4):
                if(bs[i].count(ply)==4): #myself winning cases from here
                    block_sum+=4500005
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
                if(bs[i].count(ply)==1 and (i==0 or i==3) and (bs[i][0]==ply or bs[i][3]==ply)):#this one and the next one gives extra priority
                        block_sum+=10000 #to filling either in the diagonals or in the corneres .
                if(bs[i].count(ply)==1 and (i==1 or i==2) and (bs[i][1]==ply or bs[i][2]==ply)):
                        block_sum+=10000

                if(bs[i].count(nply)==4): ########opponent winning cases from here
                        block_sum-=4500005
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
                if(bs[i].count(nply)==1 and (i==0 or i==3) and(bs[i][0]==nply or bs[i][3]==nply)):
                        block_sum-=10000
                if(bs[i].count(nply)==1 and (i==1 or i==2) and (bs[i][0]==nply or bs[i][2]==nply)):
                        block_sum-=10000

                if(trans_block[i].count(ply)==4): #now doing the same thing as above but doing it in the columns
                    block_sum+=4500005
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
                if(trans_block[i].count(ply)==1 and (i==0 or i==3) and (trans_block[i][0]==ply or trans_block[i][3]==ply)):#this one and the next one gives extra priority
                        block_sum+=10000 #to filling either in the diagonals or in the corneres .
                if(trans_block[i].count(ply)==1 and (i==1 or i==2) and (trans_block[i][1]==ply or trans_block[i][2]==ply)):
                        block_sum+=10000

                if(trans_block[i].count(nply)==4): ########opponent winning cases from here
                        block_sum-=4500005
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
                if(trans_block[i].count(nply)==1 and (i==0 or i==3) and(trans_block[i][0]==nply or trans_block[i][3]==nply)):
                        block_sum-=10000
                if(trans_block[i].count(nply)==1 and (i==1 or i==2) and (trans_block[i][0]==nply or trans_block[i][2]==nply)):
                        block_sum-=10000

##################################################################################
            #checking if a Game has been won or drawn or not after the current move
            #checking diagonals
#     `        cntpd1=0 #count of playing diagonal1
#             cntpd2=0 #count of playing diagonal2
#             cntnd1=0 #count of opposite diagonal1
#             cntnd2=0 #count of opposite diagonal2
#             cntdd1=0 #count of dash diagonal1
#             cntdd2=0 #count of dash diagonal2
#             for i in range(4):						#counts the blocks won by x, o and drawn blocks
#                 for j in range(4):
#                     if bs[i][j] == ply:
#                         cntpd1 += 1
#                     if bs[3-i][j] == ply:
#                         cntpd2 += 1
#                     if bs[i][j] == nply:
#                         cntnd1 += 1
#                     if bs[3-i][j] == nply:
#                         cntnd2 += 1
#                     if bs[i][j] == dash:
#                         cntdd1 += 1
#                     if bs[3-i][j] == dash:
#                         cntdd2 += 1
#             for i in range(4):
#                 row = bs[i]							#i'th row
#                 col = [x[i] for x in bs]			#i'th column
#                 #checking if i'th row or i'th column has been won or not
#                 if (row.count(ply) == 4):
#                     return 10000
#                 if (col.count(ply) == 4):
#                     return 10000
#                 if (row.count(nply) == 4):
#                     return -10000
#                 if (col.count(nply) == 4):
#                     return -10000
#
#             if(currentMarker==ply):
#                 if (cntpd1 == 4 or cntpd2 == 4):
#                     return 10000
#                 if (cntnd1 == 3 or cntpd2 == 1):
#                     return 95000
#
# # I don't why it's demanding such indentation! please check
#                 for i in range(4):
#                     row = bs[i]         #ith row
#                     col = [x[i] for x in bs]  #ith column
#                     if (row.count(nply)==3 and row.count(ply)==1):
#                         return 9500
#                     if (row.count(ply)==3 and row.count(dash)==1) :
#                         return 9000
#                     if (col.count(nply)==3 and col.count(ply)==1) :
#                         return 9500
#                     if (col.count(ply)==3 and col.count(dash)==1):
#                         return 9000
#             else:
#                 if (cntnd1 == 4 or cntnd2 == 4):
#                     return -10000

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
                    if((backslash.count(nply)==3 and backslash.count(ply)==0) or (forwardslash.count(nply)==3 and forwardslash.count(ply)==0)):
                        array_sum-=900#I gave it a sum of 95 whereas for the row or column sum calculation below, I have given it 90 because filling three markers in diagonal is better than filling three in same row or column
                    if((backslash.count(nply)==2 and backslash.count(ply)==0) or (forwardslash.count(nply)==2 and forwardslash.count(ply)==0)):
                        array_sum-=80


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
                        if(required_arr[i].count(nply)==3 and required_arr[i].count(ply)==0):
                            array_sum-=900
                        if(required_arr[i].count(nply)==2 and required_arr[i].count(ply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum-=80
                            else:             #if the markers found are in boundary rows
                                array_sum-=75
                        # if(required_arr[i].count(nply)==1 and required_arr[i].count(ply)==0):
                        #     array_sum-=50


                        if(transpose_arr[i].count(ply)==4 and transpose_arr[i].count(nply)==0):#doing the above eight things for the columns
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
                        if(transpose_arr[i].count(nply)==4 and transpose_arr[i].count(ply)==0):
                            array_sum-=10000
                        if(transpose_arr[i].count(nply)==3 and transpose_arr[i].count(ply)==0):
                            array_sum-=900
                        if(transpose_arr[i].count(nply)==2 and transpose_arr[i].count(ply)==0):
                            if(i==1 or i==2): #if the markers found are in the middle two rows
                                array_sum-=80
                            else:             #if the markers found are in boundary rows
                                array_sum-=75
                        if(transpose_arr[i].count(nply)==2 and transpose_arr[i].count(ply)==1):
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
            return  array_sum-baseUtility

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
            # if((time.time() - self.start_time)>14.8):
            # 	value=self.utilityOfState(temp_board, old_move, nextMarker)
            #     print depth,time.time()-self.start_time
            # 	return value , bestRow, bestCol
            # print "DEPTH:",depth
            if(depth==self.uptoMaxDepth):
            	value=self.utilityOfState(temp_board, old_move, nextMarker,baseUtility)
            	return value , bestRow, bestCol
            row=old_move[0]%4
            col=old_move[1]%4

            if(depth%2==0):
                allowed_cells = temp_board.find_valid_move_cells(old_move)
                random.shuffle(allowed_cells)
                # if(depth==0):
                #     print "old_move:",old_move
                #     print "The allowed_cells are:"
                #     print allowed_cells
                utility = 0
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker,baseUtility)
                    return value,bestRow,bestCol
                beta=parentBeta    #for a max node, beta is equal to the beta of it's parent node
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j] = currentMarker  #set the board index equal to your currentMarker
                    temp_block_status = temp_board.block_status
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
                    # if(utility>80000):
                    #     print "alpha:",alpha, "beta:",beta, "utility:",utility
                    #     print "DEPTH:",depth
                    #     print "old_move:",old_move
                    #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    #     print temp_board.print_board()
                    #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    #     cnu=0
                    #     while(True):
                    #         cnu+=1

                    if(alpha<beta):  #only call if this condition exists, otherwise prune it. That's why in the else condition, "break" is used.
                        utility,tempRow,tempCol = self.minimax(temp_board,new_move,nextMarker,depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol,baseUtility)
                        if(alpha<utility): #if the new utility is found to be more than current alpha, then of course alpha>=utility. So now, the new worst case is that alpha=utility
                            alpha=utility
                            bestRow=i  #store the best row and col coordinates.
                            bestCol=j
                    else:
                        temp_board.board_status[i][j] = "-" #returning from recursion, so make the state as it was before.
                        temp_board.block_status = temp_block_status #returning from recursion, so make the state as it was before.
                        break
                    temp_board.block_status = temp_block_status
                    temp_board.board_status[i][j] = '-';  #set the board index equal to your currentMarker
            	return alpha,bestRow,bestCol  # return the alpha value found among all it's children
            else :
                # print "old_move:",old_move
                allowed_cells=temp_board.find_valid_move_cells(old_move)
                random.shuffle(allowed_cells)
                # print "The allowed_cells are:"
                # print allowed_cells
                utility = 0
                if(len(allowed_cells)==0):
                    value=self.utilityOfState(temp_board,old_move,currentMarker,baseUtility)
                    return value,bestRow,bestCol
                alpha=parentAlpha
                for i,j in allowed_cells:
                    new_move = [i,j];
                    temp_board.board_status[i][j]=currentMarker
                    temp_block_status = temp_board.block_status
                    self.check_block_status(temp_board,old_move,new_move,currentMarker)
                    # if(utility>80000):
                    #     print "alpha:",alpha, "beta:",beta, "utility:",utility
                    #     print "DEPTH:",depth
                    #     print "old_move:",old_move
                    #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    #     print temp_board.print_board()
                    #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    #     cnu=0
                    #     while(True):
                    #         print "hi"
                    #         cnu+=1
                    if(alpha<beta):
                        utility,tempRow,tempCol=self.minimax(temp_board,new_move,nextMarker, depth+1, -100000.0, 100000.0, alpha, beta, bestRow, bestCol,baseUtility)
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
            # print "move"
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
#            print "bestRow:",bestRow,"bestCol:",bestCol
            baseUtility=self.utilityOfState(temp_board,old_move,currentMarker,0)
            utility, tempRow,tempCol= self.minimax(temp_board, old_move, currentMarker, 0, -100000.0, 100000.0, -100000.0, 100000.0,-1,-1,baseUtility)

            # print self.uptoMaxDepth
            #print "bestRow:",bestRow,"bestCol:",bestCol
            return (tempRow,tempCol) # return the bestRow and bestCol
