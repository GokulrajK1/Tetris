import pygame
import random
from constants import *

class Square:
    width = SQUARE_WIDTH

    def __init__(self, gridX, gridY, color, mainGrid) -> None:
        self.x = gridX * self.width
        self.y = gridY * self.width
        self.gridX = gridX
        self.gridY = gridY
        self.mainGrid = mainGrid
        self.color = color 

    def __repr__(self) -> str:
        return f"Square @ ({self.gridX},{self.gridY})"

    def draw(self, surface:pygame.Surface, border=True, borderColor=BLACK):
        rect = pygame.Rect(
            (self.x, self.y, self.width, self.width))
        pygame.draw.rect(surface, self.color, rect) 
        pygame.draw.rect(surface, borderColor, rect, 1) if border else None

class Tile:
    def __init__(self, piece, cartCoord, color) -> None:
        self.piece = piece
        self.cartCoord = cartCoord
        self.color = color
        self.width = Square.width

    @property
    def gridCoord(self):
        conversionX = self.piece.converters[0]
        conversionY = self.piece.converters[1]
        pieceX, pieceY = self.piece.startCoord
        return (pieceX + conversionX[self.cartCoord[0]], pieceY + conversionY[self.cartCoord[1]])

    @property
    def posCoord(self):
        gridX, gridY = self.gridCoord
        return (gridX*self.width, gridY*self.width)

    def __repr__(self) -> str:
        return f"{self.__class__} @ {self.posCoord}"

    def draw(self, surface: pygame.Surface, border):
        rect = pygame.Rect((self.posCoord[0], self.posCoord[1], self.width, self.width))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1) if border else None

