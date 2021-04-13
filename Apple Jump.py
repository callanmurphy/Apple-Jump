#Callan Murphy
#11/02/19

'''
A game created to try side-scrolling and gravity/jumping features. The user
controls an apple and can jump between randomly-generated platforms. The user
aims not to fall, but if they do, the game resets.
'''

#NOTE - impossible jumps (oversized gaps)

#initializes pygame and random libraries
import pygame, random
pygame.init()

#clock used for setting FPS
global clock
clock = pygame.time.Clock()

f = open("Data.txt", 'r')
highscore = int(f.read())
f.close
highscore_check = False

#screen properties
WIDTH = 800
HEIGHT = 600
close = 0
col1 = random.randint(100, 250)
col2 = random.randint(100, 250)
col3 = 180#random.randint(0, 250)
pygame.display.set_caption('Apple Jump')
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#user sprite
appleImage = pygame.image.load("apple.png")
appleImage = pygame.transform.scale(appleImage,(50,50))
apple = appleImage.get_rect()
apple.x = 50
apple.y = 450

#platform sprite
platformImage = pygame.image.load("Platform.png")
platformImage = pygame.transform.scale(platformImage,(75,40))
platform = platformImage.get_rect()
platform.x = 50
platform.y = 500

#platform lists
platforms = [platform]
platform_images = [platformImage]

#creation of 9 additional platforms
for i in range(9):
    platform_images.append(pygame.transform.scale(platformImage,(random.randint(30, 150), 40)))
    
for i in range(1,10):
    platforms.append(platform_images[i].get_rect())
    platforms[-1].x = platforms[-2].x + platforms[-2].width + random.randint(60,140)
    platforms[-1].y = 500

jump = 0 #player begins not jumping
check = False #used to check if player is on any platforms
score = 0 #keeps player score

#for keeping track of score
past_platforms = []
font1 = pygame.font.SysFont('Calibri', 35)
scoreText = font1.render('SCORE: ' + str(score), False, (255, 255, 255))
highscoreText = font1.render('HIGHSCORE: ' + str(highscore), False, (255, 255, 255))

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit by pressing x
            pygame.display.quit()
            playing = False
        if event.type == pygame.KEYDOWN: #quit with ESC
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                playing = False

    if playing:

        check = False
        out_of_platforms = True
        
        #player movement
        pressed = pygame.key.get_pressed() #checks if a key has been pressed
        if pressed[pygame.K_a]:
            for i in platforms:
                i.x += 3
            #playerImage = playerLeft
        if pressed[pygame.K_d]:
            for i in platforms:
                i.x -= 3
            #playerImage = playerRight
        if pressed[pygame.K_LEFT]:
            for i in platforms:
                i.x += 3
        if pressed[pygame.K_RIGHT]:
            for i in platforms:
                i.x -= 3

        #jumping
        for i in platforms:
            if jump == 0 and apple.x + 50 > i.x and apple.x < i.x + i.width and apple.y == 450:
                if pressed[pygame.K_SPACE]: jump = 36
                if pressed[pygame.K_UP]: jump = 36
        if jump > 0:
            if jump > 30:
                apple.y -= 4
            elif jump > 24:
                apple.y -= 3
            elif jump > 18:
                apple.y -= 2
            elif jump > 12:
                apple.y += 2
            elif jump > 6:
                apple.y += 3
            else:
                apple.y += 4
            jump -= 1

        #falling
        for i in platforms:
            if apple.x + 50 >= i.x and apple.x <= i.x + i.width and apple.y <= 450:
                check = True #used to check if player is on any platforms

            if apple.y > 450: #used to prevent going through platforms
                if apple.x <= i.x + i.width and apple.x + 50 >= i.x and apple.y < 520:
                    if apple.x > i.x + (i.width//2): #if between middle and right of platform
                        apple.x = i.x + i.width #prevents going through right side of platform
                    else:
                        apple.x = i.x - 50 #prevents going through left side of platform

        #falling
        if check != True: #if player is not on a platform
                if apple.y >= 500:
                    apple.y += 5
                elif apple.y >= 450:
                    apple.y += 4

        #score counter
        for i in platforms:
            if i in past_platforms:
                pass
            else:
                if apple.x + apple.width > i.x and apple.x < i.x + i.width and apple.y == 450 and i != platform:
                    past_platforms.append(i)
                    score += 1
                    scoreText = font1.render('SCORE: ' + str(score), False, (255, 255, 255))
                    col1 = random.randint(100, 250)
                    col2 = random.randint(100, 250)
                    #col3 = random.randint(0, 250)
                    if score >= highscore:
                        highscore_check = True

                    #highscore updater
                    if highscore_check == True:
                        highscore += 1
                        highscoreText = font1.render('HIGHSCORE: ' + str(highscore-1), False, (255, 255, 255))



        #reset to starting location
        if apple.y >= 640:
            highscore_check = False
            score = 0
            scoreText = font1.render('SCORE: ' + str(score), False, (255, 255, 255))
            past_platforms = []
            platform.x = 50
            platform.y = 500
            platforms = [platform]
            platform_images = [platformImage]
            apple.x = 50
            apple.y = 450
            for i in range(9):
                platform_images.append(pygame.transform.scale(platformImage,(random.randint(30, 150),40)))
            for i in range(1,10):
                platforms.append(platform_images[i].get_rect())
                platforms[-1].x = platforms[-2].x + platforms[-2].width + random.randint(60,140)
                platforms[-1].y = 500         
            

        #ensures a platform can always be jumped to
        if len(platforms) == 9:
            platform_images.append(pygame.transform.scale(platformImage,(random.randint(30, 150),40)))
            platforms.append(platform_images[-1].get_rect())
            platforms[-1].y = 500
            platforms[-1].x = platforms[-2].x + platforms[-2].width + random.randint(60,140)
            

        #removes off-screen platforms (saves memory and improves code) - max of 10 platforms
        for i in range(0,len(platforms)-1):
            if platforms[i].x + platforms[i].width < 0:
                platforms.pop(i)
                platform_images.pop(i)
                try: #in case the user falls on the first jump
                    past_platforms.pop(i)
                except:
                    pass

        #screen display
        screen.fill((col1,col2,col3))
        screen.blit(appleImage,apple)
        screen.blit(scoreText,(20,10))
        screen.blit(highscoreText, (20, 60))
        for i in range(len(platforms)):
            screen.blit(platform_images[i], platforms[i])
        pygame.display.flip()

        clock.tick(60)

f = open("Data.txt", 'r')
old_score = int(f.read())
f.close
if highscore-1 > old_score:
    f = open("Data.txt", 'w')
    f.write(str(highscore-1))
    f.close