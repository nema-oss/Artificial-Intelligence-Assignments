def result(board, i):
    q = board[i]
    board[i]=0
    for j in range(i+1, len(board)):
        if q==0:
            if i<6 and j<6 and board[j]==0:
                board[6]+=1
                board[6]+=board[12-j]
                board[12-j]=0
            break
        q-=1
        board[j]+=1
    for j in range(0, i):
        if q==0:
            break
        q-=1
        board[j]+=1
    return board

board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
board = [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0]
print(result(board, 10))