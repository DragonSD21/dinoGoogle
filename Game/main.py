import pygame as pg
import os
import random
from pynput.keyboard import Key, Controller

import Backend.dinosaur as objDinosaur
import Backend.cactu as objCactu
import Backend.bird as objBird
import Backend.background as objBackground

DIC_PATH = os.path.abspath(os.path.dirname(__file__))

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

pg.init()
SCREEN_DIMENSIONS = [pg.display.Info().current_w, pg.display.Info().current_h-70]
# SCREEN_DIMENSIONS = [800, 600]
# SCREEN_DIMENSIONS = [pg.display.Info().current_w, pg.display.Info().current_h]
GAME_SIZE = [SCREEN_DIMENSIONS[0]/5, SCREEN_DIMENSIONS[1]/50, SCREEN_DIMENSIONS[0]/5 * 3, SCREEN_DIMENSIONS[1]/2]

CACTUS_DIMENSIONS = [[446, 0, 34, 72], [480, 0, 68, 72], [548, 0, 102, 72],
                     [652, 0, 50, 102], [702, 0, 102, 102], [802, 0, 150, 102]]

DINOSAUR_DIMENSIONS = [[76, 6, 90, 96], [1338, 2, 88, 94], [1426, 2, 88, 94], [1514, 2, 88, 94], [1602, 2, 88, 94],
                       [1690, 2, 88, 94], [1782, 6, 80, 86], [1866, 36, 118, 60], [1984, 36, 118, 60]]

PTERODACTYL_DIMENSIONS = [[260, 0, 93, 84], [352, 0, 92, 84]]

BACKGROUND_DIMENSIONS = [[2, 104, 2400, 24]]

def loadImages(imageName):
    try:
        imageAll = pg.image.load(DIC_PATH + imageName)
        imagesDino = [imageAll.subsurface(dimension) for dimension in DINOSAUR_DIMENSIONS]
        imagesBird = [imageAll.subsurface(dimension) for dimension in PTERODACTYL_DIMENSIONS]
        imagesCactu = [imageAll.subsurface(dimension) for dimension in CACTUS_DIMENSIONS]
        imageBackground = [imageAll.subsurface(dimension) for dimension in BACKGROUND_DIMENSIONS]
    except pg.error:
        print("Cannot load image: ", imageName)
        raise SystemExit
    return imagesDino, imagesBird, imagesCactu, imageBackground

def getImagesDimensions(imagesDino, imagesBird, imagesCactu, imageBackground):
    dimensionsDino = [image.get_rect() for image in imagesDino]
    dimensionsBird = [image.get_rect() for image in imagesBird]
    dimensionsCactu = [image.get_rect() for image in imagesCactu]
    dimensionsBackground = [image.get_rect() for image in imageBackground]
    return dimensionsDino, dimensionsBird, dimensionsCactu, dimensionsBackground

def animation(screen, TRex, bird, cactu1, cactu2, background1, background2):
    screen.fill((255, 255, 255)) # preenche a tela com a cor branca
    screen.blit(background1.currentImage, [background1.x, background1.y])
    screen.blit(background2.currentImage, [background2.x, background2.y])
    screen.blit(TRex.currentImage, [TRex.x, TRex.y])
    screen.blit(bird.currentImage, [bird.x, bird.y])
    screen.blit(cactu1.currentImage, [cactu1.x, cactu1.y])
    screen.blit(cactu2.currentImage, [cactu2.x, cactu2.y])
    pg.draw.rect(screen, (0, 0, 0), GAME_SIZE, 1)

    pg.draw.rect(screen, (255, 255, 255), [0, 0, GAME_SIZE[0], GAME_SIZE[3]])
    pg.draw.rect(screen, (255, 255, 255), [GAME_SIZE[0]+GAME_SIZE[2], 0, SCREEN_DIMENSIONS[0], GAME_SIZE[1]+GAME_SIZE[3]])
    pg.display.update()

def randomCactu(cactu1, cactu2, background1):
    if cactu2.x < GAME_SIZE[0] + GAME_SIZE[2]:
        cactu1.changeCurrentImage()
        cactu1.calculateCoordinates(background1)
        cactu1.x = GAME_SIZE[0] + GAME_SIZE[2] - 1
    else:
        cactu2.changeCurrentImage()
        cactu2.calculateCoordinates(background1)
        cactu2.x = GAME_SIZE[0] + GAME_SIZE[2] - 1