class Piece:
    def __init__(self, pieceType, color, mainGrid) -> None:
        self.pieceType = pieceType
        self.color = color
        self.mainGrid = mainGrid
        self.tiles = []
        self.width = 4
        self.startCoord = (COLUMNS//2 - self.width//2, 0)

    @property
    def converters(self):
        if self.pieceType in ["I", "O"]:
            return ({-2: 0, -1: 1, 1: 2, 2: 3},
                    {-2: 3, -1: 2, 1: 1, 2: 0})
        else:
            return ({-1: 0, 0: 1, 1: 2},
                    {-1: 2, 0: 1, 1: 0})

    def rotate(self):
        for tile in self.tiles:
            cartX, cartY = tile.cartCoord
            tile.cartCoord = (cartY, -cartX)

    def addTile(self, cartCoord):
        newTile = Tile(self, cartCoord, self.color)
        self.tiles.append(newTile)

    def createTiles(self):
        if self.pieceType == "I":
            for i in range(4):
                self.addTile(I_PIECE_COORDS[i])
        elif self.pieceType == "O":
            for i in range(4):
                self.addTile(O_PIECE_COORDS[i])
        elif self.pieceType == "T":
            for i in range(4):
                self.addTile(T_PIECE_COORDS[i])
        elif self.pieceType == "L":
            for i in range(4):
                self.addTile(L_PIECE_COORDS[i])
        elif self.pieceType == "J":
            for i in range(4):
                self.addTile(J_PIECE_COORDS[i])
        elif self.pieceType == "Z":
            for i in range(4):
                self.addTile(Z_PIECE_COORDS[i])
        elif self.pieceType == "S":
            for i in range(4):
                self.addTile(S_PIECE_COORDS[i])

        for i in range(random.randrange(4)):
            self.rotate()

    def drawSquares(self, surface: pygame.Surface, border=True):
        for tile in self.tiles:
            tile.draw(surface, border)

    def canStrafeRight(self):
        for tile in self.tiles:
            gridX, gridY = tile.gridCoord
            if gridX == len(self.mainGrid.grid[0]) -1:
                return False 
            if self.mainGrid.grid[gridY][gridX+1]:
                return False
        return True 

    def strafeRight(self):
        if self.canStrafeRight():
            self.startCoord = (self.startCoord[0] + 1, self.startCoord[1])

    def canStrafeLeft(self):
        for tile in self.tiles:
            gridX, gridY = tile.gridCoord
            if gridX == 0:
                return False 
            if self.mainGrid.grid[gridY][gridX-1]:
                return False 
        return True 

    def strafeLeft(self):
        if self.canStrafeLeft():
            self.startCoord = (self.startCoord[0] - 1, self.startCoord[1])

    def canFall(self):
        for square in self.tiles:
            gridX, gridY = square.gridCoord
            if gridY == len(self.mainGrid.grid) - 1:
                return False 
            if self.mainGrid.grid[gridY+1][gridX]:
                return False
        return True   

    def fallTiles(self):
        if self.canFall():
            self.startCoord = (self.startCoord[0], self.startCoord[1]+1)
            return False 
        else:
            self.mainGrid.insertInGrid(self)
            return self.mainGrid.insertNewPiece()

    def instantFall(self):
        while self.canFall():
            self.startCoord = (self.startCoord[0], self.startCoord[1]+1)
        self.mainGrid.insertInGrid(self)
        return self.mainGrid.insertNewPiece()

class Grid:
    def __init__(self, rows, columns, item=0) -> None:
        self.rows = rows
        self.columns = columns
        self.grid = [[item for c in range(columns)] for r in range(rows)]

    @property
    def allSpaces(self):
        allList = []
        for row in self.grid:
            for space in row:
                allList.append(space)
        return allList           

    def drawGrid(self, surface, borderColor=BLACK): 
        for space in self.allSpaces:
            if space:
                space.draw(surface, borderColor=borderColor)

    def fillGrid(self, withSquares):
        for yIndex, row in enumerate(self.grid):
            for xIndex, space in enumerate(row):
                item = Square(xIndex, yIndex, BLACK, self) if withSquares else 0
                self.grid[yIndex][xIndex] = item 
    def insertInGrid(self, piece): 
        for tile in piece.tiles:
            gridX, gridY = tile.gridCoord
            self.grid[gridY][gridX] = Square(gridX, gridY, tile.color, self)

    def insertNewPiece(self):
        index = random.randrange(len(PIECE_TYPES))
        newPiece = Piece(PIECE_TYPES[index], PIECE_COLORS[index], self)
        newPiece.createTiles()
        return newPiece

    def dropSquares(self, partialGrid):
        reversedPartialGrid = reversed(partialGrid)
        for row in reversedPartialGrid:
            for space in row:
                if space:
                    space.y += Square.width

    def clearFilledRows(self):
        for index, row in enumerate(self.grid):
            if row.count(0) == 0:
                self.dropSquares(self.grid[:index]) 
                self.grid.pop(index)
                self.grid.insert(0, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def checkIfGameOver(self):
        if self.grid[5].count(0) != COLUMNS:
            return True 
        return False 

class Timer:
    def __init__(self, num) -> None:
        self.num = num
        self.counter = 0

    def setTimerFor(self, func, keyPressed=True):
        if keyPressed:
            if self.counter == 0:
                self.counter = self.num
                return func()
            self.counter -= 1
        else:
            self.counter = 0

    def reset(self):
        self.counter = 0 

class Label:
    def __init__(self, fontSize=50, text="", color=WHITE) -> None:
        self.x, self.y = 0, 0
        self.font = pygame.font.SysFont("Corbel", fontSize)
        self.text = text
        self.color = color
    def createText(self):
        return self.font.render(self.text, True, self.color)
    def blit(self, win, x=0, y=0, centerX=False, centerY=False):
        text = self.createText()
        if centerX:
            width = text.get_width()
            self.x = G_WIDTH/2 - width/2
        else:
            self.x = x
        if centerY:
            height = text.get_height()
            self.y = G_HEIGHT/2 - height/2 
        else:
            self.y = y 
        win.blit(text, (self.x, self.y))

class Button(Label):
    def __init__(self, fontSize=25, text="", color=WHITE) -> None:
        super().__init__(fontSize, text, color)
    def mouseHover(self):
        text = self.createText()
        width = text.get_width()
        height = text.get_height()
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.x and mousePos[0] <= self.x + width:
            if mousePos[1] >= self.y and mousePos[1] <= self.y + height:
                self.color = LIGHT_GRAY
                return True 
        self.color = WHITE
        return False 

