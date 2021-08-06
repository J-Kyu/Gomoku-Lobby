

GRID_SIZE = 10 



class Gomoku:

    def __init__(self):
        
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.whiteTokenID = None
        self.blackTokenID = None
        self.currentTurn = None

    def __init__(self,whiteTokenID,blackTokenID):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.whiteTokenID = whiteTokenID
        self.blackTokenID = blackTokenID
        self.currentTurn = [self.whiteTokenID,self.blackTokenID]


    def CheckTurn(self,tokenID):

        print('Debug-----{0} \t\t cur: {1}'.format(tokenID,self.currentTurn[0]))
        if tokenID == self.currentTurn[0]:
            return True
        else:
            return False


    def CheckEmptyLocation(self,inX,inY):

        # type conversion
        x = int(inX)
        y = int(inY)

        # check range
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return False

        # check if location is available
        if self.grid[y][x] == 0:
            return True
        else:
            return False

    def LocatePos(self,tokenID,inX,inY):
        x = int(inX)
        y = int(inY)

        # check turn
        if not self.CheckTurn(tokenID):
            print("Wrong Turn")
            return False
        
        # check valid location 
        if not self.CheckEmptyLocation(x,y):
            print("Not Empty Loc")
            return False

        # now locate dol
        if tokenID == self.whiteTokenID:
            #white
            self.grid[y][x] = 1
        else:
            #black
            self.grid[y][x] = -1
        # swap turn
        self.currentTurn = self.currentTurn[::-1]
        return True


    def GetGrid(self):
        return self.grid


    def CheckGameOver(self):

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != 0:


                    targetColor = self.grid[y][x]
                    # check 3 o'clock
                    if x <= GRID_SIZE - 5  and y <= GRID_SIZE - 5 and  targetColor == self.grid[y][x+1]==self.grid[y][x+2]==self.grid[y][x+3]==self.grid[y][x+4]:
                        if targetcolor == -1:
                            return True, self.blacktokenid
                        else:
                            return True, self.whitetokenid
                    # check  4:30 
                    if x <=  GRID_SIZE - 5 and y <= GRID_SIZE - 5 and targetColor == self.grid[y+1][x+1]==self.grid[y+2][x+2]==self.grid[y+3][x+3]==self.grid[y+4][x+4]:
                        if targetColor == -1:
                            return True, self.blackTokenID
                        else:
                            return True, self.whiteTokenID
                    # check 6 o'clock
                    if x <= GRID_SIZE - 5 and y <= GRID_SIZE - 5 and targetColor == self.grid[y+1][x]==self.grid[y+2][x]==self.grid[y+3][x]==self.grid[y+4][x]:
                        if targetcolor == -1:
                            return True, self.blacktokenid
                        else:
                            return True, self.whitetokenid
                    # check 7:30
                    if x >= 4 and y <= GRID_SIZE - 5 and  targetColor == self.grid[y+1][x-1]==self.grid[y+2][x-2]==self.grid[y+3][x-3]==self.grid[y+4][x-4]:
                        if targetcolor == -1:
                            return True, self.blacktokenid
                        else:
                            return True, self.whitetokenid
        return False, None
                    