def randomBird(bird, background1):
    bird.calculateCoordinates(background1)
    bird.x = SCREEN_DIMENSIONS[0]-1

def randomObstacle(gameTime, bird, cactu1, cactu2, background1):
    randomCactu(cactu1, cactu2, background1)
    # if gameTime < 1:
    #     randomCactu(cactu1, cactu2, background1)
    # else:
    #     if bird.x >= -bird.dimensionsBird[2] and bird.x <= SCREEN_DIMENSIONS[0]:
    #         return
    #     else:
    #         choice = random.randint(0, 2)
    #         if choice:
    #             randomCactu(cactu1, cactu2, background1)
    #         else:
    #             randomBird(bird, background1)

def render():
    keyboard = Controller()

    close = False

    gameSpeed = 4
    gameTime = 0

    generatePossibleObstacle = 0 # até 5
    
    screen = pg.display.set_mode(SCREEN_DIMENSIONS) # largura / altura
    pg.display.set_caption("T-Rex Running")

    imagesDino, imagesBird, imagesCactu, imageBackground = loadImages("/assets/imageGeneral.png")
    dimensionsDino, dimensionsBird, dimensionsCactu, dimensionsBackground = getImagesDimensions(imagesDino, imagesBird, imagesCactu, imageBackground)
    # imagesTeste = [pg.transform.scale(image, [int(GAME_SIZE[2]/10), int(GAME_SIZE[3]/4)]) for image in imagesDino]

    # TRex = objDinosaur.Dinosaur(imagesDino, GAME_SIZE)
    TRex = objDinosaur.Dinosaur(imagesDino, GAME_SIZE)
    bird = objBird.Bird(SCREEN_DIMENSIONS[0]+1, imagesBird)
    cactu1 = objCactu.Cactu(imagesCactu, GAME_SIZE)
    cactu2 = objCactu.Cactu(imagesCactu, GAME_SIZE)
    background1 = objBackground.Background(imageBackground, GAME_SIZE, 0)
    background2 = objBackground.Background(imageBackground, GAME_SIZE, 1)

    isJump = False
    isDown = False
    jumpCountMax = 25
    jumpCount = jumpCountMax

    countFrameDino = 0
    countFrameBird = 0

    # TRex.calculateInitialCoordinates(background1)
    TRex.calculateCoordinates(background1)

    while close != True:
        gameTime += 0.01
        generatePossibleObstacle += 0.1

        if generatePossibleObstacle >= 40:
            # keyboard.press(Key.up)
            # keyboard.release(Key.up)
            randomObstacle(gameTime, bird, cactu1, cactu2, background1)
            generatePossibleObstacle = 0
        pg.time.delay(5)

        animation(screen, TRex, bird, cactu1, cactu2, background1, background2);
        close = TRex.colied([cactu1, cactu2]);

        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = True

        keys = pg.key.get_pressed()
        
        if keys[pg.K_ESCAPE]:
            close = True

        if keys[pg.K_UP]:
            isJump = True

        if keys[pg.K_DOWN]:
            isDown = True
        else:
            isDown = False

        if isJump:
            if jumpCount >= -jumpCountMax:
                TRex.jump(jumpCount)
                jumpCount -= 0.53
            else:
                jumpCount = jumpCountMax
                isJump = False
                TRex.walk()
        elif isDown:
            # timeout
            if countFrameDino > 10:
                TRex.down()
                countFrameDino = 0
            countFrameDino += 1
            TRex.calculateCoordinates(background1)
        else:
            # timeout
            if countFrameDino > 10:
                TRex.walk()
                countFrameDino = 0
            countFrameDino += 1
            TRex.calculateCoordinates(background1)

        # timeout
        if bird.x < GAME_SIZE[0] + GAME_SIZE[2]:
            bird.move(gameSpeed)
            if countFrameBird > 15:
                # cactu1.changeCurrentImage()
                bird.fly()
                countFrameBird = 0
            countFrameBird += 1

        if cactu1.x < GAME_SIZE[0] + GAME_SIZE[2]:
            cactu1.move(gameSpeed, GAME_SIZE)
        if cactu2.x < GAME_SIZE[0] + GAME_SIZE[2]:
            cactu2.move(gameSpeed, GAME_SIZE)

        background1.move(gameSpeed, GAME_SIZE)
        background2.move(gameSpeed, GAME_SIZE)

    pg.quit()

render()
