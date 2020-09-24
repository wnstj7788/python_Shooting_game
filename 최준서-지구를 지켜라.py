import pygame
import sys
import random
from time import sleep


padWidth = 480   #화면의 가로크기 
padHeight = 640  #화면의 세로크기
rockImage = ['rock01.png','rock02.png','rock03.png','rock04.png','rock05.png',\
             'rock06.png','rock07.png','rock08.png','rock09.png','rock10.png',\
             'rock11.png','rock12.png','rock13.png','rock14.png','rock15.png',\
             'rock16.png','rock17.png','rock18.png','rock19.png','rock20.png',\
             'rock21.png','rock22.png','rock23.png','rock24.png','rock25.png',\
             'rock26.png','rock27.png','rock28.png','rock29.png','rock30.png']

explosionSound=['explosion01.wav','explosion02.wav','explosion03.wav','explosion04.wav']


# 운석을 맞춘 개수 계산하기
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('파괴한 운석 수 :' + str(count),True,(255,255,255))
    gamePad.blit(text,(10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf',20)
    text = font.render('놓친 운석  :' + str(count),True,(255,0,0))
    gamePad.blit(text,(360,0))

def writeMessage(text):
    global gamePad,gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf',60)
    text = textfont.render(text,True,(255,0,0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2,padHeight/2)
    gamePad.blit(text,textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.play()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage('전투기파괴!')

def gameOver():
    global gamePad
    writeMessage('게임오버!')
    
    


#게임에 등장하는 객체 드로잉
def drawObject(obj, x,y):
    global gamePad
    gamePad.blit(obj,(x,y))

def initGame():
    global gamePad, clock, background,fighter,missile,explosion,missileSound,gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth,padHeight))
    pygame.display.set_caption('최준서 - 지구를 지켜라')  #게임 이름을 지정
    background = pygame.image.load('background.png') # 배경이름
    fighter = pygame.image.load('fighter.png')#비행기 이미
    missile = pygame.image.load('missile.png')#미사일 이미지
    explosion = pygame.image.load('explosion.png')# 폭팔이미지
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    missileSound =pygame.mixer.Sound('missile.wav')
    gameOverSound =pygame.mixer.Sound('gameover.wav')
    clock = pygame.time.Clock()



def runGame():
    gamePad,clock, background ,fighter,missile,explosion

    
    
    #전투기 크기 지정 
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    #전투기 초기 위치 (x,y)
    x = padWidth * 0.45  #폭에서 0.45위치 0.9위치
    y = padHeight * 0.9
    fighterX = 0
    
    #미사일 좌표 리스트
    missileXY = []

    #운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석의 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    #미사일에 맞은 경우에는 TRUE
    isShot =False
    shotCount = 0
    rockPassed = 0
    

    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in[pygame.QUIT]: #게임 프로그램 종료 
                pygame.quit()
                sys.exit()
                
                #전투기 이동 표현 
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:#왼쪽
                    fighterX -=5

                elif event.key == pygame.K_RIGHT:#오른쪽
                        fighterX +=5
                elif event.key == pygame.K_SPACE: # 미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth/2 #전투기 중간에서 출발
                    missileY = y - fighterHeight  #전체 y좌표에서 전투기 높이 만큼 뻄 
                    missileXY.append([missileX,missileY])

            if event.type in [pygame.KEYUP]:#방향키 멈추면 전투기 멈춤 
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX =0
                    

        drawObject(background, 0 ,0) # 배경화면 그리기

        # 전투기 위치 재조정
        x +=fighterX
        if x <0:
            x =0
        elif x > padWidth -fighterWidth:
            x = padWidth - fighterWidth
            
        #전투기와 운석이 충동했는지 확
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                     (rockX + rockWidth> x and rockX + rockWidth < x + fighterWidth):
                crash()

            
        drawObject(fighter,x,y) # 전투기 게임화면에 그리기
        
        #미사일 발사 장면 구현하기
        if len(missileXY) != 0:
            for i ,bxy in enumerate(missileXY): #미사일 요소 반복함
                bxy[1] -=10 # 미사일 y좌표 -10 (위로이동)
                missileXY[i][1] = bxy[1]


                #미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0]>rockX and bxy[0]< rockX+rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                        

                if bxy[1]<=0: # 화면을 넘어가면 미사일이
                    try:
                        missileXY.remove(bxy)# 미사일 삭제
                    except:
                        pass

                    
        if len(missileXY) != 0:
            for bx,by in missileXY:
                drawObject(missile,bx,by)


        writeScore(shotCount)

        #운석 아래로 움직이기
        rockY += rockSpeed
        #운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #랜덤으로 운석을 하나더 생성하기
            rock =pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWIdth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed +=1

        # 3 놓치면 탈락 
        if rockPassed ==3:
            gameOver()

        writePassed(rockPassed)
        #운석을 맞춘 경우

        if isShot:
            #운석폭발 
            drawObject(explosion, rockX,rockY)# 폭발 그림
            destroySound.play()

            #새로운 운석
            rock =pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWIdth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10
            


            
        drawObject(rock,rockX,rockY) # 운석 그리기 
            


        pygame.display.update()# 게임 화면을 다시 그림
        
        clock.tick(60)# 화면 초당 60프레임 

    pygame.quit() #pygame 종료 

initGame()
runGame()
                
    
