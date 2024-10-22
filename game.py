import pygame
from constants import *
from objects import Button, Grid, Label, Piece, Timer

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
game = pygame.Surface((G_WIDTH, G_HEIGHT))
score = pygame.Surface((G_WIDTH, SQUARE_WIDTH*5))

mainGrid = Grid(ROWS, COLUMNS)
displayGrid = Grid(ROWS, COLUMNS)
displayGrid.fillGrid(True)
rotateTimer = Timer(40)
fallTimer = Timer(2000)
fallInstantTimer = Timer(600)
strafeRightTimer = Timer(600)
strafeLeftTimer = Timer(600)

titleLabel = Label(text="Tetris", fontSize=65)
pauseButton = Button(text="Pause")
resumeButton = Button(text="Resume")
restartButton = Button(text="Restart")

def main():
    piece = mainGrid.insertNewPiece()
    gamePaused = False 
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pauseButton.mouseHover():
                    gamePaused = True
                if resumeButton.mouseHover():
                    gamePaused = False 
                if restartButton.mouseHover():
                    mainGrid.fillGrid(False) 
                    piece = mainGrid.insertNewPiece()
                    gamePaused = False 
                    titleLabel.text = "Tetris"

        if not gamePaused:
            keys = pygame.key.get_pressed()

            rotateTimer.setTimerFor(piece.rotate, keys[pygame.K_UP])
            strafeRightTimer.setTimerFor(piece.strafeRight, keys[pygame.K_RIGHT])
            strafeLeftTimer.setTimerFor(piece.strafeLeft, keys[pygame.K_LEFT])

            if newPiece := fallInstantTimer.setTimerFor(piece.instantFall, keys[pygame.K_SPACE]):
                piece = newPiece
            if keys[pygame.K_DOWN]:
                if newPiece := piece.fallTiles():
                    piece = newPiece
                pygame.time.wait(100)
            if newPiece := fallTimer.setTimerFor(piece.fallTiles):
                piece = newPiece
                

            mainGrid.clearFilledRows()

            if mainGrid.checkIfGameOver():
                gamePaused = True 
                titleLabel.text = "Game Over"

        pauseButton.mouseHover()
        resumeButton.mouseHover()
        restartButton.mouseHover()

        updateDisplay(piece)
    pygame.quit()


def updateDisplay(piece:Piece):
    win.fill(DARK_GRAY)
    win.blit(game, (0, 0))
    win.blit(score, (0, 0))
    game.fill(BLACK)
    displayGrid.drawGrid(game, DARK_GRAY)
    score.fill(DARK_GRAY)
    piece.drawSquares(game)
    mainGrid.drawGrid(game)
    titleLabel.blit(win, y=10, centerX=True)
    pauseButton.blit(win, x=15, y=BUTTON_HEIGHT, centerX=False, centerY=False)
    resumeButton.blit(win, centerX=True, y=BUTTON_HEIGHT)
    restartButton.blit(win, x=180, y=BUTTON_HEIGHT)
    pygame.display.update()

main()
